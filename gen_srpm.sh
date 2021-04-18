#!/bin/bash

PACKAGE=$1

spectool -g "${PACKAGE}.spec"
FILE=$( rpmbuild -bs "${PACKAGE}.spec" | tail -n 1 | cut -d ' ' -f 2 )
mv "$FILE" ./


