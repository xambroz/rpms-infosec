# Created by pyp2rpm-3.3.8
%global pypi_name dsinternals
%global pypi_version 1.2.4

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:	Directory Services Internals Library for python

License:        GPL2
URL:            http://github.com/p0dalirius/pydsinternals
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
Directory Services Internals Library.
Python native library containing necessary classes, functions and
structures to interact with Windows Active Directory. Installation python3 -m
pip install dsinternals ContributingPull requests are welcome. Feel free to
open an issue if...

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Directory Services Internals Library.
Python native library containing necessary classes, functions and
structures to interact with Windows Active Directory. Installation python3 -m
pip install dsinternals ContributingPull requests are welcome. Feel free to
open an issue if...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/tests
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Mon Jan 30 2023 Michal Ambroz <rebus@seznam.cz> - 1.2.4-1
- Initial package.
