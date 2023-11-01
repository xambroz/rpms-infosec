Name:           escape_percentages
Version:        0.1
Release:        0
Summary:        ...
License:        MIT
BuildArch:      noarch

%description
This spec file verifies that escaping percentage signs in paths is possible via
exactly 2 (or 8) percentage signs in a filelist and directly in the %%files section.
It serves as a regression test for pyproject_save_files:escape_rpm_path().
When this breaks, the function needs to be adapted.


%prep
cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
EOF

cat > setup.cfg << EOF
[metadata]
name = escape_percentages
version = 0.1
[options]
packages =
    escape_percentages
[options.package_data]
escape_percentages =
    *
EOF

mkdir -p escape_percentages
touch escape_percentages/__init__.py
# the paths on disk will have 1 percentage sign if we type 2 in the spec
# we use the word 'version' after the sign, as that is a known existing macro
touch 'escape_percentages/one%%version'


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files escape_percentages
touch '%{buildroot}/two%%version'


%check
grep '/escape_percentages/one' %{pyproject_files}



%files -f %{pyproject_files}
%if v"0%{?rpmversion}" >= v"4.18.90"
/two%%version
%else
/two%%%%%%%%version
%endif
