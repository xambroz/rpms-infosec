Name:           python-patator
Version:        0.9
Summary:        Patator is a multi-purpose brute-force tool
# Group needed for EPEL
Group:          Applications/System
License:        GPLv2
URL:            https://github.com/lanjelot/patator


# RPM Package release
%global         baserelease     1

# Git information
%global         gituser         lanjelot
%global         gitname         patator
# Current version
%global         gitdate         20171214
%global         commit          4d7ebf4334d09722e318307b0cb5aa25f9849a73
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Build with python3
%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 7 )
%global         with_python3    1
%endif

# Do not build the debug package
%global         debug_package   %{nil}

# Build source is tarball release=1 or git commit=0
%global         build_release    1


%if 0%{?build_release}  > 0
# Build from the targball release
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{gitname}-%{version}.tar.gz

%else
# Build from the git commit snapshot
# Not using the 0. on the beginning of release version as these are patches past version release
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{gitname}-%{version}-%{shortcommit}.tar.gz
%endif

Patch0:         patator-module.patch


BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif



%description
Patator is a multi-purpose brute-force tool written in Python.
It has modular design, flexible usage and supports multi-threading.
Patator strives to be more reliable and flexible than his fellow predecessors.



%package        -n python2-patator
# ======================= python2-patator =============================
Summary:        %{summary}
Group:          Applications/System
%{?python_provide:%python_provide python2-patator}

# Runtime dependencies
Requires:       python2-paramiko
Requires:       python2-pycurl
Requires:       python2-pysnmp
Requires:       python2-dns
Requires:       python2-psycopg2
Requires:       python2-mysql
Requires:       python2-pycryptodomex
Recommends:     python2-ajpy
Recommends:     python2-pysmi
#Recommends:     
#Recommends:     
#Recommends:     
#Recommends:     
#Recommends:     
#Recommends:     
#Recommends:     
#Recommends:     
#Recommends:     






%description    -n python2-patator
Patator is a multi-purpose brute-force tool written in Python.
It has modular design, flexible usage and supports multi-threading.
Patator strives to be more reliable and flexible than his fellow predecessors.


%if 0%{?with_python3}
%package        -n python%{python3_pkgversion}-patator
# ======================= python3-patator =============================
Summary:        %{summary}
Group:          Applications/System
%{?python_provide:%python_provide python%{python3_pkgversion}-patator}

Requires:       python%{python3_pkgversion}-paramiko
Requires:       python%{python3_pkgversion}-pycurl
Requires:       python%{python3_pkgversion}-pysnmp
Requires:       python%{python3_pkgversion}-dns
Requires:       python%{python3_pkgversion}-psycopg2
Requires:       python%{python3_pkgversion}-mysql
Requires:       python%{python3_pkgversion}-pycryptodomex
Recommends:     python%{python3_pkgversion}-ajpy
Recommends:     python%{python3_pkgversion}-pysmi



%description    -n python%{python3_pkgversion}-patator
Patator is a multi-purpose brute-force tool written in Python.
It has modular design, flexible usage and supports multi-threading.
Patator strives to be more reliable and flexible than his fellow predecessors.
#end with_python3
%endif



%prep
# ======================= prep =======================================


# Build from tarball release version
%if 0%{?build_release} > 0
%autosetup -p 1 -n %{gitname}-%{version} -S git

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit} -S git
%endif



%build
# ======================= build ======================================
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

%install
# ======================= install ====================================
%py2_install
sed -i -e 's|#!/usr/bin/env python2|#!/usr/bin/python2|' patator.py
mv %{buildroot}%{_bindir}/patator %{buildroot}%{_bindir}/patator2

%if 0%{?with_python3}
%py3_install
sed -i -e 's|#!/usr/bin/python.*|#!/usr/bin/python3|' patator.py
mv %{buildroot}%{_bindir}/patator %{buildroot}%{_bindir}/patator3
ln -s patator3 %{buildroot}%{_bindir}/patator
%else
ln -s patator2 %{buildroot}%{_bindir}/patator
%endif



%files -n python2-patator
# ======================= files ======================================
%doc README.md
%license LICENSE
%{_bindir}/patator2
%{python2_sitelib}/*


%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-patator
%doc README.md
%license LICENSE
%{_bindir}/patator
%{_bindir}/patator3
%{python3_sitelib}/*
%else
%{_bindir}/patator
%endif

%changelog
* Tue May 08 2018 Michal Ambroz <rebus AT, seznam.cz> - 0.7-1
- build for Fedora 28


