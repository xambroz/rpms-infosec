Name:           openvas-libraries
Version:        11.0.1
Release:        4%{?dist}
Summary:        Support libraries for Greenbone Vulnerability Management Solution and OpenVAS

License:        GPLv2+
URL:            http://www.openvas.org
#               https://github.com/greenbone/gvm-libs/releases

Source0:        https://github.com/greenbone/gvm-libs/archive/v%{version}.tar.gz#/gvm-libs-%{version}.tar.gz
Source1:        https://github.com/greenbone/gvm-libs/releases/download/v%{version}/gvm-libs-%{version}.tar.gz.asc

# The authenticator public key obtained from release 11.0.0
# gpg2 -vv gvm-libs-11.0.1.tar.gz.asc
# gpg2 --search-key 9823FAA60ED1E580
# wget https://www.greenbone.net/GBCommunitySigningKey.asc
# gpg2 --import GBCommunitySigningKey.asc
# gpg2 --list-public-keys 9823FAA60ED1E580
# gpg2 --export --export-options export-minimal 8AE4BE429B60A59B311C2E739823FAA60ED1E580 > gpgkey-8AE4BE429B60A59B311C2E739823FAA60ED1E580.gpg
Source3:        gpgkey-8AE4BE429B60A59B311C2E739823FAA60ED1E580.gpg

Patch0:         openvas-libraries-strncpy.patch

Obsoletes:      openvas-libnasl
#Obsoletes:     openvas-libraries <= 9.0.3
#Provides:      libgvm = %{version}-%{release}

BuildRequires: make
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glib2-devel
BuildRequires:  gnutls-devel
BuildRequires:  gpgme-devel
BuildRequires:  graphviz
BuildRequires:  hiredis-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libksba-devel
BuildRequires:  libpcap-devel
BuildRequires:  libssh-devel
BuildRequires:  libuuid-devel
BuildRequires:  libxml2-devel
BuildRequires:  net-snmp-devel
BuildRequires:  openldap-devel
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel


%description
Library modules for the Greenbone Vulnerability Management Solution/OpenVAS
network security scanner.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development libraries and headers for use with %{name}.

%package doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

%description doc
The documentation of %{name}.

%prep
#check signature
gpgv2 --keyring %{SOURCE3} %{SOURCE1} %{SOURCE0}


%autosetup -n gvm-libs-%{version} -p1

%build
# In GCC7 format-truncation throws bogus errors when formating time/date
export CFLAGS="%{optflags} -Wno-format-truncation"
# Disable warnings -> error for stringop-truncation for now
export CFLAGS="${CFLAGS} -Wno-error=stringop-truncation"
%cmake -DLOCALSTATEDIR:PATH=%{_var} -DBUILD_WITH_LDAP=ON .
# No parallel build because it causes compilation problems
%make_build
make doc-full

%install
%make_install
# Remove static libraries
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%ldconfig_scriptlets

%files
%doc CHANGELOG.md README.md
%license COPYING
%{_libdir}/libgvm*.so.*

%files devel
%license COPYING
%{_includedir}/gvm/
%{_libdir}/libgvm_*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc doc/generated/html

%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 josef radinger <cheese@nosuchhost.net> - 11.0.1-1
- bump version
- fix path to Source1
- add Buildrequires on libxml2-devel

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 11.0.0-2
- Change misguided strncpy calls into strcpy calls to avoid (proper)
  gcc diagnostic about length of strncpy call being the same as the
  source string length

* Tue Oct 15 2019 Michal Ambroz <rebus at, seznam.cz> - 11.0.0-1
- bump to gvm-libs version 11.0.0
- put back the signature checking

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Fabian Affolter <mail@fabian-affolter.ch> - 10.0.0-1
- Update to latest upstream release 10.0.0
- Prepare for renaming, update %%files sections and remove patches
- Simplify the spec file (as it will require a re-review)

* Tue Feb 26 2019 josef radinger <cheese@nosuchhost.net> - 9.0.3-6
- make doc-full
- better description for doc-sub-package

* Sun Feb 3 2019 josef radinger <cheese@nosuchhost.net> - 9.0.3-5
- add BuildRequires on graphviz

* Sat Feb 2 2019 josef radinger <cheese@nosuchhost.net> - 9.0.3-4
- enable net-snmp-devel
- add openvas-libraries-snmp.patch (snmp -> netsnmp)
- add openvas-libraries-gcc-warnings.patch to silence compiler warning
- small reordering in spec-file
- add openvas-libraries-buffer.patch
- disable stringop-truncation on fedora >= 30

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 9.0.3-2
- Append curdir to CMake invokation. (#1668512)

* Sat Jan 12 2019 josef radinger <cheese@nosuchhost.net> - 9.0.3-1
- bump version
- cleanup spec-file
- use -delete instead of -exec rm in find

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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
