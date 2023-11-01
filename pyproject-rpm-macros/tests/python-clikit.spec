%global pypi_name clikit
Name:           python-%{pypi_name}
Version:        0.3.1
Release:        1%{?dist}
Summary:        Builds beautiful and testable command line interfaces

License:        MIT
URL:            https://github.com/sdispater/clikit
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel

%description
Tests building with the poetry build backend.


%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
%{summary}.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%generate_buildrequires
# this runtime-requires pastel<0.2 which is no longer available in Fedora
%pyproject_buildrequires -R


%build
%pyproject_wheel


%install
# Internal check that $TMPDIR is not changed
TPMDIR_original="$TMPDIR"

%pyproject_install

# Internal check that $TMPDIR is not changed
test "$TMPDIR" == "$TPMDIR_original"


%check
# Internal check that the RECORD and REQUESTED files are
# always removed in %%pyproject_wheel
test ! $(find %{buildroot}%{python3_sitelib}/ | grep -E "\.dist-info/RECORD$")
test ! $(find %{buildroot}%{python3_sitelib}/ | grep -E "\.dist-info/REQUESTED$")


%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
