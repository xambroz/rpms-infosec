Name:           python-setuptools_scm
Version:        6.0.1

Release:        0%{?dist}
Summary:        The blessed package to manage your versions by SCM tags
License:        MIT
URL:            https://github.com/pypa/setuptools_scm/
Source0:        %{pypi_source setuptools_scm}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  /usr/bin/git

# flake8 is still missing tests deps in EPEL 9
%if 0%{?fedora}
%bcond_without flake8
%else
%bcond_with flake8
%endif

%description
Here we test that %%pyproject_extras_subpkg works and generates
setuptools_scm[toml] extra subpackage.

We also check passing multiple -e flags to %%pyproject_buildrequires.
The tox environments also have a dependency on an extra ("toml").


%package -n python3-setuptools_scm
Summary:        %{summary}

%description -n python3-setuptools_scm
...

%pyproject_extras_subpkg -n python3-setuptools_scm toml


%prep
%autosetup -p1 -n setuptools_scm-%{version}


%generate_buildrequires
# Note that you should not run flake8-like linters in Fedora spec files,
# here we do it solely to check the *ability* to use multiple toxenvs.
%pyproject_buildrequires -e %{default_toxenv}-test %{?with_flake8:-e flake8}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files setuptools_scm


%check
# This tox should run all the toxenvs specified via -e in %%pyproject_buildrequires
# We only run some of the tests (running all of them requires network connection and is slow)
%tox -- -- -k test_version -Wdefault | tee toxlog

# Internal check for our macros: Assert both toxenvs were executed.
grep -E 'py%{python3_version_nodots}-test: (OK|commands succeeded)' toxlog
grep -E 'flake8: (OK|commands succeeded)' toxlog %{?!with_flake8:&& exit 1 || true}

# Internal check for our macros
# making sure that %%{_pyproject_ghost_distinfo} has the right content
test -f %{_pyproject_ghost_distinfo}
test "$(cat %{_pyproject_ghost_distinfo})" == "%ghost %{python3_sitelib}/setuptools_scm-%{version}.dist-info"


%files -n python3-setuptools_scm -f %{pyproject_files}
%doc README.rst
%doc CHANGELOG.rst
%license LICENSE
