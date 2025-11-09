#!/bin/bash

# CHROOT="all"
# CHROOT="fedora-42-x86_64"
CHROOT=${CHROOT:-"all"}

SEQUENCEFILE="sequence.txt"
SEQUENCE=$(cat "$SEQUENCEFILE" | sed -e 's/[ ]*#.*$//' | grep -v -e '^$')

if [ "$CHROOT" = "all" ] ; then
    LASTGOODFILE=${LASTGOODFILE:-"last_good.txt"}
else
    LASTGOODFILE=${LASTGOODFILE:-"last_good_${CHROOT}.txt"}
fi

LASTGOOD=$(cat "$LASTGOODFILE")
SKIP=1
if [ "x${LASTGOOD}" == "x" ] ; then
    SKIP=0
fi

echo "$SEQUENCE" | while read P DEPARGS ; do
    if [ $SKIP -eq 1 -a "$LASTGOOD" != "$P" ] ; then
        echo "=== Skipping: $P"
        continue
    elif [ "$LASTGOOD" == "$P" ] ; then
        echo "=== Skipping: $P"
        SKIP=0
        continue
    fi


    DEPS=$( echo "$DEPARGS" | cut -d '|' -f 1 )
    ARGS=$( echo "$DEPARGS" | cut -d '|' -f 2 )

    if [ "$CHROOT" = "all" ] ; then
        echo "=== Building package $P"
        echo "copr build-package rebus/infosec --name \"$P\" $ARGS"
        MSG=$( proxychains copr build-package rebus/infosec --name "$P" $ARGS )
        RESULT=$((RESULT + $?))
    else
	for C in "$CHROOT" ; do
            echo "=== Building package $P for ${C}"
            echo "copr build-package rebus/infosec --chroot "$C" --name \"$P\" $ARGS"
            MSG=$( proxychains copr build-package rebus/infosec --chroot "$C" --name "$P" $ARGS )
            RESULT=$(($RESULT + $?))
	done
    fi





    if [ "$RESULT" -ne 0 ] ; then
        echo "==== ERROR: failed package $P "
        exit
    else
        echo "==== SUCCESS building package $P"
        echo "$P" > $LASTGOODFILE
    fi
done
