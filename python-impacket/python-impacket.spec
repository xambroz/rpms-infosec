Name:           python-impacket
Summary:        Collection of Python classes providing access to network packets
Version:        0.13.0

License:        Apache-1.1 AND Zlib
URL:            https://github.com/fortra/impacket
# was           https://github.com/SecureAuthCorp/impacket
# was           https://github.com/CoreSecurity/impacket
VCS:            git:%{url}

# During re-add of the python2-impacket we found about dependency to ldapdomaindump
# feature can be avoided by option --no-dump to ntlmrelay.py
# https://bugzilla.redhat.com/show_bug.cgi?id=1672052#c8
# Also exclude stuff from examples, recommended manually
%global __requires_exclude ldapdomaindump|flask|httplib2

%global         sum             Collection of Python classes providing access to network packets

%global         common_desc     %{expand:
Impacket is a collection of Python classes focused on providing access to
network packets. Impacket allows Python developers to craft and decode network
packets in simple and consistent manner. It is highly effective when used in
conjunction with a packet capture utility or package such as Pcapy. Packets
can be constructed from scratch, as well as parsed from raw data. Furthermore,
the object oriented API makes it simple to work with deep protocol hierarchies.}

# weak dependencies not needed for the core python impacket library
# used by example scripts
# dsinternals and ldapdomaindump
# - used by ntlmrelayx.py example - feature can be avoided by option --no-dump
# https://bugzilla.redhat.com/show_bug.cgi?id=1672052#c8
# Also exclude stuff from examples, recommended manually
%global __requires_exclude ldapdomaindump|flask|httplib2|dsinternals

%global         gituser         fortra
%global         gitname         impacket
%global         commit          d843881fb8464e9725a843ec4c8d6acdc6370ecf
%global         gitdate         20251022
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# By defualt build with python3
# To disable python3 subpackage do: rpmbuild --rebuild python-impacket.*.src.rpm --without python3
%bcond_without  python3

%global         pkgver          %(echo %{version} | sed 's/\\./_/g')

# By default build from the release tarball
# to build from git snapshot use rpmbuild --rebuild python-impacket.*.src.rpm --without release
%bcond_without  release

%if %{with release}
Release:        %autorelease
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/%{gitname}_%{pkgver}/%{gitname}-%{version}.tar.gz
%else
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

# https://github.com/fortra/impacket/pull/1689
# remove unnecessary shebang
Patch0:         python-impacket-0.12.0-cleanup.patch

# relax the strict requirement for version ==24.0.0
Patch1:         python-impacket-0.12.0-pyopenssl.patch

BuildArch:      noarch

BuildRequires:  sed
BuildRequires:  grep

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
%{common_desc}


#===== the python3 package definition
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
# Requires:       python%%{python3_pkgversion}-pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Requires:       python%{python3_pkgversion}-httplib2
Requires:       python%{python3_pkgversion}-flask
%endif


%description -n python%{python3_pkgversion}-%{gitname}
Python3 package of %{name}. %{common_desc}


#===== Preparation
%prep
%if %{with release}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}

# https://github.com/fortra/impacket/pull/1689
# 1) set library modules as non-executable as there is no main functionality and is meant to be used only via import
# impacket/examples/ldap_shell.py
# impacket/examples/smbclient.py
# 2) convert ends of lines from windows to unix (as rest of the project) for the file impacket/examples/mssqlshell.py
# 3) remove unnecessary shebang for impacket/examples/mssqlshell.py
chmod -x impacket/examples/ldap_shell.py impacket/examples/smbclient.py
sed -i -e 's/\r//g' impacket/examples/mssqlshell.py



%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif

# Clean-up

# Use explicit python3 shabeng instead of generic env python
%py3_shebang_fix impacket examples


# Rename split.py to splitpcap.py due to generic name colliding with DiderStevensSuite
# https://github.com/fortra/impacket/issues/1938
mv examples/split.py examples/splitpcap.py
sed -i -e "s%/split.py%/splitpcap.py%" impacket.egg-info/SOURCES.txt

# Drop useles dependency on future
# https://github.com/fortra/impacket/commit/d7b5e3 - will be fixed in 0.12.0
sed -i "s/'future',//" setup.py

#===== Build
%build
%py3_build


#===== Check
%check
PYTHONPATH=$BUILD_ROOT/usr/lib/python%{python3_version}/site-packages/ python3 -c \
    'import impacket.ImpactPacket ; impacket.ImpactPacket.IP().get_packet()'


#===== Install
%install
%py3_install

#now in license directory
rm -f %{buildroot}%{_defaultdocdir}/%{name}/LICENSE


#===== files for python3 package
%if %{with python3}
%files -n       python%{python3_pkgversion}-%{gitname}
%license        LICENSE
%doc            ChangeLog.md README.md
%{python3_sitelib}/%{gitname}/
%{python3_sitelib}/%{gitname}*.egg-info
%exclude %{_defaultdocdir}/%{gitname}
# %%exclude %%{_defaultdocdir}/%%{gitname}/testcases/*
%exclude %{_defaultdocdir}/%{gitname}/README.md
%{_bindir}/*.py
# with python3
%endif


%changelog
%autochangelog
