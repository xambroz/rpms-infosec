Name:           python-pwntools
Version:        4.14.1
Release:        %autorelease
Summary:        A CTF framework and exploit development library
URL:            https://github.com/Gallopsled/pwntools/
VCS:            git:https://github.com/Gallopsled/pwntools/

# ./LICENSE-pwntools.txt - base project of pwntools is licensed as MIT
# ./pwnlib/data/includes/LICENSE.txt
#    - header files from FreeBSD licensed with BSD 2-clause license
#    - header files from dietlibc licensed with GPLv2 or later
# ./pwnlib/data/useragents/LICENSE.txt - script `download-useragents.py licensed with BSD 2-clause license
License:        MIT AND BSD-2-Clause AND GPL-2.0-or-later

%global         srcname pwntools


# Source0:      %%{url}/archive/%%{srcname}-%%{version}.tar.gz
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

# Unicorn package currently doesn't build on s390x platform, but it is used ony for resolving plt.
# Other functionality of pwntools should be still working
# https://github.com/Gallopsled/pwntools/pull/2568/
Patch1:         python-pwntools-4.14.1-weak-unicorn.patch


BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# Waiting on pwntools to support newer sphinx shipped by Fedora.
# BuildRequires:  python%%{python3_pkgversion}-sphinx

# Build requirements for %%check
BuildRequires:  python%{python3_pkgversion}-capstone
BuildRequires:  python%{python3_pkgversion}-mako
BuildRequires:  python%{python3_pkgversion}-packaging
BuildRequires:  python%{python3_pkgversion}-paramiko
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-psutil
BuildRequires:  python%{python3_pkgversion}-pyelftools
BuildRequires:  python%{python3_pkgversion}-pygments
BuildRequires:  python%{python3_pkgversion}-pyserial
BuildRequires:  python%{python3_pkgversion}-pysocks
BuildRequires:  python%{python3_pkgversion}-dateutil
BuildRequires:  python%{python3_pkgversion}-requests
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-sortedcontainers
BuildRequires:  python%{python3_pkgversion}-wheel

# some packages missing on EPEL
%if (0%{?fedora})
BuildRequires:  python%{python3_pkgversion}-intervaltree
BuildRequires:  python%{python3_pkgversion}-colored-traceback
BuildRequires:  python%{python3_pkgversion}-ROPGadget
BuildRequires:  python%{python3_pkgversion}-rpyc

# Omiting the unicorn on purpose for now as it creates unwanted src.rpm build dependency on s390x for some reason
# %%ifnarch s390x s390
# BuildRequires:  python%%{python3_pkgversion}-unicorn
# %%endif
%endif



# Unicorn python3 module currently not available on s390x architecture F39/F40
# limited functionality will be available
#%%if ( 0%%{?fedora} && 0%%{?fedora} >= 39 )
#%%global __requires_exclude ^python.*unicorn.*
#%%endif

# Some packages are missing in EPEL9/8
# limited functionality will be available
%if 0%{?rhel}
%global __requires_exclude python%{python3_pkgversion}-unicorn,python%{python3_pkgversion}-intervaltree,python%{python3_pkgversion}-colored-traceback,python%{python3_pkgversion}-ROPGadget,python%{python3_pkgversion}-rpyc
%endif


%description
Pwntools is a CTF framework and exploit development library. Written
in Python, it is designed for rapid prototyping and development, and
intended to make exploit writing as simple as possible.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Requires:       binutils

# As we have ignored the requirement of unicorn, lets at least recommend it
# Recommends only supported on fedora and rhel8+
# %%if (0%%{?fedora}) || ( 0%%{?rhel} && 0%%{?rhel} >= 8 )
Recommends:      python%{python3_pkgversion}-unicorn
# %%endif

%description -n python%{python3_pkgversion}-%{srcname}
Pwntools is a CTF framework and exploit development library. Written
in Python, it is designed for rapid prototyping and development, and
intended to make exploit writing as simple as possible.

# Waiting on pwntools to support newer sphinx shipped by Fedora.
# %%package doc
# Summary:        pwntools documentation
#
# %%description doc
# Documentation for pwntools.

%prep
%autosetup -n %{srcname}-%{version} -p1

#wrong permission
chmod -x docs/requirements.txt

# Generate buildrequres is failing to generate viable deps:
# - s390x due to missing (optional) python3 unicorn module
# - epel due to missing python3 modules colored-traceback, intervaltree, rpyc, unicorn
# generate_buildrequires
# pyproject_buildrequires


%build
%py3_build
# Waiting on pwntools to support newer sphinx shipped by Fedora.
# # Generate html documentation.
# PYTHONPATH=${PWD} sphinx-build-2 docs/source html
# # Remove the sphinx-build leftovers.
# rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

mv %{buildroot}%{_bindir}/checksec %{buildroot}%{_bindir}/checksec-pwntools

# setuptools < 60 installs pwntools-doc to sitelib
# setuptools >= 60 changes the installation location
# remove pwntools-doc from both locations
rm -rf %{buildroot}%{python3_sitelib}/pwntools-doc
rm -rf %{buildroot}%{_prefix}/pwntools-doc


%check
export PYTHONPATH="${PYTHONPATH:-%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}}"
%py3_check_import pwn pwnlib
%{__python3} -c "from pwn import *; sh=process('bash'); sh.sendline(b'echo hello | md5sum'); x=sh.read(); assert (x == b'b1946ac92492d2347c6235b4d2611184  -\n');"


%files -n python%{python3_pkgversion}-%{srcname}
%doc CHANGELOG.md CONTRIBUTING.md README.md TESTING.md docs/requirements.txt
%license LICENSE-pwntools.txt
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/pwn/
%{python3_sitelib}/pwnlib/
%{_bindir}/asm
%{_bindir}/checksec-pwntools
%{_bindir}/common
%{_bindir}/constgrep
%{_bindir}/cyclic
%{_bindir}/debug
%{_bindir}/disablenx
%{_bindir}/disasm
%{_bindir}/elfdiff
%{_bindir}/elfpatch
%{_bindir}/errno
%{_bindir}/hex
%{_bindir}/libcdb
%{_bindir}/main
%{_bindir}/phd
%{_bindir}/pwn
%{_bindir}/pwnstrip
%{_bindir}/scramble
%{_bindir}/shellcraft
%{_bindir}/template
%{_bindir}/unhex
%{_bindir}/update
%{_bindir}/version

# Waiting on pwntools to support newer sphinx shipped by Fedora.
# %%files doc
# %%doc html
# %%license LICENSE-pwntools.txt

%changelog
%autochangelog
