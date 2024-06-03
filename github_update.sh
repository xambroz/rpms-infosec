#!/bin/bash
COPR=rebus/infosec
CHROOTS=$( proxychains copr get rebus/infosec |grep download.copr| sed -e 's/^[ ]*//; s/:.*//' )
PACKAGER=$( rpmdev-packager )
CHDATE=$( LANG=en date "+%a %b %d %Y" )

GITHUBCONF=~/.config/github.conf
source $GITHUBCONF

PACKAGE=$1

FORCE=0
if [ "$2" == "-f" ] ; then
	FORCE=1
fi

echo "=== Processing package $PACKAGE"
if [ -f "$PACKAGE/${PACKAGE}.spec" ] ; then
	SPECFILE="$PACKAGE/${PACKAGE}.spec"
elif [ -f "$PACKAGE/rawhide/${PACKAGE}.spec" ] ; then
	SPECFILE="$PACKAGE/rawhide/${PACKAGE}.spec"
elif [ -f "${PACKAGE}.spec" ] ; then
	SPECFILE="${PACKAGE}.spec"
elif [ -f "$PACKAGE" ] ; then
	SPECFILE="$PACKAGE"
        PACKAGE=$( basename "$PACKAGE" .spec )
else
	"=== ERROR: specfile for package $PACKAGE not found"
	exit 1
fi

SPEC=$(cat "$SPECFILE" )
GITNAME=$( echo "$SPEC" | grep "%global[ \t]*gitname" | awk '{print $3;}' )
if [ $? -ne 0 -o "x${GITNAME}" = "x" ] ; then
	echo "=== ERROR: gitname not found in the spec file"
	echo ""
	exit 1
fi

GITUSER=$( echo "$SPEC" | grep "%global[ \t]*gituser" | awk '{print $3;}' )

GITDATESPEC=$( echo "$SPEC" | grep "%global[ \t]*gitdate" | awk '{print $3;}' )

if [ $? -ne 0 -o "x${GITUSER}" = "x" ] ; then
	echo "ERROR: gituser not found in the spec file"
	echo ""
	exit 1
fi



RELEASES=$( curl --silent -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITAPIKEY" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$GITUSER/$GITNAME/releases" )

if [ $? -ne 0 ] ; then
	echo "ERROR: curl failed"
	echo "https://api.github.com/repos/$GITUSER/$GITNAME/releases"
	echo ""
	exit 1
fi


GITVERSION=$( echo "$RELEASES" | jq '.[0].tag_name' | sed -e 's/^"//; s/"$//; s/^v//; ' | head -n 1 )
SPECVERSION=$( echo "$SPEC" |grep -e '^Version:' | awk '{print $2};' )

HTML_URL=$( echo "$RELEASES" | jq '.[0].html_url' | sed -e 's/^"//; s/"$//;' )

HTML_RELEASE=$( curl --silent -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITAPIKEY" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "$HTML_URL" )

if [ $? -ne 0 ] ; then
	echo "ERROR: curl failed"
	echo "$HTML_URL"
	echo ""
	exit 1
fi


GITCOMMIT=$( echo "$HTML_RELEASE" | grep -o -P '(?<=\/commit\/)[a-f0-9]{40}(?=/hover)' | head -n 1 )
SPECCOMMIT=$( echo "$SPEC" | grep -E '^%global[ \t]*commit[ \t]*[a-f0-9]{40}'| awk '{print $3}' | tail -n 1 )

JSON_COMMIT=$( curl --silent -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITAPIKEY" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$GITUSER/$GITNAME/commits/$GITCOMMIT" )

GITDATE=$( echo "$JSON_COMMIT" | jq ".commit.author.date" | sed -e 's/["-]//g; s/T.*$//;' )


if [ "$GITVERSION" == "$SPECVERSION" -a "$GITCOMMIT" == "$SPECCOMMIT" -a "$GITDATE" == "$GITDATESPEC" ] ; then
	echo "=== Package $PACKAGE is up to date: $GITVERSION , commit: $GITCOMMIT, gitdate: $GITDATE"
	echo ""
	exit 0
fi

echo "=== INFO: Package $PACKAGE needs update"
echo "Git version:  $GITVERSION		Commit: $GITCOMMIT	Gitdate: $GITDATE"
echo "SPEC version: $SPECVERSION		Commit: $SPECCOMMIT	Gitdate: $GITDATESPEC"
echo ""

if [ "$FORCE" -eq 1 ] ; then
	set -x
	echo "=== Updating package $PACKAGE"

	# WARNING - rpmdev-bumpspec doesn't hanlde %baserelease macro
	# rpmdev-bumpspec --verbose --comment "bump to $GITVERSION" "$SPECFILE"

	sed -i -e "s/\\(Version:.*\\)${SPECVERSION}/\\1${GITVERSION}/;
	           s/\\(^%global[ \t]*baserelease[ \t]*\\)[0-9]*/\\11/;
                   s/\\(^%global[ \t]*commit[ \t]*\\)${SPECCOMMIT}/\\1${GITCOMMIT}/;
                   s/\\(^%global[ \t]*gitdate[ \t]*\\)${GITDATESPEC}/\\1${GITDATE}/;
                   s/\\(^%changelog\\)/\\1\\n\* $CHDATE $PACKAGER - ${GITVERSION}-1\n- bump to $GITVERSION\\n/;
        " "$SPECFILE"


	git diff ./
	echo git commit "$SPECFILE" -m "$PACKAGE - bump to $GITVERSION"
fi


exit 0

