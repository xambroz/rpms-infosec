Name:           python-dsinternals
Version:        1.2.4
Release:        2%{?dist}
Summary:        Directory Services Internals Library for python
License:        GPL-2.0-only
URL:            http://github.com/p0dalirius/pydsinternals

%global pypi_name dsinternals
%global pypi_version 1.2.4

Source0:        %{pypi_source}

# Build related stuff
# https://github.com/p0dalirius/pydsinternals/pull/8.patch
Patch0:         dsinternals-1.2.4-build.patch


BuildArch:      noarch

BuildRequires:  python3-rpm-macros

%if ! 0%{?rhel} == 7
# pyproject-rpm-macros missing on EPEL7
BuildRequires:  pyproject-rpm-macros
%endif

# Planning the compatibility with EPEL, hence using the pkgversion
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools


%if 0%{?rhel} && 0%{?rhel} < 9
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel

# Needed for tests
BuildRequires:  python%{python3_pkgversion}-pyOpenSSL
BuildRequires:  python%{python3_pkgversion}-pycryptodomex
%endif


%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 9 )
BuildRequires:  python%{python3_pkgversion}-tox-current-env
%endif

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

# Sanitize the executable permissions
find ./ -type f -exec chmod -x '{}' ';'
chmod +x setup.py

%py3_shebang_fix dsinternals
%py3_shebang_fix tests


# Generating of build requirements doesn't work on epel7, has problems on epel8
%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 9 )
%generate_buildrequires
%pyproject_buildrequires -t
%endif


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files dsinternals


%check
# rhel7 missing tox and pyproject macros
%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 9 )
python3 -m unittest discover -v
%tox
%endif


%files -n python%{python3_pkgversion}-dsinternals -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Tue Jan 23 2024 Michal Ambroz <rebus@seznam.cz> - 1.2.4-2
- conditionalized pyproject_buildrequires

* Mon Jan 30 2023 Michal Ambroz <rebus@seznam.cz> - 1.2.4-1
- Initial package
