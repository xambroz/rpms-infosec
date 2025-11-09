Summary:        John the Ripper password cracker
Name:           john-bleeding
Version:        1.9.0
%global         jumbo_version 1

License:        GPL-2.0-only
URL:            http://www.openwall.com/john
VCS:            git:https://github.com/openwall/john
Group:          Applications/System

# 8yyeverything is generated with debug, but then it fails
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
%global         commit          73baa17cee62c4da9b01fb89554d2e5c76f5ac4e
%global         gitdate         20250401
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         vcsurl          %(vcs=%{vcs}; echo ${vcs:4})


# bcond_without = By default build from the release tarball
# to build from git snapshot use rpmbuild --rebuild python-impacket.*.src.rpm --without release
# bcond_with    = build from git snapshot
%bcond_with     release
%bcond_without  single

%if %{with release}
Release:        %autorelease -s jumbo.%{jumbo_version}

Source0:        %{url}/k/john-%{version}-jumbo-%{jumbo_version}.tar.xz
Source1:        %{url}/k/john-%{version}-jumbo-%{jumbo_version}.tar.xz.sign


# This patch fixes build issue, which results in following error message:
# dynamic_fmt.o: In function `DynamicFunc__crypt_md5_to_input_raw_Overwrite_NoLen':
# .../BUILD/john-1.8.0-jumbo-1/src/dynamic_fmt.c:4989: undefined reference to `MD5_body_for_thread'
# https://github.com/magnumripper/JohnTheRipper/issues/1093
Patch1:         john-bleeding-01-inlines.patch

# Patch needed to be able to compule with the support of opencl
# already fixed in the upstream development version
Patch2:         %{vcsurl}/commit/4f5f6fc8dca0102da7e307e44d5600af04c00ca9.patch#/john-bleeding-02-opencl.patch

# Fix gcc11 compile error about alignment of struct.
# https://github.com/openwall/john/issues/4604
# https://github.com/openwall/john/pull/4611
# https://bugzilla.redhat.com/show_bug.cgi?id=1937076
# https://github.com/openwall/john/commit/154ee1156d62dd207aff0052b04c61796a1fde3b
Patch3:         %{vcsurl}/pull/4611.patch#/john-bleeding-03-gcc11.patch

%else
Release:        %autorelease -s jumbo.%{jumbo_version}.%{gitdate}git%{shortcommit}
Source0:        %{vcsurl}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz#/%{name}-%{version}-%{gitdate}-%{shortcommit}.tar.gz

# To be able to pass the OPTFLAGS and MAKEFLAGS
Patch4:         john-bleeding-04-optflags.patch


%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
# Requires:     john = %%{version}

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
# TODO: Fix python scripts
# Buildrequires:  python%%{python3_pkgversion}-future
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
chmod -R u+r src

# Change configuration directory to allow separate john instances
sed -i -e 's|/usr/libexec/john|/usr/libexec/%{name}|' \
       -e 's|/usr/share/john|/etc/%{name}|' \
       -e 's#\$JOHN/john.conf#%{_sysconfdir}/%{name}/john.conf#' \
       -e 's#\~/\.john#~/.%{name}#' \
    src/params.h

# Change env python to python
echo TODO: python versions
sed -i -e 's%#![ ]*/usr/bin/env[ ]*python[ ]*$%#!/usr/bin/python2%;
           s%#![ ]*/usr/bin/env[ ]*python3[ ]*$%#!/usr/bin/python3%;
           s%#!/usr/bin/python$%#!/usr/bin/python2%;' \
    run/*.py doc/README.apex doc/Auditing-Kerio-Connect.md

sed -i -e 's%#![ ]*/usr/bin/env[ ]*perl[ ]*$%#!/usr/bin/perl%;' run/*.pl

pushd run
echo TODO: futurize-%{python3_version} -w aix2john.py
popd

# Disable rexgen in the build script
sed -i -e 's/--enable-rexgen//;' src/packaging/build.sh


%build
%set_build_flags

cd src

# Use verbose make and fedora optimization flags
export MAKEFLAGS="-j$(nproc) VERBOSE=1"
export OPTFLAGS="%{optflags}"

# -DJOHN_SYSTEMWIDE=1 ... use system-wide installation of john
# -DJOHN_SYSTEMWIDE_HOME=/etc/%{name} ... take the configuration files from the /etc directory
# -fcommon ... don't complain about redefined global definitions
# -g ... debug
export CPPFLAGS="$CFLAGS -DJOHN_SYSTEMWIDE=1 -fcommon -g"

#%%configure
# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info
# ./configure --enable-pkg-config
# make

# Do not strip files at install
export STRIP=true

%if %{with single}
SYSTEM_WIDE='--with-systemwide '
X86_REGULAR="--disable-native-tests --disable-opencl $SYSTEM_WIDE"
./configure $X86_REGULAR  --enable-simd=sse2  CPPFLAGS="-D_BOXED -DOMP_FALLBACK -DOMP_FALLBACK_BINARY=\"\\\"john-sse2\\\"\""
# do_build ../run/john-sse2-omp
make clean
make -j8
mv ../run/john ../run/%{name}-sse2-omp
ln -s %{name}-sse2-omp ../run/%{name}

%else
# Build multiple optimized packages
./packaging/build.sh
%endif


%install

# Directories
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/rules
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -d -m 755 %{buildroot}%{_datarootdir}/%{name}/extra/
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d/

# Binary
install -m 755 run/%{name} %{buildroot}%{_bindir}/%{name}


# Links to john
LINKS="unafs unique undrop unshadow rar2john zip2john gpg2john base64conv"
for I in $LINKS ; do
    ln -f -s %{name} %{buildroot}%{_bindir}/${I}
done

# Standalone binaries
PROJ="eapmd5tojohn tgtsnarf mkvcalcproba calc_stat racf2john hccap2john raw2dyna genmkvpwd putty2john dmg2john uaf2john SIPdump vncpcap2john cprepair bitlocker2john wpapcap2john keepass2john"
for I in $PROJ ; do
    install -m 755 run/${I} %{buildroot}%{_bindir}/
done

# Scripts
install -m 755 run/*.pl %{buildroot}%{_bindir}/
install -m 755 run/*.py %{buildroot}%{_bindir}/
install -m 755 run/*.rb %{buildroot}%{_bindir}/

# Feature binaries
install -m 755 run/%{name}-* %{buildroot}%{_libexecdir}/%{name}/

# Configuration
install -m 644 run/stats %{buildroot}%{_sysconfdir}/%{name}/stats
install -m 644 run/*.conf %{buildroot}%{_sysconfdir}/%{name}/

# Shared files
install -m 644 run/*.chr %{buildroot}%{_sysconfdir}/%{name}/
install -m 644 run/*.lst %{buildroot}%{_sysconfdir}/%{name}/
install -m 644 run/rules/* %{buildroot}%{_sysconfdir}/%{name}/rules/



# Install Bash completion
install -m 755 run/john.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d/%{name}.bash_completion

# Remove files conflicting with john package
%if "%{name}" != "john"
rm -f %{buildroot}%{_bindir}/john
rm -f %{buildroot}%{_bindir}/unafs
rm -f %{buildroot}%{_bindir}/unique
rm -f %{buildroot}%{_bindir}/unshadow
%endif


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
%{_sysconfdir}/%{name}
#%%{_sysconfdir}/%%{name}/stats
#%%{_sysconfdir}/%%{name}/*.conf
%{_bindir}/*
%{_sysconfdir}/bash_completion.d/%{name}.bash_completion
%{_libexecdir}/%{name}/%{name}-*

%changelog
%autochangelog

