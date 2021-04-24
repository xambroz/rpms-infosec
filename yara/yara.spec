Name:           yara
Version:        4.0.5
Release:        1%{?dist}
Summary:        Pattern matching Swiss knife for malware researchers

# yara package itself is licensed as ASL 2.0
# bison grammar parsers in libyara/* are dual licensed under ASL 2.0 and GPLv3+ license.
# resulting binary package licensed as ASL 2.0
License:        ASL 2.0
#               http://github.com/VirusTotal/yara/releases
URL:            http://VirusTotal.github.io/yara/


%global         gituser         VirusTotal
%global         gitname         yara
# Commit of version 4.0.4
%global         commit          814b6296f4ce389c8c16b5508b56f1f3d9af554d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# additional module for yara
%global         androguard_gituser         Koodous
%global         androguard_gitname         androguard-yara
# Commit from 2020-04-22
%global         androguard_commit          3eea86ae2c4ee6ad3cc1cb3c2711b03db078831a
%global         androguard_shortcommit     %(c=%{androguard_commit}; echo ${c:0:7})
%global         androguard_gitdate         2020-04-22

# Build from git commit baseline
#Source0:       https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
# Build from git release version
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

#               http://github.com/Koodous/androguard-yara/
Source1:        https://github.com/%{androguard_gituser}/%{androguard_gitname}/archive/%{androguard_commit}/%{androguard_gitname}-%{androguard_gitdate}-%{androguard_shortcommit}.tar.gz

# Patch based on the androguard-yara installation guide to enable the androguard module
Patch0:         %{name}-androguard.patch

# Use default sphix theme to generate documentation rather than sphinx_rtd_theme
# to avoid static installation of font files on fedora >= 24
Patch1:         %{name}-docs-theme.patch

# Fixed in 3.6.0 upstream
# Patch https://patch-diff.githubusercontent.com/raw/VirusTotal/yara/pull/627.patch
# Fixes: CVE-2016-10210 CVE-2016-10211 CVE-2017-5923 CVE-2017-5924
# Patch2:         %%{name}-pull627.patch

# API of yr_re_match changed, fix needed for Androguard
# https://github.com/Koodous/androguard-yara/issues/8
# merged in https://github.com/Koodous/androguard-yara/commit/034f0a49e58d798abcaa28c9864451da9da29413
# Patch3: yara-androguard-matchapi.patch



BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  m4
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  sharutils
BuildRequires:  file
BuildRequires:  gawk
BuildRequires:  gzip
BuildRequires:  xz
BuildRequires:  pcre
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libtool
BuildRequires:  file-devel
BuildRequires:  jansson-devel >= 2.5
BuildRequires:  openssl-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  protobuf-compiler

# html doc generation
BuildRequires:  /usr/bin/sphinx-build

%description
YARA is a tool aimed at (but not limited to) helping malware researchers to
identify and classify malware samples. With YARA you can create descriptions
of malware families (or whatever you want to describe) based on textual or
binary patterns. Each description, a.k.a rule, consists of a set of strings
and a Boolean expression which determine its logic.


%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
This package contains documentation for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
# setup -qn %%{gitname}-%%{commit}
%setup -q

# Add the Androguard module
# %%setup -qn %%{gitname}-%%{commit} -a 1 -D -T
%setup -q -a 1 -D -T
pushd %{androguard_gitname}-%{androguard_commit}

# Patch yr_re_match api in androguard-yara
# https://github.com/Koodous/androguard-yara/issues/8
# %%patch3 -p 1 -b .matchapi

cp -p androguard.c ../libyara/modules/
popd
# Patch based on the androguard-yara installation guide to enable the androguard module
%patch0 -p 1 -b .androguard

# Use default sphix theme to generate documentation rather than sphinx_rtd_theme
# to avoid static installation of font files on fedora >= 24
%patch1 -p 1 -b .fonts


autoreconf --force --install


%build

# Add missing definition on RHEL7                                                                                                      
%if 0%{?rhel} && 0%{?rhel} == 7                                                                                                        
export CFLAGS="$CFLAGS -D PROTOBUF_C_FIELD_FLAG_ONEOF=4"                                                                               
%endif    

# macro %%configure already does use CFLAGS="\{optflags}" and yara build
# scripts configure/make already honors that CFLAGS
%configure --enable-magic --enable-cuckoo --enable-debug --enable-dotnet \
        --enable-macho --enable-dex --enable-pb-tests \
        --with-crypto \
        --htmldir=%{_datadir}/doc/%{name}/html
make %{?_smp_mflags}

# build the HTML documentation
pushd docs
make html
popd


%install
make install DESTDIR=%{buildroot}

# Remove static libraries
rm %{buildroot}%{_libdir}/lib%{name}.la
rm %{buildroot}%{_libdir}/lib%{name}.a

# Remove the rebuild-needed tag so it is not installed in doc pkg
rm -f %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo


%ldconfig_scriptlets


%files
%doc AUTHORS CONTRIBUTORS README.md
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}c.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%files doc
%license COPYING
%doc docs/_build/html


%changelog
* Fri Feb 5 2021 Michal Ambroz <rebus at, seznam.cz> - 4.0.5-1
- bump to yara bugfix 4.0.5 release

* Wed Feb 3 2021 Michal Ambroz <rebus at, seznam.cz> - 4.0.4-1
- bump to yara bugfix 4.0.4 release

* Thu Jul 16 2020 Michal Ambroz <rebus at, seznam.cz> - 4.0.2-1
- bump to yara bugfix 4.0.2 release
- fix build on epel7

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de> - 4.0.1-2
- Rebuilt for protobuf 3.12

* Tue Jun 2 2020 Michal Ambroz <rebus at, seznam.cz> - 4.0.1-1
- bump to yara bugfix 4.0.1 release

* Tue Apr 28 2020 Michal Ambroz <rebus at, seznam.cz> - 4.0.0-1
- bump to yara 4.0.0 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Michal Ambroz <rebus at, seznam.cz> - 3.11.0-1
- bump to 3.11.0 release (#1760678)
- BUGFIX: Some regexp character classes not matching correctly when used with “nocase” modifier (upstream #1117)
- BUGFIX: Reduce the number of ERROR_TOO_MANY_RE_FIBERS errors for certain hex pattern containing large jumps (upstream #1107)
- BUGFIX: Buffer overrun in “dotnet” module (upstream #1108)
- BUGFIX: Memory leak while attaching to a process fails (upstream #1070)

* Sat Sep 28 2019 Michal Ambroz <rebus at, seznam.cz> - 3.10.0-3
- change the sphinx build dependency

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 03 2019 Michal Ambroz <rebus at, seznam.cz> - 3.10.0-1
- bump to 3.10.0 release (#1680204)
- Harden virtual machine against malicious code.
- BUGFIX: Regression bug in hex strings containing wildcards (upstream #1025).
- BUGFIX: Buffer overrun in “elf” module.
- BUGFIX: Buffer overrun in “dotnet” module.

* Sat Mar 16 2019 Michal Ambroz <rebus at, seznam.cz> - 3.9.0-1
- bump to 3.9.0 release (#1680203)
- switch from python-sphinx to python3-sphinx for generating the documentation for fc31+
- should fix also #1660398 (CVE-2018-19974 CVE-2018-19975 CVE-2018-19976),
  but by design it might be always dangerous to run yara signatures compiled by 3rd party,
  so it is advised to re-compile yara rules instead
- BUGFIX: Denial of service when using "dex" module. Found by the Cisco Talos team. (upstream #1023, CVE-2019-5020)
- BUGFIX: Buffer overflow in "dotnet" module.
- BUGFIX: Regexp regression when using nested quantifiers {x,y} for certain values of x and y. (#1018)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Michal Ambroz <rebus at, seznam.cz> - 3.8.1-1
- bump to 3.8.1 release (#1613093)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Michal Ambroz <rebus at, seznam.cz> - 3.7.1-1
- bump to 3.7.1 release (#1534993)

* Wed Nov 15 2017 Michal Ambroz <rebus at, seznam.cz> - 3.7.0-1
- bump to 3.7.0 release (#1511921)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 16 2017 Michal Ambroz <rebus at, seznam.cz> - 3.6.3-1
- bump to 3.6.3 release - bugfix CVE-2017-11328

* Mon Jul 03 2017 Michal Ambroz <rebus at, seznam.cz> - 3.6.2-1
- bump to 3.6.2 release - bugfix CVE-2017-9304, CVE-2017-9465

* Wed May 24 2017 Michal Ambroz <rebus at, seznam.cz> - 3.6.0-1
- bump to 3.6.0 release
- update the androguard-yara with bugfixes

* Thu Apr 13 2017 Michal Ambroz <rebus at, seznam.cz> - 3.5.0-7
- Adding patch from pull request 627 until 3.5.1 is released
- https://patch-diff.githubusercontent.com/raw/VirusTotal/yara/pull/627.patch
- Fixes CVE-2016-10210 CVE-2016-10211 CVE-2017-5923 CVE-2017-5924

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 09 2016 Michal Ambroz <rebus at, seznam.cz> - 3.5.0-5
- import package to Fedora
- remove unnecessary .buildinfo tag from doc package

* Fri Aug 05 2016 Michal Ambroz <rebus at, seznam.cz> - 3.5.0-4
- package review - bugzilla #1362265
- cosmetics of the changelog
- using default spinx theme to remove the static fonts

* Fri Aug 05 2016 Michal Ambroz <rebus at, seznam.cz> - 3.5.0-3
- package review - bugzilla #1362265
- dropped Buildroot, pkgconfig, zlib-devel, defattr
- added buildrequires gcc
- change license back to ASL 2.0 only

* Thu Aug 04 2016 Michal Ambroz <rebus at, seznam.cz> - 3.5.0-2
- package review - bugzilla #1362265
- changed packaging of doc sub-package

* Thu Aug 04 2016 Michal Ambroz <rebus at, seznam.cz> - 3.5.0-1
- bump to new 3.5.0

* Wed Aug 03 2016 Michal Ambroz <rebus at, seznam.cz> - 3.4.0-6
- package review - bugzilla #1362265
- dropped dependency of python-tools

* Mon Aug 01 2016 Michal Ambroz <rebus at, seznam.cz> - 3.4.0-4
- compile with the androguard module

* Wed Jun 08 2016 Michal Ambroz <rebus at, seznam.cz> - 3.4.0-2
- jansson dependency >= 2.5

* Wed Jun 08 2016 Michal Ambroz <rebus at, seznam.cz> - 3.4.0-1
- python3 stuff

* Mon Jun 22 2015 Michal Ambroz <rebus at, seznam.cz> - 3.4.0-0.git20150618
- initial build for Fedora Project
