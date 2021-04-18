#!/bin/bash

find ./ -maxdepth 1 -type d | grep -v -E '^./$|^./.git' | \
while read I ; do
    mkdir -p "$I/.copr"
    ln -f -s '../../Makefile.copr' "${I}/.copr/Makefile"
done
