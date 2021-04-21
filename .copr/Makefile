# Makefile proposed by Quentin Dufour
# https://quentin.dufour.io/blog/2018-05-20/build-a-rpm-package-and-publish-it-on-copr/
rpmbuild_src = $(shell rpmbuild --eval '%{_sourcedir}')
PWD = $(shell pwd)
.PHONY: prepare srpm rpm

prepare:
	dnf -y install rpmdevtools rpm-build
	spectool -g -R $(spec)

srpm: prepare
	rpmbuild -bs --define "_sourcedir $(PWD)" --define "_srcrpmdir $(outdir)" $(spec)

rpm: prepare
	rpmbuild -bb --define "_sourcedir $(PWD)"  --define "_rpmdir $(outdir)" $(spec)

