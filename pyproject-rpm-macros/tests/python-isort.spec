%global modname isort

Name:               python-%{modname}
Version:            4.3.21
Release:            7%{?dist}
Summary:            Python utility / library to sort Python imports

License:            MIT
URL:                https://github.com/timothycrosley/%{modname}
Source0:            %{url}/archive/%{version}-2/%{modname}-%{version}-2.tar.gz
BuildArch:          noarch
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      pyproject-rpm-macros

%description
This package contains executables.
Building this tests that executables are not listed when +auto is not used
with %%pyproject_save_files.

This package also uses %%{python3_pkgversion} in name and has a very limited
set of dependencies -- allows to set a different value for it in the CI.

%package -n python%{python3_pkgversion}-%{modname}
Summary:            %{summary}

%description -n python%{python3_pkgversion}-%{modname}
%{summary}.


%prep
%autosetup -n %{modname}-%{version}-2


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files isort


%check
# Internal check if the instalation outputs expected result
test -d %{buildroot}%{python3_sitelib}/%{modname}/
test -d %{buildroot}%{python3_sitelib}/%{modname}-%{version}.dist-info/

# Internal check that executables are not present when +auto was not used with %%pyproject_save_files
grep -F %{_bindir}/%{modname} %{pyproject_files} && exit 1 || true


%files -n python%{python3_pkgversion}-%{modname} -f %{pyproject_files}
%doc README.rst *.md
%license LICENSE
%{_bindir}/%{modname}
