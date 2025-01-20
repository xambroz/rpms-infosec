Summary:        John the Ripper password cracker
Name:           john-jumbo
Version:        1.9.0
%global         baserelease     8
%global         jumbo_version 1

License:        GPL-2.0-only
URL:            http://www.openwall.com/john
VCS:            https://github.com/openwall/john
Group:          Applications/System

# everything is generated with debug, but then it fails
# RPM build errors:
#   Could not open %%files file /rpmbuild/BUILD/john-4222aa48e282fdd608b4b54a7efadb834a999b42/debugsourcefiles.list: No such file or directory
%bcond_with     debug

%if %{without debug}
%global debug_package %{nil}
%endif

%global         common_desc     %{expand:
John the Ripper is a fast password cracker. Its primary purpose is to
detect weak Unix passwords, but a number of other hash types are
supported as well.
This package includes the john added with the jumbo %{jumbo_version} patch to
add many more types of the passwords.
}

%global         gituser         openwall
%global         gitname         john
%global         commit          4222aa48e282fdd608b4b54a7efadb834a999b42
%global         gitdate         20231204
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# bcond_without = By default build from the release tarball
# to build from git snapshot use rpmbuild --rebuild python-impacket.*.src.rpm --without release
# bcond_with    = build from git snapshot
%bcond_with  release

%if %{with release}
Release:        %{baserelease}.jumbo.%{jumbo_version}%{?dist}

Source0:        http://www.openwall.com/john/k/john-%{version}-jumbo-%{jumbo_version}.tar.xz
Source1:        http://www.openwall.com/john/k/john-%{version}-jumbo-%{jumbo_version}.tar.xz.sign


# This patch fixes build issue, which results in following error message:
# dynamic_fmt.o: In function `DynamicFunc__crypt_md5_to_input_raw_Overwrite_NoLen':
# .../BUILD/john-1.8.0-jumbo-1/src/dynamic_fmt.c:4989: undefined reference to `MD5_body_for_thread'
# https://github.com/magnumripper/JohnTheRipper/issues/1093
Patch0:         john-jumbo-inlines.patch

# Patch needed to be able to compule with the support of opencl
# already fixed in the upstream development version
Patch1:         https://github.com/openwall/john/commit/4f5f6fc8dca0102da7e307e44d5600af04c00ca9.patch#/john-jumbo-opencl.patch

# Fix gcc11 compile error about alignment of struct.
# https://github.com/openwall/john/issues/4604
# https://bugzilla.redhat.com/show_bug.cgi?id=1937076
Patch2:         https://patch-diff.githubusercontent.com/raw/openwall/john/pull/4611.patch#/john-jumbo-gcc11.patch

%else
Release:        %{baserelease}.jumbo.%{jumbo_version}.git%{gitdate}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz#/%{name}-%{version}-%{gitdate}-%{shortcommit}.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       john = %{version}

# Ignore perl dependencies in the /extra directory
%filter_requires_in %{_datarootdir}/%{name}/extra
%filter_setup


Buildrequires:  gcc
Buildrequires:  yasm
Buildrequires:  make
Buildrequires:  binutils
Buildrequires:  autoconf
Buildrequires:  grep
Buildrequires:  findutils
Buildrequires:  coreutils
Buildrequires:  pkgconf-pkg-config
Buildrequires:  perl-interpreter
# For optional AES-NI support
Buildrequires:  yasm
# Fix python scripts
Buildrequires:  python%{python3_pkgversion}-future
Buildrequires:  python%{python3_pkgversion}-future
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

Buildrequires:  nss-devel
Buildrequires:  krb5-devel
Buildrequires:  gmp-devel
Buildrequires:  opencl-headers
Buildrequires:  openssl-devel
Buildrequires:  zlib-devel
Buildrequires:  libpcap-devel
Buildrequires:  bzip2-devel



%description
%{common_desc}


%prep
%if %{with release}
# Build from git release version
%autosetup -p 1 -n john-%{version}-jumbo-%{jumbo_version}
%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif

# Unbundle
rm run/lib/ExifTool.pm




#rm doc/INSTALL

#fix permissions
chmod go-wx doc/*
chmod a+x doc/extras
sed -i 's#\$JOHN/john.conf#%{_sysconfdir}/%{name}/john.conf#' src/params.h
chmod -R u+r src


# Change env python to python
sed -i -e 's%#![ ]*/usr/bin/env[ ]*python[ ]*$%#!/usr/bin/python2%;
           s%#![ ]*/usr/bin/env[ ]*python3[ ]*$%#!/usr/bin/python3%;
           s%#!/usr/bin/python$%#!/usr/bin/python2%;' \
    run/*.py doc/README.apex doc/Auditing-Kerio-Connect.md

sed -i -e 's%#![ ]*/usr/bin/env[ ]*perl[ ]*$%#!/usr/bin/perl%;' run/*.pl

pushd run
futurize-%{python3_version} -w aix2john.py
popd

# Disable rexgen in the build script
sed -i -e 's/--enable-rexgen//;' src/packaging/build.sh





%build
%set_build_flags

cd src

# -DJOHN_SYSTEMWIDE=1 ... use system-wid installation of john
# -fcommon ... don't complain about redefined global definitions
# -g ... debug
export CFLAGS="$CFLAGS -DJOHN_SYSTEMWIDE=1 -fcommon -g"

#%%configure
# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info
# ./configure --enable-pkg-config
# make

# Do not strip files at install
export STRIP=true
./packaging/build.sh



%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 run/john %{buildroot}%{_bindir}/%{name}
install -d -m 755 %{buildroot}%{_libexecdir}/john
install -m 755 run/*.pl %{buildroot}%{_bindir}/
install -m 755 run/*.py %{buildroot}%{_bindir}/
install -m 755 run/*.rb %{buildroot}%{_bindir}/
install -m 755 run/john-* %{buildroot}%{_libexecdir}/john/
install -m 755 run/stats %{buildroot}%{_libexecdir}/john/
install -m 755 run/*.conf %{buildroot}%{_libexecdir}/john/
install -d -m 755 %{buildroot}%{_datarootdir}/%{name}/extra/


for LINK in `find run/ -type l` ; do
    LINKNAME=$(basename "$LINK" )
    pushd %{buildroot}%{_bindir}
    ln -s %{name} "$LINKNAME"
    popd
done

# Remove files conflicting with john package
rm -f %{buildroot}%{_bindir}/john
rm -f %{buildroot}%{_bindir}/unafs
rm -f %{buildroot}%{_bindir}/unique
rm -f %{buildroot}%{_bindir}/unshadow


# perl-SHA is not in Fedora at the moment
# rm %%{buildroot}%%{_libexecdir}/john/sha-test.pl


# Files in non-productive quality due to missing dependencies in Fedora
for I in itunes_backup2john.pl lion2john-alt.pl pdf2john.pl radius2john.pl sha-test.pl ; do
    [ -f "%{buildroot}%{_bindir}/usr/bin/$I" ] && \
        mv -f %{buildroot}%{_bindir}/usr/bin/${I} %{buildroot}%{_datarootdir}/%{name}/extra/
done

chmod a-x %{buildroot}%{_datarootdir}/%{name}/extra/*.pl &&



%files
%doc doc/*
%doc %{_datarootdir}/%{name}/extra
%license
%{_bindir}/*
%{_libexecdir}/john/john-*
%{_libexecdir}/john/stats
%{_libexecdir}/john/dumb16.conf
%{_libexecdir}/john/dumb32.conf
%{_libexecdir}/john/dynamic.conf
%{_libexecdir}/john/rules-by-rate.conf
%{_libexecdir}/john/rules-by-score.conf
%{_libexecdir}/john/unisubst.conf
%{_libexecdir}/john/dynamic_disabled.conf
%{_libexecdir}/john/dynamic_flat_sse_formats.conf
%{_libexecdir}/john/john.conf
%{_libexecdir}/john/hybrid.conf
# %%{_libexecdir}/john/john.local.conf
%{_libexecdir}/john/korelogic.conf
%{_libexecdir}/john/regex_alphabets.conf
%{_libexecdir}/john/repeats16.conf
%{_libexecdir}/john/repeats32.conf

%changelog
%{?%autochangelog: %autochangelog }
