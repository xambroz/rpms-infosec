%define rhelp_version 0.3.0

Name:           dd_rescue
Version:        1.99.12
Release:        2%{?dist}
Summary:        Fault tolerant "dd" utility for rescuing data from bad media
# No version specified
License:        GPL+
URL:            http://www.garloff.de/kurt/linux/ddrescue/
Source0:        http://www.garloff.de/kurt/linux/ddrescue/dd_rescue-%{version}.tar.bz2
Source1:        http://www.kalysto.org/pkg/dd_rhelp-%{rhelp_version}.tar.gz
Source2:        http://www.garloff.de/kurt/linux/ddrescue/dd_rescue-%{version}.tar.bz2.asc
#               Public key obtained from http://www.garloff.de/kurt/garloff.pub.asc
Source3:        gpgkey-6669F7340D31E95EC5565490DE4F1B3A2BFFC5BF.gpg

BuildRequires:  autoconf
# We require aclocal which is shipped with automake
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  lzo-devel
BuildRequires:  make

# Shell script dd_rhelp requires several other things to run
Requires:       cat
Requires:       grep
Requires:       sed
Requires:       coreutils
Requires:       bc





%description
ddrescue is a utility similar to the system utility "dd" which copies
data from a file or block device to another. ddrescue does however
not abort on errors in the input file. This makes it suitable for
rescuing data from media with errors, e.g. a disk with bad sectors.

This package includes dd_rhelp, a wrapper script facilitating data
recovery.

%prep
gpgv2 --keyring %{SOURCE3} %{SOURCE2} %{SOURCE0}
%setup -q -n %{name}-%{version}
%setup -q -n %{name}-%{version} -a 1 -D -T

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
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 05 2022 Michal Ambroz <rebus AT seznam dot cz> - 1.99.12-1
- bump to 1.99.12

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 29 2021 Michal Ambroz <rebus AT seznam dot cz> - 1.99.11-1
- bump to 1.99.11

* Mon Mar  8 2021 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.99.10-14
- Update to dd_rescue-1.99.10 and dd_rhelp-0.3.0

* Sat Feb 27 2021 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.99.9-13
- Update to dd_rescue-1.99.9 and dd_rhelp-0.3.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 28 2020 Jeff Law <law@redhat.com> - 1.99.8-12
- Re-enable LTO as upstream GCC target/96939 has been fixed

* Mon Aug 10 2020 Jeff Law <law@redhat.com> - 1.99.8-11
- Disable LTO on armv7 for now

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb  1 2019 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.99.8-6
- On ppc64le, remove x86-only *.c before dep generation breaks the build

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.99.8-3
- Added gcc and gnupg2 buildrequires.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Michal Ambroz <rebus AT seznam dot cz> - 1.99.8-1
- bump to latest upstream release 1.99.8
- add signature as a source file

* Tue Nov 14 2017 Michal Ambroz <rebus AT seznam dot cz> - 1.99.7-1
- bump to latest upstream release 1.99.7

* Sun Oct 29 2017 Michal Ambroz <rebus AT seznam dot cz> - 1.99.6-1
- bump to latest upstream release 1.99.6

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.99.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Michal Ambroz <rebus AT seznam dot cz> - 1.99.5-1
- bump to latest upstream release 1.99.5

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Sep 12 2015 Michal Ambroz <rebus AT seznam dot cz> - 1.99-1
- bump to latest upstream release 1.99

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Michal Ambroz <rebus AT seznam dot cz> - 1.98-1
- bump to latest upstream release 1.98

* Sun Aug 31 2014 Michal Ambroz <rebus AT seznam dot cz> - 1.46-1
- bump to latest upstream release 1.46

* Wed Aug 27 2014 Dan Horák <dan[at]danny.cz> - 1.45-4
- fix build on non-x86 64-bit arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Michal Ambroz <rebus AT seznam dot cz> - 1.45-1
- bump to latest upstream release 1.45

* Sat May 24 2014 Michal Ambroz <rebus AT seznam dot cz> - 1.44-1
- bump to latest upstream release 1.44

* Sat Mar 22 2014 Michal Ambroz <rebus AT seznam dot cz> - 1.42.1-3
- fix libdir to reflect ppc64 

* Sat Mar 22 2014 Michal Ambroz <rebus AT seznam dot cz> - 1.42.1-2
- bump to latest upstream release 1.42.1

* Thu Sep 05 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.40-1
- Update to 1.40.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 04 2013 Michal Ambroz <rebus AT seznam dot cz> - 1.31-1
- bump to latest upstream release 1.31

* Wed Jan 30 2013 Michal Ambroz <rebus AT seznam dot cz> - 1.30-1
- bump to latest upstream release 1.30

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.28-1
- Use mktemp based BuildRoot
- Ship file FAQ.dd_rhelp
- Update to dd_rescue-1.28 and dd_rhelp-0.3.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.23-1
- Update to 1.23.

* Thu Nov 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.22-1
- Update to 1.22.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-8
- fix license tag
