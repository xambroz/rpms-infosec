#!/bin/bash

SVN_VERSION=r238
SVN_DATE=20140110

proxychains svn checkout  -r "$SVN_VERSION" https://svn.code.sf.net/p/beye/code/ "beye-${SVN_DATE}"

pushd "beye-${SVN_DATE}"
rm -rf .svn

popd

tar cjvf "beye-${SVN_DATE}.tar.bz2" "beye-${SVN_DATE}"

