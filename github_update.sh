#!/bin/bash
GITHUBCONF=~/.config/github.conf
source $GITHUBCONF

PACKAGE=$1

FORCE=0
if [ "$2" == "-f" ] ; then
	FORCE=1
fi

echo "=== Processing package $PACKAGE"
SPECFILE="$PACKAGE/${PACKAGE}.spec"
SPEC=$(cat "$SPECFILE" )
GITNAME=$( echo "$SPEC" | grep "%global[ \t]*gitname" | awk '{print $3;}' )
if [ $? -ne 0 -o "x${GITNAME}" = "x" ] ; then
	echo "=== ERROR: gitname not found in the spec file"
	echo ""
	exit 1
fi

GITUSER=$( echo "$SPEC" | grep "%global[ \t]*gituser" | awk '{print $3;}' )

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
SPECCOMMIT=$( echo "$SPEC" | grep -E '^%global.*commit[ \t]*[a-f0-9]{40}'| awk '{print $3}' | tail -n 1 )

if [ "$GITVERSION" == "$SPECVERSION" -a "$GITCOMMIT" == "$SPECCOMMIT" ] ; then
	echo "=== Package $PACKAGE is up to date: $GITVERSION , commit: $GITCOMMIT"
	echo ""
	exit 0
fi

echo "=== INFO: Package $PACKAGE needs update"
echo "Git version:  $GITVERSION		Commit: $GITCOMMIT"
echo "SPEC version: $SPECVERSION		Commit: $SPECCOMMIT"
echo ""

if [ "$FORCE" -eq 1 ] ; then
	set -x
	echo "=== Updating package $PACKAGE"
	rpmdev-bumpspec --verbose --comment "bump to $GITVERSION" \
		--new "$GITVERSION" "$SPECFILE"
	sed -i -e "s/$SPECCOMMIT/$GITCOMMIT/;" "$SPECFILE"
	git commit "$SPECFILE" -m "$PACKAGE - bump to $GITVERSION"
fi


exit 0

