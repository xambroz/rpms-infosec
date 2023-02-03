#!/bin/bash

PACKAGE=$1

find "./$PACKAGE" -maxdepth 1 -type d | grep -v -E '^./$|^./.git' | \
while read I ; do
    PACKAGE=$(basename "$I")
    grep -i "NoSource:" "${I}/${PACKAGE}.spec"
    if [ $? -eq 0 ] ; then
        # Do not add to COPR the binary packages
        continue
    fi

    copr add-package-scm --clone-url "https://github.com/xambroz/rpms-infosec" \
        --subdir "${PACKAGE}" \
        --spec "${PACKAGE}.spec" \
        --type git \
        --method make_srpm \
        --name "${PACKAGE}" \
        --webhook-rebuild on \
        rebus/infosec

    # package probably already exists, fix parameters
    if [ $? -ne 0 ] ; then
        copr edit-package-scm --clone-url "https://github.com/xambroz/rpms-infosec" \
        --subdir "${PACKAGE}" \
        --spec "${PACKAGE}.spec" \
        --type git \
        --method make_srpm \
        --name "${PACKAGE}" \
        --webhook-rebuild on \
        rebus/infosec
    fi


done
