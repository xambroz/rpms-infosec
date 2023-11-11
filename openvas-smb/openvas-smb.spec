Name:           openvas-smb
Summary:        SMB module for the OpenVAS Scanner
URL:            http://www.openvas.org
#               http://www.openvas.org/install-source.html
#               https://github.com/greenbone/openvas-smb/releases
License:        LGPLv2
Group:          System Environment/Libraries
Version:        1.0.3

%global         gituser         greenbone
%global         gitname         openvas-smb
%global         gitdate         20180326
%global         commit          4a198b84f47023aa0fc009e53de461b0e87df3bc
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/%{gituser}/%{gitname}/releases/download/v%{version}/%{name}-%{version}.tar.gz.sig

# The authenticator public key obtained from release 9.0.2
# gpg2 -vv openvas-libraries-9.0.2.tar.gz.sig
# gpg2 --search-key 48479FF648DB4530
# gpg2 --export --export-options export-minimal C3B468D2288C68B9D526452248479FF648DB4530 > gpgkey-C3B468D2288C68B9D526452248479FF648DB4530.gpg
Source3:        gpgkey-C3B468D2288C68B9D526452248479FF648DB4530.gpg

BuildRequires:  cmake >= 2.6.0
BuildRequires:  perl-interpreter
BuildRequires:  git
BuildRequires:  heimdal-devel >= 1.6.0
BuildRequires:  pkgconfig
BuildRequires:  gnutls-devel >= 2.12.10
BuildRequires:  popt-devel
BuildRequires:  glib2-devel

BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc



%description
openvas-libraries is the base library for the OpenVAS network
security scanner.


%package devel
Summary:        Development files for openvas-libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development libraries and headers for use with %{name}.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
# check the validity of GPG signature
gpgv2 --keyring %{SOURCE3} %{SOURCE1} %{SOURCE0}

%autosetup -p 1 -n %{gitname}-%{version}



%build
# -Wno-format-truncation:
# in GCC7 format-truncation throws bogus errors when formating time/date
export CFLAGS="%{optflags} -Wno-format-truncation"

%cmake -DLOCALSTATEDIR:PATH=%{_var} -DBUILD_WITH_LDAP=ON
# No parallel build because it causes compilation problems
make
make doc

%install
rm -rf %{buildroot}
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Remove static libraries
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# Currently I don't know for what is this used so I removing it
rm -f %{buildroot}/%{_datadir}/openvas/openvas-lsc-rpm-creator.sh

#Install openvas-check-setup
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/

%ldconfig_scriptlets


%files
%defattr(-,root,root,-)
%doc README COPYING* ChangeLog CHANGES
%dir %{_datadir}/openvas
%dir %{_sysconfdir}/openvas
%{_bindir}/openvas-nasl
%{_bindir}/openvas-nasl-lint
%{_bindir}/openvas-check-setup
%{_mandir}/man1/openvas-nasl.1*
%{_mandir}/man1/openvas-nasl-lint.1*
%{_libdir}/libopenvas_base.so.*
#%{_libdir}/libopenvas_hg.so.*
%{_libdir}/libopenvas_misc.so.*
%{_libdir}/libopenvas_nasl.so.*
%{_libdir}/libopenvas_omp.so.*
#%{_datadir}/openvas/openvas-services
%{_libdir}/libopenvas_osp.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/openvas/
%{_libdir}/libopenvas_base.so
#%{_libdir}/libopenvas_hg.so
%{_libdir}/libopenvas_misc.so
%{_libdir}/libopenvas_nasl.so
%{_libdir}/libopenvas_omp.so
%{_libdir}/libopenvas_osp.so
%{_libdir}/pkgconfig/libopenvas_base.pc
%{_libdir}/pkgconfig/libopenvas_omp.pc
%{_libdir}/pkgconfig/libopenvas_nasl.pc
%{_libdir}/pkgconfig/libopenvas_misc.pc
%{_libdir}/pkgconfig/libopenvas_osp.pc


%files doc
%doc doc/generated/html
%doc doc/test_ipv6_packet_forgery.nasl


%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 9.0.2-2
- switch to the github release file
- add signature checking

* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 9.0.2-1
- bump to OpenVas-9 version 9.0.2

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 17 2017 Michal Ambroz <rebus at, seznam.cz> - 9.0.1-1
- bump to OpenVas-9 version 9.0.1
- fix gcc7 fallthrough
- ignore format-truncation warnings 

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.0.8-3
- Rebuild for gpgme 1.18

* Mon Sep 05 2016 Michal Ambroz <rebus at, seznam.cz> - 8.0.8-1
- bump to OpenVas-8 version 8.0.8

* Sat Feb 27 2016 josef radinger <cheese@nosuchhost.net> - 8.0.7-2
- sync spec-files across fedora versions

* Sat Feb 27 2016 josef radinger <cheese@nosuchhost.net> - 8.0.7-1
- use -Wno-unused-const-variable
- use -Wno-error=misleading-indentation
- bump version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 23 2015 josef radinger <cheese@nosuchhost.net> - 8.0.6-1
- bump version

* Tue Sep 29 2015 josef radinger <cheese@nosuchhost.net> - 8.0.5-1
- bump version

* Fri Sep 11 2015 josef radinger <cheese@nosuchhost.net> - 8.0.4-2
- rebuild

* Wed Jul 15 2015 Michal Ambroz <rebus at, seznam.cz> - 8.0.4-1
- bump to OpenVas-8 version 8.0.4

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Michal Ambroz <rebus at, seznam.cz> - 8.0.3-1
- bump to OpenVas-8 version 8.0.3

* Sat Apr 04 2015 Michal Ambroz <rebus at, seznam.cz> - 7.0.9-1
- bump to OpenVas-7 version 7.0.9

* Sat Dec 06 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.6-1
- bump to OpenVas-7 version 7.0.6

* Tue Nov 04 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.5-1
- bump to OpenVas-7 version 7.0.5

* Fri Sep 12 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.4-1
- bump to OpenVas-7 version 7.0.4

* Tue Sep 02 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.3-2
- clean-up patches

* Tue Sep 02 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.3-1
- bump to OpenVas-7 version 7.0.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.2-2
- bump to OpenVas-7 version 7.0.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Michal Ambroz <rebus at, seznam.cz> - 7.0.1-1
- bump to OpenVas-7 version 7.0.1

* Thu Apr 24 2014 Tomáš Mráz <tmraz@redhat.com> - 6.0-5.beta5
- Rebuild for new libgcrypt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-4.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Michal Ambroz <rebus at, seznam.cz> - 6.0-3.beta5
- update to 6.0 beta5 upstream release

* Thu Mar 07 2013 Tomáš Mráz <tmraz@redhat.com> - 6.0-2.beta3
- rebuilt with new GnuTLS

* Sat Feb 09 2013 Michal Ambroz <rebus at, seznam.cz> - 6.0-1.beta3
- fix wrong size to memset

* Wed Feb 06 2013 Michal Ambroz <rebus at, seznam.cz> - 6.0-0.beta3
- bump to OpenVas-6 version 6.0+beta3

* Thu Nov 15 2012 Michal Ambroz <rebus at, seznam.cz> - 5.0.4-1
- bump to OpenVas-5 version 5.0.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Michal Ambroz <rebus at, seznam.cz> - 4.0.7-1
- adding openvas-check-setup based on suggestion of Reindl Harald
- bump to version 4.0.7

* Tue Jan 24 2012 Michal Ambroz <rebus at, seznam.cz> - 4.0.6-4
- separate documentation package, build with ldap support

* Sun Jan 15 2012 Michal Ambroz <rebus at, seznam.cz> - 4.0.6-3
- removed pach openvas-libraries-4.0.6-key.patch again as gnutls will be
  upgraded to 2.2.14 in Fedora 16 soon

* Mon Jan 09 2012 Michal Ambroz <rebus at, seznam.cz> - 4.0.6-2
- added openvas-libraries-4.0.6-key.patch to fix use-after-free issue causing
  SIGSEGV fault in gnutls code

* Fri Nov 04 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.6-1
- bump to version 4.0.6

* Tue Oct 18 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.5-5
- revert back to code withou gnutls modifications to confirm gnutls
issues are not caused by it
- disabling the -Werror to avoid compilation issues with the deprecated gnutls code

* Thu Oct 06 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.5-4
- fix the priorities string

* Sat Jul 30 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.5-3
- gnutls > 2.12.0 has deprecated gnutls_transport_set_lowat

* Sun Jul 3 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.5-2
- change from deprecated gnutls_*_set_priority to gnutls_priority_set_direct

* Fri Jun 10 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.5-1
- bump to 4.0.5

* Fri May 06 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.4-1
- bump to 4.0.4

* Tue Mar 22 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.3-2
- patch not used

* Fri Mar 18 2011 Michal Ambroz <rebus at, seznam.cz> - 4.0.3-1
- Bump to latest stable release 4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Stjepan Gros <stjepan.gros@gmail.com> - 3.1.4-1
- Bump to latest stable release
- Added libuuid-devel build time dependency

* Mon Apr 5 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 3.0.3-3
- Obsolete openvas-libnasl

* Wed Mar 3 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 3.0.3-2
- Correct license to LGPLv2

* Mon Mar 1 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 3.0.3-1
- Upgraded to a new upstream version
- Spec from Stjepan Gros

* Thu Nov 26 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 2.0.4-3
- Update to 2.0.4.
- Fix %%setup invocation.
- Add BR: glib2-devel.
- Version bump so that it builds

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.0-2-2
- More changes to the spec

* Tue Sep 9 2008 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.0.2-1
- Built on newer upstream version
- Minor spec changes

* Tue Sep 9 2008 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.0.1-1
- Inital Fedora version

* Tue Apr 15 2008 Jan-Oliver Wagner <jan-oliver.wagner@intevation.de>
  Initial SUSE 10.2 spec file, tested for i586
