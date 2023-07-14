# Created by pyp2rpm-3.3.8
%global pypi_name umodbus
%global pypi_version 1.0.4

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Implementation of the Modbus protocol in pure Python

License:        MPL
URL:            https://github.com/AdvancedClimateSystems/umodbus/
Source0:        https://files.pythonhosted.org/packages/source/u/%{pypi_name}/uModbus-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
 uModbus or (μModbus) is a pure Python implementation of the Modbus protocol as
described in the MODBUS Application Protocol Specification V1.1b3_. uModbus

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       (python3dist(pyserial) >= 3.4 with python3dist(pyserial) < 4)
%description -n python3-%{pypi_name}
 uModbus or (μModbus) is a pure Python implementation of the Modbus protocol as
described in the MODBUS Application Protocol Specification V1.1b3_. uModbus


%prep
%autosetup -n uModbus-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/uModbus-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Fri Jul 14 2023 Michal Ambroz <rebus@seznam.cz> - 1.0.4-1
- Initial package.
