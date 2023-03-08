# Created by pyp2rpm-3.3.8
%global pypi_name pygdbmi
%global pypi_version 0.11.0.0

Name:           python-pygdbmi
Version:        0.11.0.0
Release:        1%{?dist}
Summary:        Parse gdb machine interface output with Python

License:        MIT
URL:            https://github.com/cs01/pygdbmi
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%global _description %{expand:
<h1 align"center"> pygdbmi - Get Structured Output from GDB's Machine Interface
<p align"center"><a href" <img src" alt"Test status" /></a><a href" <img src"
alt"PyPI version"/></a></p>**Documentation** [ Code** [ (**py**) [**gdb**](
machine interface [(**mi**)](
}

%description %_description


%package -n     python%{python3_pkgversion}-pygdbmi
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-pygdbmi}

%description -n python%{python3_pkgversion}-pygdbmi
<h1 align"center"> pygdbmi - Get Structured Output from GDB's Machine Interface
<p align"center"><a href" <img src" alt"Test status" /></a><a href" <img src"
alt"PyPI version"/></a></p>**Documentation** [ Code** [ (**py**) [**gdb**](
machine interface [(**mi**)](


%prep
%autosetup -n pygdbmi-%{version}
# Remove bundled egg-info
rm -rf pygdbmi.egg-info

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pygdbmi

%files -n python%{python3_pkgversion}-pygdbmi -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Wed Mar 08 2023 Michal Ambroz <rebus@seznam.cz> - 0.11.0.0-1
- Initial package.
