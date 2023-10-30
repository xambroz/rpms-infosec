Name:           python-ipaddress
Version:        1.0.23
Release:        1%{?dist}
Summary:        IPv4/IPv6 manipulation library
License:        Python Software Foundation License
URL:            https://github.com/phihag/ipaddress

%global pypi_name ipaddress
%global pypi_version %{version}

# macro pytest is not defined on rhel7
%{!?pytest: %global pytest pytest-3}


Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytest

%description
Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2

%package -n     python%{python3_pkgversion}-ipaddress
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-ipaddress}

%description -n python%{python3_pkgversion}-ipaddress
Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%pytest -sv

%files -n python%{python3_pkgversion}-ipaddress
%license LICENSE
%doc README.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Sat Feb 11 2023 Michal Ambroz <rebus@seznam.cz> - 1.0.23-1
- Initial package.
