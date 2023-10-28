Name:           python-xlrd2
Version:        1.3.4
Release:        1%{?dist}
Summary:        Library to extract data from Microsoft Excel legacy spreadsheet files (xls)

License:        Apache-2.0
URL:            https://github.com/DissectMalware/xlrd2
Source0:        https://github.com/DissectMalware/xlrd2/releases/download/v%{version}/xlrd2-%{version}.tar.gz

# https://github.com/DissectMalware/xlrd2/issues/11
# Patch0:         https://patch-diff.githubusercontent.com/raw/DissectMalware/xlrd2/pull/12.patch#/python-xlrd2-xmlengine.patch
Patch0:         https://patch-diff.githubusercontent.com/raw/python-excel/xlrd/pull/375.patch#/python-xlrd2-defusedxmliter.patch

BuildArch:      noarch

%global pypi_name xlrd2
# macro is not defined on rhel7
%{!?pytest: %global pytest pytest-3}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-pytest

%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
# pkginfo used for generating the documentation, missing on rhel7
BuildRequires:  python%{python3_pkgversion}-pkginfo
%endif

%global _description %{expand:
The xlrd2 module is an effort to extend [xlrd project]( which is no longer
mintained by its developers). The main goal is to make it suitable for
extracting necessary information from malicious xls documents.
**Xlrd Purpose**: Provide a library for developers to use to extract data
from Microsoft Excel (tm) spreadsheet files.
It is not an end-user tool.
}

%description %_description


%package -n     python%{python3_pkgversion}-xlrd2
Summary:        %{summary}
%description -n python%{python3_pkgversion}-xlrd2 %_description
%if 0%{?rhel}
%{?python_provide:%python_provide python%{python3_pkgversion}-xlrd2}
%else
%py_provides    python3-xlrd2
%endif


%package -n python-xlrd2-doc
Summary:        xlrd2 documentation
%description -n python-xlrd2-doc
Documentation for xlrd2


%prep
%autosetup -p 1 -n xlrd2-%{version}
# Remove bundled egg-info
rm -rf .egg-info

# Unfinished migration from xlrd to xlrd2
sed -i -e 's/from xlrd/from xlrd2/;' scripts/runxlrd2.py docs/vulnerabilities.rst

# Fix CRLF ends of lines
echo "=== Fixing CRLF ends of lines for all text files"
find ./ -type f '!' '(' -name '*.xls' -o -name '*.xlsx' ')' -print -exec sed '-i' '-e' 's/\r$//' '{}' ';'



%build
# package doesn't support pyproject yet
%py3_build

%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 ) 
# on rhel7 there is missing package python3-pkginfo
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
%endif

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install


%check
%pytest -sv -k "not test_names_demo"


%files -n python%{python3_pkgversion}-xlrd2
%license LICENSE docs/licenses.rst
%doc README.md
%{_bindir}/runxlrd2.py
%{python3_sitelib}/xlrd2
%{python3_sitelib}/xlrd2-%{version}-py%{python3_version}.egg-info

# on rhel7 there is missing package python3-pkginfo
%files -n python-xlrd2-doc
%license LICENSE docs/licenses.rst
%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 ) 
%doc html
%endif
%doc examples

%changelog
* Sat Dec 10 2022 Michal Ambroz <rebus@seznam.cz> - 1.3.4-1
- Initial package.
