Name:           bkhive
Version:        1.1.1
Release:        21%{?dist}
#Needed for EPEL
Summary:        Dump the syskey bootkey from a Windows system hive

License:        GPLv2+
URL:            http://ophcrack.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ophcrack/%{name}-%{version}.tar.gz

#Patch adds possibility to install with current user and not only root
Patch0:         %{name}-install.patch

BuildRequires:  gcc
BuildRequires: make

%description
This tool is designed to recover the syskey bootkey from a Windows NT/2K/XP
system hive. Then we can decrypt the SAM file with the syskey and dump
password hashes.

Syskey is a Windows feature that adds an additional encryption layer to the
password hashes stored in the SAM database.

%prep
%setup -q
%patch0 -p 1 -b .install


%build
make %{?_smp_mflags} CFLAGS="%{optflags}"


%install
rm -rf %{buildroot}
OWNER=`id -un`
GROUP=`id -gn`

make install DESTDIR=%{buildroot} BINDIR=%{_bindir} MANDIR=%{_mandir}/man1/ OWNER=${OWNER} GROUP=${GROUP}


%files
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*



%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-20
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 7 2012 Michal Ambroz <rebus AT seznam.cz> - 1.1.1-4
- Added Group tag, which is mandatory for EPEL5

* Sat Aug 4 2012 Michal Ambroz <rebus AT seznam.cz> - 1.1.1-3
- source for EL5 got somehow stucked, trying to bump revision

* Mon Jun 25 2012 Michal Ambroz <rebus AT seznam.cz> - 1.1.1-2
- fix license - GPLv2+

* Sun May 27 2012 Michal Ambroz <rebus AT seznam.cz> - 1.1.1-1
- initial build for Fedora 17
