Name:           python-regipy
Version:        3.1.6
Release:        1%{?dist}
Summary:        Python Registry Parser
License:        MIT
URL:            https://github.com/mkorman90/regipy/

%global pypi_name regipy
%global pypi_version %{version}

Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(attrs) >= 21
BuildRequires:  python3dist(click) >= 7
BuildRequires:  python3dist(click) >= 7
BuildRequires:  python3dist(construct) >= 2.10
BuildRequires:  python3dist(inflection) >= 0.5.1
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-flake8)
BuildRequires:  python3dist(pytest-flake8)
BuildRequires:  python3dist(pytz)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(tabulate)
BuildRequires:  python3dist(tabulatelibfwsi-python) >= 20220123

%global _description %{expand:
regipy Regipy is a python library for parsing offline registry hives!Features:*
Use as a library * Recurse over the registry hive, from root or a given path
and get all subkeys and values * Read specific subkeys and values * Apply
transaction logs on a registry hive * Command Line Tools: * Dump an entire
registry hive to json * Apply transaction logs on a registry hive * Compare
registry hives...
}

%description %_description


%package -n     python%{python3_pkgversion}-regipy
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-regipy}

Requires:       python3dist(attrs) >= 21
Requires:       python3dist(click) >= 7
Requires:       python3dist(click) >= 7
Requires:       python3dist(construct) >= 2.10
Requires:       python3dist(inflection) >= 0.5.1
Requires:       python3dist(pytest)
Requires:       python3dist(pytest-flake8)
Requires:       python3dist(pytz)
Requires:       python3dist(setuptools)
Requires:       python3dist(tabulate)
Requires:       python3dist(tabulatelibfwsi-python) >= 20220123
%description -n python%{python3_pkgversion}-regipy
regipy Regipy is a python library for parsing offline registry hives!Features:*
Use as a library * Recurse over the registry hive, from root or a given path
and get all subkeys and values * Read specific subkeys and values * Apply
transaction logs on a registry hive * Command Line Tools: * Dump an entire
registry hive to json * Apply transaction logs on a registry hive * Compare
registry hives...


%prep
%autosetup -n regipy-%{version}
# Remove bundled egg-info
rm -rf regipy.egg-info

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files regipy

%check
%{__python3} setup.py test

%files -n python%{python3_pkgversion}-regipy -f %{pyproject_files}
%license LICENSE
%doc README.md docs/README.rst
%{_bindir}/registry-diff
%{_bindir}/registry-dump
%{_bindir}/registry-parse-header
%{_bindir}/registry-plugins-list
%{_bindir}/registry-plugins-run
%{_bindir}/registry-transaction-logs
%{python3_sitelib}/regipy
%{python3_sitelib}/regipy-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Dec 08 2023 Michal Ambroz <rebus@seznam.cz> - 3.1.6-1
- Initial package.
