Name:           python-minidump
Version:        0.0.22
Release:        1%{?dist}
Summary:        Python library to parse Windows minidump file format

License:        None
URL:            https://github.com/skelsec/minidump

# Created by pyp2rpm-3.3.10
%global pypi_name minidump
%global pypi_version %{version}

Source0:        %{pypi_source}
BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
Python library to parse Windows minidump file format

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

Requires:       python3dist(setuptools)
%description -n python%{python3_pkgversion}-%{pypi_name}
Python library to parse Windows minidump file format


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/minidump
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sat Nov 25 2023 Michal Ambroz <rebus@seznam.cz> - 0.0.22-1
- Initial package.
