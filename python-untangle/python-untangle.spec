Name:           python-untangle
Version:        1.2.1
Release:        1%{?dist}
Summary:        Converts XML to Python objects

License:        MIT
URL:            https://github.com/stchris/untangle
Source0:        https://github.com/stchris/untangle/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(defusedxml)

%description
[![Build Status]( [![PyPi version]( <a href" alt"Code style: black" src"
Converts XML to a Python object. * Siblings with similar names are grouped into
a list. * Children can be accessed with parent.child, attributes with
element['attribute'].

%package -n     python3-untangle
Summary:        %{summary}
%{?python_provide:%python_provide python3-untangle}

Requires:       (python3dist(defusedxml) >= 0.7.1 with python3dist(defusedxml) < 0.8~~)
%description -n python3-untangle
[![Build Status]( [![PyPi version]( <a href" alt"Code style: black" src"
Converts XML to a Python object. * Siblings with similar names are grouped into
a list. * Children can be accessed with parent.child, attributes with
element['attribute'].


%prep
%autosetup -n untangle-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-untangle
%license LICENSE
%doc README.md AUTHORS CHANGELOG.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/untangle.py
%{python3_sitelib}/untangle-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 07 2022 Michal Ambroz <rebus@seznam.cz> - 1.2.1-1
- Initial package.
