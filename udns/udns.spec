Name:           udns
Version:        0.6
Release:        1%{?dist}
Summary:        DNS resolver library for both synchronous and asynchronous DNS queries
License:        LGPL-2.1-or-later
URL:            http://www.corpit.ru/mjt/udns.html
Source:         http://www.corpit.ru/mjt/udns/udns-%{version}.tar.gz

# Provide autoconf-style fake prototype for socket to avoid implicit function declarations.
Patch0: udns-configure-c99.patch

BuildRequires: make
BuildRequires: gcc

%description
udns is a resolver library for C (and C++) programs, and a collection
of useful DNS resolver utilities.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1

%build
CFLAGS="%{optflags}" ./configure --enable-ipv6
%{__make} %{?_smp_mflags} all sharedlib

%install
%{__install} -Dp -m0755 libudns.so.0 %{buildroot}%{_libdir}/libudns.so.0
%{__ln_s} -f libudns.so.0 %{buildroot}%{_libdir}/libudns.so
%{__install} -Dp -m0755 dnsget %{buildroot}%{_bindir}/dnsget
%{__install} -Dp -m0444 dnsget.1 %{buildroot}%{_mandir}/man1/dnsget.1

%{__install} -Dp -m0444 udns.3 %{buildroot}%{_mandir}/man3/udns.3
%{__install} -Dp -m0644 udns.h %{buildroot}%{_includedir}/udns.h

%files
%doc COPYING.LGPL NEWS NOTES TODO
%doc %{_mandir}/man1/dnsget.1*
%{_bindir}/dnsget
%{_libdir}/libudns.so.*

%files devel
%doc %{_mandir}/man3/udns.3*
%{_includedir}/udns.h
%{_libdir}/libudns.so

%changelog
* Tue Jul 30 2024 Michal Ambroz <rebus _AT seznam.cz> - 0.6-1
- bump to 0.6

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 10 2024 Michal Ambroz <rebus _AT seznam.cz> - 0.5-1
- bump to 0.5

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Florian Weimer <fweimer@redhat.com> - 0.4-23
- Further C compatibility fixes

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Florian Weimer <fweimer@redhat.com> - 0.4-20
- C99 compatibility fixes for the autoconf-style configure script (#2159628)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Adrian Reber <adrian@lisas.de> - 0.4-11
- Added BR: gcc
- Removed ldconfig scriptlets
- Removed rm -rf at the start of %%install

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Adrian Reber <adrian@lisas.de> - 0.4-1
- updated to 0.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Adrian Reber <adrian@lisas.de> - 0.2-1
- updated to 0.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 14 2008 Adrian Reber <adrian@lisas.de> - 0.0.9-3
- removed rblcheck binary to resolve conflict with package rblcheck

* Wed Jul 16 2008 Adrian Reber <adrian@lisas.de> - 0.0.9-2
- removed static library
- added correct optflags
- fixed license tag

* Thu Nov 22 2007 Dag Wieers <dag@wieers.com> - 0.0.9-1 - +/
- Initial package. (using DAR)
