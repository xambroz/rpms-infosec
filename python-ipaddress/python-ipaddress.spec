# Created by pyp2rpm-3.3.8
%global pypi_name ipaddress
%global pypi_version 1.0.23

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        IPv4/IPv6 manipulation library

License:        Python Software Foundation License
URL:            https://github.com/phihag/ipaddress
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%pytest -sv

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sat Feb 11 2023 Michal Ambroz <rebus@seznam.cz> - 1.0.23-1
- Initial package.
