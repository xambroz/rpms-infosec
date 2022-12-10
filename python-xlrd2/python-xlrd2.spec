# Created by pyp2rpm-3.3.8
%global pypi_name xlrd2
%global pypi_version 1.3.4

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Library for developers to extract data from Microsoft Excel legacy spreadsheet files (xls)

License:        Apache License 2.0
URL:            None
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)

%description
 xlrd2xlrd2 is an effort to extend [xlrd project]( which is no longer mintained
by its developers. The main goal is to make it suitable for extracting
necessary information from malicious xls documents.**Xlrd Purpose**: Provide a
library for developers to use to extract data from Microsoft Excel (tm)
spreadsheet files. It is not an end-user tool.**Versions of Python supported**:
2.7,...

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
 xlrd2xlrd2 is an effort to extend [xlrd project]( which is no longer mintained
by its developers. The main goal is to make it suitable for extracting
necessary information from malicious xls documents.**Xlrd Purpose**: Provide a
library for developers to use to extract data from Microsoft Excel (tm)
spreadsheet files. It is not an end-user tool.**Versions of Python supported**:
2.7,...

%package -n python-%{pypi_name}-doc
Summary:        xlrd2 documentation
%description -n python-%{pypi_name}-doc
Documentation for xlrd2

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
%{__python3} setup.py test &&

%files -n python3-%{pypi_name}
%license LICENSE docs/licenses.rst
%doc README.md
%{_bindir}/runxlrd2.py
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE docs/licenses.rst

%changelog
* Sat Dec 10 2022 Michal Ambroz <rebus@seznam.cz> - 1.3.4-1
- Initial package.
