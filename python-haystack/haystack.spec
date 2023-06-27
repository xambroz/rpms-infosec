%global pypi_name haystack

Name:           %{pypi_name}
Version:        0.42
Release:        1%{?dist}
Summary:        A process heap analysis framework

License:        GPL-3.0-or-later
URL:            https://github.com/trolldbois/python-haystack
Source0:        https://github.com/trolldbois/python-haystack/archive/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Test requirements, some tests are failing. gnu/stubs-32.h would be needed 
# for the x86_64 build because the dumps for the tests are not provided
#BuildRequires:  clang
#BuildRequires:  python3-pytest
#BuildRequires:  python3-ptrace
#BuildRequires:  python3-construct
#BuildRequires:  python3-pefile
#BuildRequires:  python3-future

%description
haystack is an heap analysis framework, focused on searching and reversing
of C structure in allocated memory.

The first function/API is the SEARCH function. It gives the ability
to search for known record types in a process memory dump or live
process's memory. The second function/API is the REVERSE function in the
extension python-haystack-reverse It aims at helping an analyst in reverse
engineering the memory records types present in a process heap. It focuses
on reconstruction, classification of classic C structures from memory. It
attempts to recreate types definition.

%prep
%autosetup -n python-%{pypi_name}-%{version}
# Remove the shebangs
sed -i -e '/^#!\//, 1d' haystack/{*.py,*/*.py,*/*/*.py}

%build
%py3_build

%install
%py3_install

#%check
#%{__python3} setup.py test

%files
%doc CHANGES.txt README.rst TODO
%license LICENSE.txt
%{_bindir}/*
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}*.egg-info

%changelog
* Sat Jun 15 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.42-1
- Initial package for Fedora
