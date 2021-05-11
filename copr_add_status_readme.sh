#!/bin/bash
find ./ -maxdepth 1 -type d | sort | cut -d / -f 2 | \
while read I ; do 
    echo "- ![$I](https://copr.fedorainfracloud.org/coprs/rebus/infosec/package/$I/status_image/last_build.png) - $I"
done >> README.md


