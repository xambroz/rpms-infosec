#!/bin/sh -e
if [ $# -lt 2 ]; then
	echo "Usage: $0 dist <bodhi updates new arguments>"
	exit 1
fi
dist=${1}
shift
if [ ! -f .side-tag-$dist ]; then
   echo "No existing side tag for $dist"
   exit 1
fi

bodhi updates new --from-tag $(cat .side-tag-$dist) "$@"
