#!/bin/bash

PACKAGE=$1

if [ -f "${PACKAGE}/changelog" ] ; then
	echo "WARNING: changelog file is already existing, I do not touch that"
else
	echo "WARNING: creating changelog"
	sed '1,/%changelog/d' $PACKAGE/${PACKAGE}.spec > $PACKAGE/changelog
	git add $PACKAGE/changelog
fi

SPECMODIFIED=0
grep "%autochangelog" ${PACKAGE}/${PACKAGE}.spec > /dev/null
if [ $? -eq 0 ] ; then
	echo "WARNING: %autochangelog already found, not touching that"
else
	echo "WARNING: %autochangelog not found, deleting changelog and replacing with %autochangelog"
	sed -i '/%changelog/,$c\%changelog\n%autochangelog' $PACKAGE/${PACKAGE}.spec
	SPECMODIFIED=1
fi

grep "%autorelease" ${PACKAGE}/${PACKAGE}.spec > /dev/null
if [ $? -eq 0 ] ; then
	echo "WARNING: %autorelease already found, not touching that"
else
	echo "WARNING: %autorelease not found, switching to %autorelease"
	sed -i -E 's/(^Release:[ \t]*).*$/\1%aurorelease/'  $PACKAGE/${PACKAGE}.spec
	SPECMODIFIED=1
fi

if [ $SPECMODIFIED -eq 1 ] ; then
	git commit $PACKAGE/${PACKAGE}.spec -m "$PACKAGE .. switched to autorelease/autochangelog"
fi
