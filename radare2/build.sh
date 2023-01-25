#!/bin/sh -xe
branch=${1:-$(git branch --show-current)}
dist=$(echo $branch | cut -d- -f1)
case $dist in
devel)
	dist=rawhide
	;;
esac

fedpkg switch-branch $branch
if [ -f .side-tag-$branch ]; then
   echo "Side tag for $branch exists"
   read ok
else
   fedpkg --release $dist request-side-tag > .side-tag-$branch.txt
   head -1 .side-tag-$branch.txt | cut "-d'" -f2 > .side-tag-$branch
fi

git merge rawhide
git push
fedpkg --release $dist verrel > .ver-$branch
fedpkg --release $dist build --target=$(cat .side-tag-$branch)
