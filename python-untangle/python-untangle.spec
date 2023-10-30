Name:           python-untangle
Version:        1.2.1
Release:        1%{?dist}
Summary:        Converts XML to Python objects

License:        MIT
URL:            https://github.com/stchris/untangle
Source0:        https://github.com/stchris/untangle/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch


# macro pytest is not defined on rhel7
%{!?pytest: %global pytest pytest-3}


BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-defusedxml
BuildRequires:  python3-pytest


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

Requires:       python%{python3_pkgversion}-defusedxml >= 0.7.1

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
%pytest


%files -n python%{python3_pkgversion}-untangle
%license LICENSE
%doc README.md AUTHORS CHANGELOG.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/untangle.py
%{python3_sitelib}/untangle-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 07 2022 Michal Ambroz <rebus@seznam.cz> - 1.2.1-1
- Initial package.
