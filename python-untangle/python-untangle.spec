Name:           python-untangle
Version:        1.2.1
Release:        1%{?dist}
Summary:        Converts XML to Python objects

License:        MIT
URL:            https://github.com/stchris/untangle
Source0:        https://github.com/stchris/untangle/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch


# macro pytest is not defined on rhel7
%{!?pytest: %global pytest PYTHONPATH="%{buildroot}%{python3_sitelib}:$PYTHONPATH" pytest-3}


BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-defusedxml
BuildRequires:  python%{python3_pkgversion}-pytest


%description
[![Build Status]( [![PyPi version]( <a href" alt"Code style: black" src"
Converts XML to a Python object. * Siblings with similar names are grouped into
a list. * Children can be accessed with parent.child, attributes with
element['attribute'].

%package -n     python%{python3_pkgversion}-untangle
Summary:        %{summary}
%if 0%{?rhel}
%{?python_provide:%python_provide python%{python3_pkgversion}-untangle}
%else
%py_provides    python3-xlrd2
%endif

Requires:       python%{python3_pkgversion}-defusedxml

%description -n python%{python3_pkgversion}-untangle
Converts XML to a Python object. Siblings with similar names are grouped into
a list. Children can be accessed with parent.child, attributes with
element.


%prep
%autosetup -n untangle-%{version}

%build
%py3_build

%install
%py3_install

%check
%if 0%{?rhel} == 7
# avoid UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 6: ordinal not in range(128)
# in UnicodeTestCase.test_unicode_element
export LANG=en_US.UTF-8
%endif

%pytest -sv


%files -n python%{python3_pkgversion}-untangle
%license LICENSE
%doc README.md AUTHORS CHANGELOG.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/untangle.py
%{python3_sitelib}/untangle-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 07 2022 Michal Ambroz <rebus@seznam.cz> - 1.2.1-1
- Initial package.
