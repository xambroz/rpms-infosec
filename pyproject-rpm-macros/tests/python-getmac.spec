Name:           python-getmac
Version:        0.8.3
Release:        0%{?dist}
Summary:        Get MAC addresses of remote hosts and local interfaces
License:        MIT
URL:            https://github.com/GhostofGoes/getmac
Source0:        %{pypi_source getmac}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros


%global _description %{expand:
Test that manpages are correctly processed by %%%%%%%%pyproject_save_files '*' +auto.
Run %%%%%%%%_pyproject_check_import_allow_no_modules twice
- exclude all modules and test the check still passes thanks to -M option
- regression test: test that check imports all modules even if -M option is set}


%description %_description

%package -n     python3-getmac
Summary:        %{summary}

%description -n python3-getmac %_description


%prep
%autosetup -p1 -n getmac-%{version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '*' +auto


%check
# Internal check for our macros, assert the behavior of the import check macros
# Both of the macros should succeed
%pyproject_check_import
%_pyproject_check_import_allow_no_modules
(%{pyproject_check_import}) 2>pyproject_check_import.stderr
(%{_pyproject_check_import_allow_no_modules}) 2>_pyproject_check_import_allow_no_modules.stderr

# Modules were found, stderrs should include getmac.getmac
grep '^Check import: getmac\.getmac$' pyproject_check_import.stderr
grep '^Check import: getmac\.getmac$' _pyproject_check_import_allow_no_modules.stderr

# Now let's pretend no modules were found at all
echo -e '' > %{_pyproject_modules}

# This should fail
(%{pyproject_check_import}) && exit 1 || true

# This should succeed and say something about no modules found
%{_pyproject_check_import_allow_no_modules}
(%{_pyproject_check_import_allow_no_modules}) 2>_pyproject_check_import_allow_no_modules.stderr
grep '\bNo modules to check found\b' _pyproject_check_import_allow_no_modules.stderr

# We want to ensure the rest of the %%check section is still executed
# (To avoid a temptation to call `exit 0` from %%_pyproject_check_import_allow_no_modules)
# We'll touch a marker file here and assert its presence in %%files
touch %{buildroot}/check-completed-entirely

# Internal check for our macros, assert there is a manpage:
test -f %{buildroot}%{_mandir}/man1/getmac.1*


%files -n python3-getmac -f %{pyproject_files}
/check-completed-entirely
