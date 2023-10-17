Name:           python-pan
Version:        0.22.0
%global         baserelease     1

License:        ISC
URL:            https://github.com/kevinsteves/pan-python
VCS:            https://github.com/kevinsteves/pan-python

%global         common_desc     %{expand:
pan-python is a Python package for Palo Alto Networks Next-Generation Firewalls,
WildFire and AutoFocus. It provides several components:
- Python and command line interface to the PAN-OS and Panorama XML API
- Command line program for managing PAN-OS XML configurations
- Python and command line interface to the WildFire API
- Python and command line interface to the AutoFocus API
- Python and command line interface to the PAN-OS licensing API
}

%global         sum             Python package for Palo Alto Networks Next-Generation Firewalls, WildFire and AutoFocus

%global         gituser         kevinsteves
%global         gitname         pan-python
%global         commit          d0db2571978edb9cf3036ed3c54a04499f82d332
%global         gitdate         20230308
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# By default build from the release tarball
# to build from git snapshot use rpmbuild --rebuild python-impacket.*.src.rpm --without release
%bcond_without  release

%if %{with release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/v%{version}/%{gitname}-%{version}.tar.gz
%else
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif


Summary:        %{sum}

BuildArch:      noarch

BuildRequires:  sed
BuildRequires:  grep

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  python%{python3_pkgversion}-tox-current-env


%description
%{common_desc}

#===== the python3 package definition
%package -n python%{python3_pkgversion}-pan
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}
Provides:       pan-python = %{version}-%{release}


%description -n python%{python3_pkgversion}-pan
Python3 package of %{name}. %{common_desc}


#===== Preparation
%prep
%if %{with release}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif


%generate_buildrequires
%pyproject_buildrequires -t


#===== Build
%build
%pyproject_wheel


#===== Check
%check
%tox
# Default tox
# PYTHONPATH=%%{buildroot}%%{python3_sitelib} python3 -c \
#    'import impacket.ImpactPacket ; impacket.ImpactPacket.IP().get_packet()'



#===== Install
%install
%pyproject_install
%pyproject_save_files pan


#===== files for python3 package
%files -n       python%{python3_pkgversion}-pan -f %{pyproject_files}
%license        LICENSE.txt
%doc            AUTHORS.rst HISTORY.rst README.rst
%{_bindir}/*.py


%changelog
* Tue Oct 17 2023 Michal Ambroz <rebus AT_ seznam.cz> - 0.22.0-1
- Initial package

