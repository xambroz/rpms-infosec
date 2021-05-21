Name:           python-impacket
Version:        0.9.22
%global         baserelease     4

License:        ASL 1.1 and zlib
URL:            https://github.com/SecureAuthCorp/impacket
# was           https://github.com/CoreSecurity/impacket

# During re-add of the python2-impacket we found about dependency to ldapdomaindump
# feature can be avoided by option --no-dump to ntlmrelay.py
# https://bugzilla.redhat.com/show_bug.cgi?id=1672052#c8
# Also exclude stuff from examples, recommended manually
%global __requires_exclude ldapdomaindump|flask|httplib2


%global         common_desc     %{expand:
Impacket is a collection of Python classes focused on providing access to
network packets. Impacket allows Python developers to craft and decode network
packets in simple and consistent manner. It is highly effective when used in
conjunction with a packet capture utility or package such as Pcapy. Packets
can be constructed from scratch, as well as parsed from raw data. Furthermore,
the object oriented API makes it simple to work with deep protocol hierarchies.}


%global         gituser         SecureAuthCorp
%global         gitname         impacket
%global         commit          2438fb66cea4c6a9b4a04939e1ef9c4208d60134
%global         gitdate         20201123
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         sum             Collection of Python classes providing access to network packets


# By defualt build with python3
# To disable python3 subpackage do: rpmbuild --rebuild python-impacket.*.src.rpm --without python3
%bcond_without  python3


# By default the package is not build with support of python2
# But the project still supports the execution in python2 or python3
# To build with python2 support do:
# rpmbuild --rebuild python-impacket.*.src.rpm --with python2
%bcond_with     python2
# Build also the python2 package when rebuilding on older releases
%if %{with python2} || (0%{?fedora} && 0%{?fedora} <= 31 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
%global         with_python2    1
%endif


%global         pkgver          %(echo %{version} | sed 's/\\./_/g')

# By default build from the release tarball
# to build from git snapshot use rpmbuild --rebuild python-impacket.*.src.rpm --without release
%bcond_without  release

%if %{with release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/%{gitname}_%{pkgver}/%{gitname}-%{version}.tar.gz
%else
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif


Summary:        %{sum}

# Fedora specific fixing:
# ldap3 version - we need 2.8.1 as minimum (20210501), but tested to work with 2.5.1 (previous version EL7)
# win32 - we do not want package to advertise for libraries needed on win32
# python3.9 - allow build on python3.9 neede for >= fc34
Patch0:         python-impacket-setup.patch

# Build with python3.9 - needed on >= FC34
# reported to upstream https://github.com/SecureAuthCorp/impacket/issues/1032
Patch1:         https://patch-diff.githubusercontent.com/raw/SecureAuthCorp/impacket/pull/1054.patch#/python-impacket-python39.patch

# Fix CVE-2021-31800 - 1957428, 1957427 during 0.9.22 lifecycle
# fix path traversal in smbserver.py
Patch2:         https://github.com/SecureAuthCorp/impacket/commit/49c643bf66620646884ed141c94e5fdd85bcdd2f.patch#/python-impacket-CVE-2021-31800.patch


BuildArch:      noarch

BuildRequires:  sed
BuildRequires:  grep

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif


%description
%{common_desc}

#===== the python2 package definition
%if %{with python2}
%package -n python2-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{gitname}}
Provides:       impacket = %{version}-%{release}

# Used by many
Requires:       python2-pycryptodomex

# Used by /usr/bin/psexec.py
Requires:       python2-pyasn1

# On Fedora and RHEL8 we can use "Recommends" clause for non-essential stuff
%if 0%{?fedora} || 0%{?rhel} >= 8
# Used by /usr/bin/nsplit.py
Requires:       python2-pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Recommends:     python2-httplib2
Recommends:     python2-flask
# Used by /usr/bin/ntlmrelayx.py
Recommends:     python2-pyOpenSSL
Requires:       python2-ldap3

%else
# OnRHEL7 there is no Recommends clause so we need to handle it here
# Used by /usr/bin/nsplit.py
Requires:       pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Requires:       python2-httplib2
# Recommends:   python2-flask     - package not available any pore on EPEL7
# Used by /usr/bin/ntlmrelayx.py
# Recommends:   python2-pyOpenSSL - package not available any more on EPEL7
Requires:       python2-ldap3

# #1900077 - https://bugzilla.redhat.com/show_bug.cgi?id=1900077
# pytho2 packages for Flask and pyOpenSSL not available on RHEL7
# Functionality not needed for majority of use-cases.
# Missing libraries can still be installed from pip or Centos if needed
%global __requires_exclude                     ^python2-pyOpenSSL
%global __requires_exclude %__requires_exclude|^python2-flask
%endif


%description -n python2-%{gitname}
Python2 package of %{name}. %{common_desc}

# with python2
%endif


#===== the python3 package definition
%if %{with python3}
%package -n python%{python3_pkgversion}-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}
Provides:       impacket = %{version}-%{release}

# Used by many
Requires:       python%{python3_pkgversion}-pycryptodomex

# Used by /usr/bin/psexec.py
Requires:       python%{python3_pkgversion}-pyasn1

# Used by /usr/bin/ntlmrelayx.py
Requires:       python%{python3_pkgversion}-pyOpenSSL
Requires:       python%{python3_pkgversion}-ldap3

%if 0%{?fedora} || 0%{?rhel} >= 8
# Used by /usr/bin/nsplit.py
Recommends:     python%{python3_pkgversion}-pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Recommends:     python%{python3_pkgversion}-httplib2
Recommends:     python%{python3_pkgversion}-flask
%else
# python3 package for pcapy currently missing in EPEL7
# Used by /usr/bin/nsplit.py
%global __requires_exclude pcapy|ldapdomaindump|flask|httplib2
# Requires:       python%{python3_pkgversion}-pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Requires:       python%{python3_pkgversion}-httplib2
Requires:       python%{python3_pkgversion}-flask
%endif


%description -n python%{python3_pkgversion}-%{gitname}
Python3 package of %{name}. %{common_desc}
 # with_python3
%endif



#===== Preparation
%prep
%if %{with release}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif

# Clean-up

# Use explicit python3 shabeng instead of generic env python
# to get prepared for switch the default to python3
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python3|' \
    impacket/mqtt.py \
    impacket/examples/ntlmrelayx/servers/socksserver.py

# Moving uncrc32
# https://github.com/SecureAuthCorp/impacket/issues/403
sed -i -e 's|^import uncrc32|from impacket.examples import uncrc32|;' examples/nmapAnswerMachine.py



#===== Build
%build
%if %{with python2}
%py2_build
%endif

%if %{with python3}
%py3_build
%endif


#===== Check
%check
%if %{with python2}
PYTHONPATH=$BUILD_ROOT/usr/lib/python%{python2_version}/site-packages/ python2 -c \
    'import impacket.ImpactPacket ; impacket.ImpactPacket.IP().get_packet()'
%endif
%if %{with python3}
PYTHONPATH=$BUILD_ROOT/usr/lib/python%{python3_version}/site-packages/ python3 -c \
    'import impacket.ImpactPacket ; impacket.ImpactPacket.IP().get_packet()'
%endif



#===== Install
%install
%if %{with python2}
%py2_install
pushd %{buildroot}%{_bindir}
for I in *.py ; do
    BASENAME=$(basename "$I" .py)
    mv "$I" "${BASENAME}-%{python2_version}"
    ln -s "${BASENAME}-%{python2_version}" "${BASENAME}-2"

done
popd
%endif

%if %{with python3}
%py3_install
pushd %{buildroot}%{_bindir}
for I in *.py ; do
    BASENAME=$(basename "$I" .py)
    mv "$I" "${BASENAME}-%{python3_version}"
    ln -s "${BASENAME}-%{python3_version}" "${BASENAME}-3"
done
popd
%endif

# Default link
pushd %{buildroot}%{_bindir}

%if (0%{?fedora} && 0%{?fedora} <= 30 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
    #Link to python2 as default on fedora up to 30 and rhel up to 7
    for I in *-2 ; do
        BASENAME=$(basename "$I" "-2" )
        ln -s "${I}" "${BASENAME}.py"
    done
%else
    #Link to python3 as default on fedora 31+ and rhel8+ and everything else
    for I in *-3 ; do
        BASENAME=$(basename "$I" "-3" )
        ln -s "${I}" "${BASENAME}.py"
    done
%endif
popd

#now in license directory
rm -f %{buildroot}%{_defaultdocdir}/%{name}/LICENSE



#===== files for python2 package
%if %{with python2}
%files -n       python2-%{gitname}
%license        LICENSE
%doc            ChangeLog README.md
%{python2_sitelib}/%{gitname}/
%{python2_sitelib}/%{gitname}*.egg-info
%exclude %{_defaultdocdir}/%{gitname}
# %%exclude %%{_defaultdocdir}/%%{gitname}/testcases/*
%exclude %{_defaultdocdir}/%{gitname}/README.md
%{_bindir}/*-%{python2_version}
%{_bindir}/*-2
%if (0%{?fedora} && 0%{?fedora} <= 30 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
%{_bindir}/*.py
%endif
# with python2
%endif



#===== files for python3 package
%if %{with python3}
%files -n       python%{python3_pkgversion}-%{gitname}
%license        LICENSE
%doc            ChangeLog README.md
%{python3_sitelib}/%{gitname}/
%{python3_sitelib}/%{gitname}*.egg-info
%exclude %{_defaultdocdir}/%{gitname}
# %%exclude %%{_defaultdocdir}/%%{gitname}/testcases/*
%exclude %{_defaultdocdir}/%{gitname}/README.md
%{_bindir}/*-%{python3_version}
%{_bindir}/*-3
%if (0%{?fedora} && 0%{?fedora} >= 31 ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
%{_bindir}/*.py
%endif
# with python3
%endif


%changelog
* Fri May 21 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-4
- remove the dependency to python-crypto

* Fri May 07 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-3
- fix CVE-2021-31800 - #1957428, #1957427 during 0.9.22 lifecycle

* Sun May 02 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-2
- fix dependencies for EPEL7 as of #1893859

* Wed Apr 14 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-1
- Updated to new upstream release 0.9.22
- modernize specfile with bconds
- upstream patch for python39 compatibility (needed for FC34+)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.21-6
- Rebuilt for Python 3.9

* Tue Apr 28 2020 Michal Ambroz <rebus _AT seznam.cz> - 0.9.21-5
- fix dependency - pcapy renamed to python2-pcapy, python3-pcapy in fedora

* Tue Apr 28 2020 Michal Ambroz <rebus _AT seznam.cz> - 0.9.21-4
- cosmetics, remove comments with endif, macros with comments

* Thu Apr 02 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.21-3
- Updated to new upstream release 0.9.21

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.20-2
- patch the ldap3 dependencies to allow >=2.5.1 as we have already
  2.6 in Fedora 30 with updates. Dependency is used only for
  ntlmrelayx example and right now missing the ldapdump dependency
  anyway

* Sat Oct 12 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.20-1
- bump to version 0.9.20
- generate python3 packages, preference goes to python3
- omit python2 for fc32+ rhel8+

* Tue Sep 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.19-2
- Only recommend packages needed for examples

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.19-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.19-1
- bump to version 0.9.19

* Tue Feb 05 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.18-3
- conditional dependencies for EPEL7 - python-flask and pyOpenSSL

* Mon Feb 04 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.18-2
- add missing dependencies for EPEL7 - python2-setuptools
- patch setup.py to remove python_version to meet RHEL7 setuptools version

* Mon Feb 04 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.18-1
- bump to version 0.9.18 

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.17-0.4.20180308gite0af5bb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.17-0.3.20180308gite0af5bb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Michal Ambroz <rebus _AT seznam.cz> - 0.9.17-0.2
- fix python runtime dependencies #1506227

* Sun Mar 11 2018 Michal Ambroz <rebus _AT seznam.cz> - 0.9.17-0.1
- bump to development version of 0.9.17 as there won't be any 0.9.16

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 12 2016 Michal Ambroz <rebus _AT seznam.cz> - 0.9.15-4
- fix python provides for the python-impacket

* Wed Aug 24 2016 Michal Ambroz <rebus _AT seznam.cz> - 0.9.15-3
- python2/3 split package, disable python3 subpackage by default
- fix FTBFS

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 14 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.15-1
- Update to latest upstream release (rhb#1307918)

* Tue Mar 01 2016 Michal Ambroz <rebus _AT seznam.cz> - 0.9.14-1
- Updated to new upstream release 0.9.14
- as Impacket upstream is not ready for python3 I propose to have the py3
  building ready, but disabled by default

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.13-2
- Cleanup and py3

* Wed Jul 22 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.13-1
- Updated to new upstream release 0.9.13
- Fix FTBS (rhbz#1239842)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.12-1
- Updated to new upstream release 0.9.12

* Sat Jun 28 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.11-2
- Move files out of /usr/bin
- Update licence (according to mailing list)

* Wed Feb 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.11-1
- Updated to new upstream release 0.9.11

* Sat Aug 10 2013 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.10-1
- Updated to new upstream release 0.9.10

* Sat Nov 17 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.9.9-1
- Initial package

