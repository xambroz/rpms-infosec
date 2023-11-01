Name:           python-mistune
Version:        0.8.3
Release:        11%{?dist}
Summary:        Markdown parser for Python

License:        BSD
URL:            https://github.com/lepture/mistune
Source0:        %{url}/archive/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

# optional dependency, listed explicitly to have the extension module:
BuildRequires:  python%{python3_pkgversion}-Cython

%description
This package contains an extension module. Does not contain pyproject.toml.
Has a script (.py) and extension (.so) with identical name.
Building this tests:
- installing both a script and an extension with the same name
- default build backend without pyproject.toml
Check %%pyproject_check_import basic functionality.

This package also uses %%{python3_pkgversion} in name and has a very limited
set of dependencies -- allows to set a different value for it in the CI.

%package -n python%{python3_pkgversion}-mistune
Summary:        %summary

%description -n python%{python3_pkgversion}-mistune
%{summary}


%prep
%autosetup -n mistune-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files mistune


%check
%pyproject_check_import

# Internal check for our macros
# making sure that pyproject_install outputs these files so that we can test behaviour of %%pyproject_save_files
# when a package has multiple files with the same name (here script and extension)
test -f %{buildroot}%{python3_sitearch}/mistune.py
test -f %{buildroot}%{python3_sitearch}/mistune.cpython-*.so


%files -n python%{python3_pkgversion}-mistune -f %{pyproject_files}
%doc README.rst
%license LICENSE
