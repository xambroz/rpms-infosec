Name:           nwipe
Version:        0.35
Release:        1%{?dist}
Summary:        Securely erase disks using a variety of recognized methods


%global         gituser         martijnvanbrummelen
%global         gitname         nwipe
%global         commit          ab6c4c0014af7e423a4d90ca4e6f201cb30a1f98
%global         gitdate         20201209
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


License:        GPL-2.0-only
# used to be    http://nwipe.sourceforge.net
URL:            https://github.com/martijnvanbrummelen/nwipe
VCS:            https://github.com/martijnvanbrummelen/nwipe
# Releases      https://github.com/martijnvanbrummelen/nwipe/releases

#Source0:       https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Lower the build requirements to autoconf used in rhel6
Patch1:         nwipe-epel6.patch

# Move the usage of int64t bellow the stdint.h include which defines it
Patch2:         nwipe-epel-int64t.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  parted-devel
BuildRequires:  ncurses-devel
BuildRequires:  libconfig-devel
BuildRequires:  autoconf
BuildRequires:  automake

# Recommends only supported on fedora and rhel8+
%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
# used to provide serial number of drive over supported USB to SATA interface
Recommends:     smartmontools
# provide SMBIOS/DMI host data to log file
Recommends:     dmidecode
%endif


%description
The nwipe is a command that will securely erase disks using a variety of 
recognized methods. It is a fork of the dwipe command used by Darik's 
Boot and Nuke (dban). Nwipe was created out of need to run the DBAN dwipe
command outside of DBAN. This allows it to use any host distribution which
gives better hardware support. It is essentially the same as dwipe, with 
a few changes:
- pthreads is used instead of fork
- The parted library is used to detect drives
- The code is designed to be compiled with gcc
- Increased number of wipe methods
- Smartmontools is used to provide USB serial #
- DmiDecode is used to provide host info to nwipes log 

%prep
#autosetup -n %%{gitname}-%%{commit} -p 1
%autosetup -n %{gitname}-%{version} -p 1


%build

# On RHEL7 it is needed to explicitly pregress to c99 compatibility mode
%if 0%{?rhel} && 0%{?rhel} <= 7
export CFLAGS="%{optflags} -std=c99 -D_XOPEN_SOURCE=500"
%endif

autoreconf -vif

%configure
# make %%{?_smp_mflags}
%make_build


%install
# make install DESTDIR=%%{buildroot} LDFLAGS="-lncurses -lpanel"
%make_install


%files
%license COPYING
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Fri Nov 03 2023 Michal Ambroz <rebus at, seznam.cz> 0.35-1
- bump to 0.35

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 05 2022 Michal Ambroz <rebus at, seznam.cz> 0.34-1
- bump to 0.34

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Michal Ambroz <rebus at, seznam.cz> 0.33-1
- bump to 0.33

* Sat Mar 12 2022 Michal Ambroz <rebus at, seznam.cz> 0.32-1
- bump to 0.32

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Feb 20 2021 Nick Law (PartialVolume) <nick.craig.law at, gmail.com> - 0.30-1
- bump to 0.30 - based on PR #1 https://src.fedoraproject.org/rpms/nwipe/pull-request/1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Michal Ambroz <rebus at, seznam.cz> 0.26-1
- bump to 0.26

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 01 2019 Michal Ambroz <rebus at, seznam.cz> 0.25-1
- bump to 0.25

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Michal Ambroz <rebus at, seznam.cz> 0.24-1
- bump to 0.24

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 06 2016 Michal Ambroz <rebus at, seznam.cz> 0.21-3
- fix changelog

* Tue Sep 06 2016 Michal Ambroz <rebus at, seznam.cz> 0.21-1
- bump to 0.21

* Mon Aug 08 2016 Michal Ambroz <rebus at, seznam.cz> 0.20-1
- bump to 0.20

* Thu Aug 04 2016 Michal Ambroz <rebus at, seznam.cz> 0.19-1
- bump to 0.19 - upstream fixes prng and build for fedora<23

* Mon Aug 01 2016 Michal Ambroz <rebus at, seznam.cz> 0.18-1
- bump to 0.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Michal Ambroz <rebus at, seznam.cz> 0.17-3
- fix build on epel6

* Mon Jun 22 2015 Michal Ambroz <rebus at, seznam.cz> 0.17-2
- patch to fix the randr mersene twister on 64bit platform (bug id 1151036)

* Mon Jun 22 2015 Michal Ambroz <rebus at, seznam.cz> 0.17-1
- upgrade to version 0.17, switch to github repository

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 16 2013 Michal Ambroz <rebus at, seznam.cz> 0.14-2
- removed build requirement to autoconf again

* Sat Feb 16 2013 Michal Ambroz <rebus at, seznam.cz> 0.14-1
- upgrade to version 0.14

* Sun Feb 10 2013 Michal Ambroz <rebus at, seznam.cz> 0.13-2
- patched build to check for ncurses independently from panel

* Sun Feb 10 2013 Michal Ambroz <rebus at, seznam.cz> 0.13-1
- upgrade to version 0.13

* Tue Feb 05 2013 Michal Ambroz <rebus at, seznam.cz> 0.12-1
- upgrade to version 0.12

* Mon Sep 24 2012 Michal Ambroz <rebus at, seznam.cz> 0.11-1
- upgrade to version 0.11

* Fri Aug 10 2012 Michal Ambroz <rebus at, seznam.cz> 0.10-1
- upgrade to version 0.10

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Michal Ambroz <rebus at, seznam.cz> 0.08-1
- upgrade to version 0.08

* Thu Mar 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.06-3
- rebuild (parted)

* Fri Jan 06 2012 Michal Ambroz <rebus at, seznam.cz> 0.06-2
- redownload of upstream package - original release of 0.06 contained binaries

* Thu Jan 05 2012 Michal Ambroz <rebus at, seznam.cz> 0.06-1
- added Group field
- FSF address and manpage was fixed upstream
- bump to new version 0.06

* Sun Jan 01 2012 Michal Ambroz <rebus at, seznam.cz> 0.05-3
- added clean stage for EPEL5 compatibility

* Sun Jan 01 2012 Michal Ambroz <rebus at, seznam.cz> 0.05-2
- fixed defattr based on package review from Ivan Romanov

* Wed Dec 28 2011 Michal Ambroz <rebus at, seznam.cz> 0.05-1
- initial build for Fedora





