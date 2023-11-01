#!/usr/bin/bash -eux
. /etc/os-release

version=$(echo "${VERSION_ID}" | cut -d. -f1)
arch="x86_64"

case $NAME in
  "Fedora Linux"|"Fedora")
    mock="fedora-${version}-${arch}"
    repos="local"
    ;;

  "CentOS Stream"|"Red Hat Enterprise Linux")
    mock="centos-stream+epel-next-${version}-${arch}"
    repos="local,local-centos-stream"
    ;;

  *)
    echo "Not supported OS" >&2
    exit 1
    ;;
esac

pkgname=${1}
shift

config="/tmp/${mock}-ci.cfg"

# create mock config if not present
# this makes sure tested version of pyproject-rpm-macros is available
# TODO: check if it has precedence if the release was not bumped in tested PR
if [ ! -f $config ]; then
  original="/etc/mock/${mock}.cfg"
  cp $original $config

  echo -e '\n\n' >> $config
  echo -e 'config_opts["package_manager_max_attempts"] = 10' >> $config
  echo -e 'config_opts["package_manager_attempt_delay"] = 60' >> $config
  echo -e '\n\nconfig_opts[f"{config_opts.package_manager}.conf"] += """' >> $config

  # The zuul CI has zuul-build.repo
  # The Jenkins CI has test-<pkgname>.repo
  # We run this code from various packages, so we support any <pkgname>
  if [ -f /etc/yum.repos.d/zuul-build.repo ]; then
    cat /etc/yum.repos.d/zuul-build.repo >> $config
  else
    cat /etc/yum.repos.d/test-*.repo >> $config
  fi
  echo -e '\n"""\n' >> $config
fi

# prepare the rpmbuild folders, make sure nothing relevant is there
mkdir -p ~/rpmbuild/SRPMS
rm -f ~/rpmbuild/SRPMS/${pkgname}-*.src.rpm

# download the sources and create SRPM
spectool -g ${pkgname}.spec
rpmbuild -bs --define '_sourcedir .' ${pkgname}.spec

# build the SRPM in mock
res=0
mock --verbose --isolation=simple -r $config --enablerepo="$repos" init
mock --verbose --isolation=simple -r $config --enablerepo="$repos" "$@" ~/rpmbuild/SRPMS/${pkgname}-*.src.rpm || res=$?

# move the results to the artifacts directory, so we can examine them
artifacts=${TEST_ARTIFACTS:-/tmp/artifacts}

# on Fedora Rawhide, the directory contains "rawhide" instead of the actual version
pushd /var/lib/mock/${mock}/result || pushd /var/lib/mock/${mock/${version}/rawhide}/result
mv *.rpm ${artifacts}/ || :
for log in *.log; do
 mv ${log} ${artifacts}/${pkgname}-${log}
done
popd

exit $res
