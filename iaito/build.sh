#!/bin/sh -xe
branch=${1:-$(git branch --show-current)}
dist=$(echo $branch | cut -d- -f1)
case $dist in
devel)
	dist=rawhide
	;;
esac

fedpkg switch-branch $branch
if [ !-f ../radare2/.side-tag-$branch ]; then
   echo "ERROR: radare2 side tag for $branch missing"
   exit 1
fi
if [ ! -f ../radare2/.ver-$branch ]; then
   echo "ERROR: radare2 build for $branch missing"
   exit 1
fi
tag=$(cat ../radare2/.side-tag-$branch)
build=$(cat ../radare2/.ver-$branch)

git merge rawhide
git push
koji wait-repo $tag --build=$build
fedpkg --release=$dist build --target=$tag
