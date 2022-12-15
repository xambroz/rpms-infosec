%global pypi_name xlrd2
%global pypi_version 1.3.4

Name:           python-xlrd2
Version:        1.3.4
Release:        1%{?dist}
Summary:        Library for developers to extract data from Microsoft Excel legacy spreadsheet files (xls)

License:        Apache License 2.0
URL:            https://github.com/DissectMalware/xlrd2
Source0:        https://github.com/DissectMalware/xlrd2/releases/download/v%{version}/xlrd2-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)

%global _description %{expand:
 xlrd2xlrd2 is an effort to extend [xlrd project]( which is no longer mintained
by its developers. The main goal is to make it suitable for extracting
necessary information from malicious xls documents.**Xlrd Purpose**: Provide a
library for developers to use to extract data from Microsoft Excel (tm)
spreadsheet files. It is not an end-user tool.**Versions of Python supported**:
2.7,...
}

%description %_description


%package -n     python%{python3_pkgversion}-xlrd2
Summary:        %{summary}
%description -n python%{python3_pkgversion}-xlrd2 %_description
%{?python_provide:%python_provide python%{python3_pkgversion}-xlrd2}



%package -n python-xlrd2-doc
Summary:        xlrd2 documentation
%description -n python-xlrd2-doc
Documentation for xlrd2

%prep
%autosetup -n xlrd2-%{version}
# Remove bundled egg-info
rm -rf .egg-info

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

%files -n python%{python3_pkgversion}-xlrd2
%license LICENSE docs/licenses.rst
%doc README.md
%{_bindir}/runxlrd2.py
%{python3_sitelib}/xlrd2
%{python3_sitelib}/xlrd2-%{version}-py%{python3_version}.egg-info

%files -n python-xlrd2-doc
%license LICENSE docs/licenses.rst
%doc html

%changelog
* Sat Dec 10 2022 Michal Ambroz <rebus@seznam.cz> - 1.3.4-1
- Initial package.
