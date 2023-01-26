Name:           skipfish
Version:        2.10
Release:        0.23.b%{?dist}
Summary:        Web application security scanner


# Whole package licensed with ASL 2.0 license except 
# string-inl.h which has BSD type license
# icons which are licensed under LGPLv3
License:        ASL 2.0 and BSD and LGPLv3

URL:            http://code.google.com/p/skipfish/
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/skipfish/%{name}-%{version}b.tgz
# was:          http://%%{name}.googlecode.com/files/%%{name}-%%{version}b.tgz

# Use common paths and fedora build options and use fedora policy compiler flag
Patch01:         skipfish-01-makefile-format-security.patch

# Patch to build with GCC10 where -fno-common is the default
Patch02:         skipfish-02-gcc10.patch

# Patch from Kali linux
# https://gitlab.com/kalilinux/packages/skipfish/-/tree/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches

# From 21a6780ce8b5a17ffe2b17eda2abf5ca60fd6f46 Mon Sep 17 00:00:00 2001
# From: Igor Bezzubchenko <garikello@gmail.com>
# Date: Thu, 7 Jan 2021 14:21:32 +0300
# Subject: [PATCH] fixing broken ciphersuite evaluation for newer OpenSSLs
Patch3:         https://gitlab.com/kalilinux/packages/skipfish/-/raw/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches/Fix-broken-ciphersuite-evaluation-for-newer-OpenSSLs.patch#/skipfish-fix-broken-ciphersuite-evaluation-for-newer-OpenSSLs.patch

# From:         Igor Bezzubchenko <garikello@gmail.com>
# Date:         Sun, 3 Jan 2021 22:49:21 +0300
# Subject:      Fix for openssl 1.1
# Origin:       https://gitlab.com/kalilinux/packages/skipfish/-/merge_requests/1
Patch4:         https://gitlab.com/kalilinux/packages/skipfish/-/raw/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches/Fix-for-openssl-1.1.patch#/skipfish-fix-for-openssl-1.1.patch


# From: Sophie Brun <sophie@offensive-security.com>
# Date: Wed, 6 Jan 2021 15:31:58 +0100
# Subject: Fix small syntax issues in manpage
Patch5:         https://gitlab.com/kalilinux/packages/skipfish/-/raw/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches/Fix-small-syntax-issues-in-manpage.patch#/skipfish-fix-small-sytax-issues-in-manpage.patch



BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  libidn-devel
BuildRequires:  make
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel

%description
High-performance, easy, and sophisticated Web application security testing
tool. It features a single-threaded multiplexing HTTP stack, heuristic 
detection of obscure Web frameworks, and advanced, differential security
checks capable of detecting blind injection vulnerabilities, stored XSS,
and so forth.

%prep
%autosetup -p 1 -n %{name}-%{version}b
cp -p assets/COPYING COPYING.icons


%build
sed -i 's|^// #define PROXY_SUPPORT|#define PROXY_SUPPORT|' src/config.h
%make_build CFLAGS="%{optflags} -fno-common"



%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_datadir}/%{name}/assets/COPYING
rm -f doc/skipfish.1


%files
%doc COPYING ChangeLog README 
%doc doc/
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/assets
%dir %{_datadir}/%{name}/dictionaries
%dir %{_datadir}/%{name}/signatures
%{_datadir}/%{name}/dictionaries/*
%{_datadir}/%{name}/signatures/*
%{_datadir}/%{name}/assets/index.html
%{_bindir}/%{name}
%{_bindir}/sfscandiff
%{_mandir}/man1/%{name}.1*



#Icons are licensed as LGPLv3 http://www.everaldo.com/crystal/
%doc COPYING.icons
%{_datadir}/%{name}/assets/*.png


%changelog
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.23.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Apr 25 2020 Michal Ambroz <rebus AT seznam.cz> - 2.10-0.22.b
- fix FTBFS - build with -fno-common, which is now default for GCC10

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.21.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.20.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.19.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.18.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat May 12 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 2.10-0.17.b
- rebuilt

* Sun Feb 18 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 2.10-0.16.b
- Add gcc as BR (minimal buildroot change)
- Remove deprecated bits

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.15.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.14.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.13.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Gwyn Ciesla <limburgher@gmail.com> - 2.10-0.12.b
- Fix FTBFS by using compat-openssl10.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.11.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-0.10.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Athmane Madjoudj <athmane@fedoraproject.org>  2.10-0.9.b
- Enable proxy support

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-0.8.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-0.7.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-0.6.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb 23 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.10-0.5.b
- Fix bogus date

* Sun Dec 08 2013 Athmane Madjoudj <athmane@fedoraproject.org>  2.10-0.4.b
- Use -Werror=format-security flag (rhbz #1037329).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-0.3.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-0.2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 07 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.10-0.1.b
- Update to 2.10b

* Sun Sep 02 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.09-0.1.b
- Update to 2.09b

* Sun Sep 02 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.08-0.2.b
- Add pcre-devel as build requirement.

* Sun Sep 02 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.08-0.1.b
- Update to 2.08b
- Update the patch and spec file to the new upstream source structure.

* Wed Jun 20 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.07-0.1.b
- Update to 2.07b
- Add sfscandiff comparison tool

* Sun Apr 08 2012 Michal Ambroz <rebus AT seznam.cz> - 2.05-0.1.b
- rebuild for version 2.05b
- removed the default skipfish.wl as this version no longer an option
- addedd manpage

* Mon Oct 03 2011 Michal Ambroz <rebus AT seznam.cz> - 2.03-0.1.b
- rebuild for version 2.03b

* Sun Mar 27 2011 Michal Ambroz <rebus AT seznam.cz> - 1.85-0.1.b
- rebuild for version 1.85b

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.84-0.2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Michal Ambroz <rebus AT seznam.cz> - 1.84-0.1.b
- rebuild for version 1.84b

* Sun Aug 08 2010 Michal Ambroz <rebus AT seznam.cz> - 1.54-0.1.b
- rebuild for version 1.54b

* Sun May 09 2010 Michal Ambroz <rebus AT seznam.cz> - 1.34-0.1.b
- update to new version

* Wed Apr 28 2010 Michal Ambroz <rebus AT seznam.cz> - 1.32-0.4.b
- use fixed patch for memory allocation from Tomas Mraz <tmraz at redhat.doc>

* Tue Apr 27 2010 Michal Ambroz <rebus AT seznam.cz> - 1.32-0.3.b
- use new patch for memory allocation from Tomas Mraz <tmraz at redhat.doc>

* Fri Apr 23 2010 Michal Ambroz <rebus AT seznam.cz> - 1.32-0.2.b
- fix memory allocation to be compliant with FORTIFY_SOURCE

* Sun Apr 18 2010 Michal Ambroz <rebus AT seznam.cz> - 1.32-0.1.b
- Update to 1.32b
- merge back to 1 package on request of Tomas Mraz <tmraz AT redhat.com>

* Sun Apr 18 2010 Michal Ambroz <rebus AT seznam.cz> - 1.31-0.3.b
- return explicit dir to files

* Sun Apr 18 2010 Michal Ambroz <rebus AT seznam.cz> - 1.31-0.2.b
- Incorporated comments from  Martin Gieseking <martin.gieseking AT uos.de>

* Sat Apr 17 2010 Michal Ambroz <rebus AT seznam.cz> - 1.31-0.1.b
- Update to 1.31b

* Sat Apr 10 2010 Michal Ambroz <rebus AT seznam.cz> - 1.30-0.1.b
- Update to 1.30b

* Mon Mar 29 2010 Michal Ambroz <rebus AT seznam.cz> - 1.29-0.1.b
- Update to 1.29b

* Mon Mar 29 2010 Michal Ambroz <rebus AT seznam.cz> - 1.26-0.2.b
- removed attr from the spec
- separate icons package with LGPLv3 license

* Thu Mar 25 2010 Michal Ambroz <rebus AT seznam.cz> - 1.26-0.1.b
- Update to 1.26b
- Incorporated comments from  Martin Gieseking <martin.gieseking AT uos.de>

* Thu Mar 25 2010 Michal Ambroz <rebus AT seznam.cz> - 1.25b-1
- Update to 1.25b

* Tue Mar 23 2010 Michal Ambroz <rebus AT seznam.cz> - 1.16b-1
- Initial build for Fedora 12

