# Created by pyp2rpm-3.3.8
%global pypi_name dsinternals
%global pypi_version 1.2.4

Name:           python-dsinternals
Version:        1.2.4
Release:        1%{?dist}
Summary:        Directory Services Internals Library for python

License:        GPL2
URL:            http://github.com/p0dalirius/pydsinternals
Source0:        %{pypi_source}
Patch0:         dsinternals-1.2.4-build.patch
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  python%{python3_pkgversion}-pyOpenSSL
BuildRequires:  python%{python3_pkgversion}-pycryptodomex


%global _description %{expand:
Directory Services Internals Library.
Python native library containing necessary classes, functions and
structures to interact with Windows Active Directory. Installation python3 -m
pip install dsinternals ContributingPull requests are welcome. Feel free to
open an issue if...
}

%description %_description


%package -n     python%{python3_pkgversion}-dsinternals
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-dsinternals}

%description -n python%{python3_pkgversion}-dsinternals
%_description

%prep
%autosetup -p1 -n dsinternals-%{version}
# Remove bundled egg-info
rm -rf .egg-info

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files dsinternals



%check
python3 -m unittest discover -v
%tox

%files -n python%{python3_pkgversion}-dsinternals -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Mon Jan 30 2023 Michal Ambroz <rebus@seznam.cz> - 1.2.4-1
- Initial package
