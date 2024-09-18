Name:           dd_rescue
Version:        1.99.15
Release:        %autorelease
Summary:        Fault tolerant "dd" utility for rescuing data from bad media
# No version specified
License:        GPL-2.0-only OR GPL-3.0-only
URL:            http://www.garloff.de/kurt/linux/ddrescue/

%global         rhelp_version 0.3.0

Source0:        http://www.garloff.de/kurt/linux/ddrescue/dd_rescue-%{version}.tar.bz2
Source1:        http://www.kalysto.org/pkg/dd_rhelp-%{rhelp_version}.tar.gz
Source2:        http://www.garloff.de/kurt/linux/ddrescue/dd_rescue-%{version}.tar.bz2.asc
#               Public key obtained from http://www.garloff.de/kurt/garloff.pub.asc
Source3:        gpgkey-6669F7340D31E95EC5565490DE4F1B3A2BFFC5BF.gpg

# Fix the dd_rescue version detection in dd_help
Patch0:         dd_rescue-rhelp_version.patch

# Avoid c99 detection on RHEL7
# fixed in 1.99.15
# Patch1:         dd_rescue-noc99.patch

BuildRequires:  autoconf
# We require aclocal which is shipped with automake
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  lzo-devel
BuildRequires:  make

# Shell script dd_rhelp.test requires several other things to run
BuildRequires:  bc
BuildRequires:  grep
BuildRequires:  coreutils

# Shell script dd_rhelp requires several other things to run
Requires:       grep
Requires:       sed
Requires:       coreutils
Requires:       bc





%description
The dd_rescue is a utility similar to the system utility "dd" which copies
data from a file or block device to another. The dd_rescue does however
not abort on errors in the input file. This makes it suitable for
rescuing data from media with errors, e.g. a disk with bad sectors.

This package includes dd_rhelp wrapper script facilitating data
recovery. It is trying to make it so simple to recover as:
dd_rhelp source target

Please note Fedora ships also GNU ddrescue, which probably gives
faster and more reliable results rescuing whole disks.
But still there might be some niche pattern of bad sectors,
which might get better covered by dd_rescue and both tools
might be used with sub-sequent runs cooperatively on the same disk image.


%prep
gpgv2 --keyring %{SOURCE3} %{SOURCE2} %{SOURCE0}
%setup -q -n %{name}-%{version}
%setup -q -n %{name}-%{version} -a 1 -D -T
%autopatch -p 1

%build
autoreconf -vif
%configure

%ifarch ppc64le
rm -f aesni.c find_nonzero_sse2.c find_nonzero_arm.c find_nonzero_arm64.c
%endif
make RPM_OPT_FLAGS="%{optflags}" %{?_smp_mflags} LIB=%{_lib}
cp -p README.dd_rescue README
cp -p dd_rhelp-%{rhelp_version}/README README.dd_rhelp
cp -p dd_rhelp-%{rhelp_version}/FAQ FAQ.dd_rhelp

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIR=%{buildroot}/%{_bindir} INSTASROOT="" INSTALLFLAGS="" LIB=%{_lib}
install -D -m 755 dd_rhelp-%{rhelp_version}/dd_rhelp %{buildroot}%{_bindir}/dd_rhelp

%check
pushd dd_rhelp-%{rhelp_version}
PATH="../:$PATH" bash ./dd_rhelp.test &&
popd


%files
%doc COPYING README README.dd_rhelp FAQ.dd_rhelp
%{_bindir}/dd_rescue
%{_bindir}/dd_rhelp
%{_mandir}/man1/%{name}.*
%{_mandir}/man1/ddr_lzo.*
%{_mandir}/man1/ddr_crypt.*
%{_libdir}/libddr_MD5.so
%{_libdir}/libddr_hash.so
%{_libdir}/libddr_lzo.so
%{_libdir}/libddr_null.so
%{_libdir}/libddr_crypt.so


%changelog
%autochangelog
