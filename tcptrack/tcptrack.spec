Name:           tcptrack
Version:        1.4.3
Release:        10%{?dist}
Summary:        Displays information about tcp connections on a network interface

License:        LGPLv2+
URL:            https://github.com/bchretien/tcptrack
Source0:        https://github.com/bchretien/tcptrack/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Build on F36+ has stronger argument type checking and needs this patch
# was already reported upstream in https://github.com/bchretien/tcptrack/pull/10/
Patch0:         https://github.com/bchretien/tcptrack/commit/409007afbce8ec5a81312a2a4123dd83b62b4494.patch#/tcptrack-1.4.3-type-mismatch.patch

BuildRequires: make
BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  ncurses-devel
BuildRequires:  libpcap-devel

%description
tcptrack is a sniffer which displays information about TCP connections
it sees on a network interface. It passively watches for connections on 
the network interface, keeps track of their state and displays a list of
connections in a manner similar to the unix 'top' command. It displays 
source and destination addresses and ports, connection state, idle time, 
and bandwidth usage

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man*/%{name}.*

%changelog
* Thu Jan 19 2023 Michal Ambroz <rebus _AT seznam.cz> - 1.4.3-11
- cherrypick patch to fix format typs

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.3-1
- Fix BR
- UPdate to new upstream version 1.4.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.2-9
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.2-7
- Remove -Werror from AM_CXXFLAGS in src/Makefile.* (FTBFS RHBZ#1107444).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Patrick Uiterwijk <puiterwijk@gmail.com> - 1.4.2-3
- Rebuild for package maintainership change

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Jitesh Shah <jitesh.1337@gmail.com> - 1.4.2-1
- New release 1.4.2
- Heap overflow fix and misc fixes (No official changelog on the website)

* Thu Jul 14 2011 Jitesh Shah <jitesh.1337@gmail.com> - 1.4.0-3
- Fixed a build fault

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-1
- Update to 1.4.0
- Add patch to increase text ui select timeout to reduce cpu usage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 27 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.3.0-1
- Update to 1.3.0
- Added tcptrack-1.3.0-util.patch patch 

* Mon Jan 28 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-5
- Modified lincese to LGPLv2+

* Mon Jan 28 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-4
- Removed minimal version from BuildRequires

* Tue Jan 22 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-3
- Removed "Requires: libpcap >= 0.9.7"

* Tue Jan 22 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-2
- Fixed mixed-use-of-spaces-and-tabs (spaces: line 1, tab: line 13)
- Fixed strange-permission tcptrack-1.2.0.tar.gz 0770
- Fixed strange-permission tcptrack.spec 0770
- Fixed Source0 using %%{name} and %%{version} 

* Mon Jan 21 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-1
- Initial RPM release
