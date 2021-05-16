Name:           samdump2
Version:        3.0.0
Release:        20%{?dist}
Summary:        Retrieves syskey and extracts hashes from Windows 2k/NT/XP/Vista SAM

#MD5 RC4 DES functions are linked from openssl library
#Code of samdump2 is GPLv2+
License:        GPLv2+
URL:            http://sourceforge.net/projects/ophcrack/files/samdump2
Source0:        http://downloads.sourceforge.net/ophcrack/%{name}-%{version}.tar.bz2

Patch0:         %{name}-install.patch

# Patch from Debian to move from legacy openssl version to contemporary version
# Author: Joao Eriberto Mota Filho <eriberto@debian.org>
Patch1:         %{name}-openssl.patch

BuildRequires:  openssl-devel
BuildRequires:  make
BuildRequires:  gcc


%description
This tool is designed to recover the syskey bootkey from Windows NT/2K/XP/Vista
system hive and uses it to decrypt and dump password hashes from the SAM hive.


%prep
%autosetup


%build
make %{?_smp_mflags} CFLAGS="%{optflags}" LIBS="-lcrypto"


%install
rm -rf %{buildroot}

OWNER=`id -un`
GROUP=`id -gn`

make install DESTDIR=%{buildroot} BINDIR=%{_bindir} MANDIR=%{_mandir}/man1/ OWNER=${OWNER} GROUP=${GROUP}


%files
%doc AUTHORS COPYING README LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Feb 17 2021 Michal Ambroz <rebus AT seznam.cz> - 3.0.0-20
- use Debian patch to switch to the current version of openssl for crypto
- adding dependencies to make and gcc

* Thu Aug 06 2020 Jeff Law <law@redhat.com> - 3.0.0-19
- Add gcc as build requirement

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-18
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

-* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-17
-- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

-* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-16
-- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 17 2017 Michal Ambroz <rebus AT seznam.cz> - 3.0.0-10
- fix FTBFS due to openssl change by linking to the compat lib for Fedora 26

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 27 2012 Michal Ambroz <rebus AT seznam.cz> - 3.0.0-1
- initial build for Fedora 17

