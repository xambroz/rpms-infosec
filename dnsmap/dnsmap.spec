Name:           dnsmap
Version:        0.36
Release:        1%{?dist}
Summary:        Sub-domains bruteforcer
License:        GPL-2.0-or-later
URL:            https://github.com/resurrecting-open-source-projects/dnsmap
# was URL:      http://code.google.com/p/dnsmap/

%global         gituser         resurrecting-open-source-projects
%global         gitname         dnsmap
%global         gitdate         20210226
%global         commit          2e3c23390a47cdf897367737db80f593475ed2a1
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Was Source0:  http://dnsmap.googlecode.com/files/dnsmap-%%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake


%description
dnsmap is a small tool that perform brute-forcing of domains.
It can use a built-in list or an external dictionary file and
saves output to TXT/CSV format.

%prep
%autosetup -p 1
autoreconf -v -i

%build
%configure
%make_build

%install
%make_install

%files
%doc doc ChangeLog README.md TODO
%license COPYING
%{_bindir}/dnsmap*
%{_mandir}/man1/dnsmap-bulk.1*
%{_mandir}/man1/dnsmap.1*

%changelog
* Tue Nov 28 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.36-1
- switch over to the ressurected project on github
- bump to release 0.36

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 06 2018 Fabian Affolter <mail@fabian-affolter.ch> - 0.30-15
- Fix BR
- Update spec file

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 17 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.30-2
- Fix description and summary

* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.30-1
- Update to 0.30
- Fix the license
- Remove dnsmap-0.25-Makefile.patch (included by the upstream)
- Replace generally useful macros by regular commands

* Tue Feb 02 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 0.25-1
- Initial package build
