Name:           printrun
Version:        2.0.0~rc6
%global upstream_version 2.0.0rc6
Release:        0%{?dist}
Summary:        RepRap printer interface and tools
License:        GPLv3+ and FSFAP
URL:            https://github.com/kliment/Printrun
Source0:        https://github.com/kliment/Printrun/archive/%{name}-%{upstream_version}.tar.gz

# fix locale location
Patch0:         https://github.com/kliment/Printrun/pull/1101.patch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  gcc

%description
This package contains lang files outside of printrun module.
Building this tests that lang files are marked with %%lang in filelist.


%prep
%autosetup -p1 -n Printrun-printrun-%{upstream_version}


%generate_buildrequires
%pyproject_buildrequires -R


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files printrun +auto


%check
# Internal check if generated lang entries are same as
# the ones generated using %%find_lang
%find_lang pronterface
%find_lang plater

grep '^%%lang' %{pyproject_files} | sort > tested.lang
sort pronterface.lang plater.lang > expected.lang
diff tested.lang expected.lang

# Internal check that generated files contain nested __pycache__ directories
grep -E '/printrun/__pycache__$' %{pyproject_files}


%files -f %{pyproject_files}
%doc README*
%license COPYING
