# Created by pyp2rpm-3.3.8
%global pypi_name ppdeep
%global pypi_version 20200505

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Pure-Python library for computing fuzzy hashes (ssdeep)

License:        None
URL:            https://github.com/elceef/ppdeep
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools


%description
This is a pure-Python library for computing context triggered piecewise hashes
(CTPH), also called fuzzy hashes, or often ssdeep after the name of a popular
tool. At a very high level, fuzzy hashing is a way to determine whether two
inputs are similar, rather than identical. Fuzzy hashes are widely adopted in
digital forensics and malware detection.This implementation is based on SpamSum
by...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
This is a pure-Python library for computing context triggered piecewise hashes
(CTPH), also called fuzzy hashes, or often ssdeep after the name of a popular
tool. At a very high level, fuzzy hashing is a way to determine whether two
inputs are similar, rather than identical. Fuzzy hashes are widely adopted in
digital forensics and malware detection.This implementation is based on SpamSum
by...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Mon Oct 23 2023 Michal Ambroz <rebus@seznam.cz> - 20200505-1
- Initial package.
