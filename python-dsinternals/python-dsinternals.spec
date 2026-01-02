Name:           python-dsinternals
Version:        1.2.4
Release:        %autorelease -b 5
Summary:        Directory Services Internals Library for python
URL:            http://github.com/p0dalirius/pydsinternals

# contained LICESNE file has old FSF address
# reported to upstream - https://github.com/p0dalirius/pydsinternals/issues/14
License:        GPL-2.0-only

%global         pypi_name dsinternals
%global         pypi_version 1.2.4

Source0:        %{pypi_source}
Source1:        %{name}.rpmlintrc

# Build related stuff
# https://github.com/p0dalirius/pydsinternals/pull/8.patch
Patch0:         dsinternals-1.2.4-build.patch

BuildArch:      noarch

BuildRequires:  python3-rpm-macros
BuildRequires:  pyproject-rpm-macros

# Planning the compatibility with EPEL, hence using the pkgversion
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools


%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 9 )
# Needed for tests
BuildRequires:  python%{python3_pkgversion}-pyOpenSSL
BuildRequires:  python%{python3_pkgversion}-pycryptodomex

# python3-tox-current-env package is not available on EPEL8
# https://src.fedoraproject.org/rpms/python-tox-current-env
BuildRequires:  python%{python3_pkgversion}-tox-current-env

%else
# RHEL8 - deps bellow are for RHEL8
# This should be added by generate_buildrequires on newer platforms
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel

# Needed for tests
# RHEL8 - only the python3 versions of these pkgs available
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pycryptodomex

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

# Remove shebangs from Python library modules (they shouldn't be executable)
find dsinternals -type f -name "*.py" -exec sed -i -e '1{\@^#!/usr/bin/env python@d; \@^#!/usr/bin/python@d}' {} \;


# Generating of build requirements doesn't work on EPEL8
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
%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 9 )
%tox

%else
# RHEL8 - Tox not available on RHEL8
python3 -m unittest discover -v
%endif


%files -n python%{python3_pkgversion}-dsinternals -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
%autochangelog
