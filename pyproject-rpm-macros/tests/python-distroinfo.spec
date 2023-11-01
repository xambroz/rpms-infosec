Name:             python-distroinfo
Version:          0.3.2
Release:          0%{?dist}
Summary:          Parsing and querying distribution metadata stored in text/YAML files
License:          ASL 2.0
URL:              https://github.com/softwarefactory-project/distroinfo
Source0:          %{pypi_source distroinfo}
BuildArch:        noarch

BuildRequires:    pyproject-rpm-macros
BuildRequires:    python3-devel
BuildRequires:    python3-pytest
BuildRequires:    git-core

%description
This package uses setuptools and pbr.
It has setup_requires and tests that %%pyproject_buildrequires correctly
handles that including runtime requirements.
Run %%pyproject_check_import with top-level modules filtering.


%package -n python3-distroinfo
Summary:          %{summary}

%description -n python3-distroinfo
...


%prep
%autosetup -p1 -n distroinfo-%{version}
# we don't need pytest-runner
sed -Ei "s/(, )?'pytest-runner'//" setup.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files distroinfo


%check
%pytest
%pyproject_check_import -t


%files -n python3-distroinfo -f %{pyproject_files}
%doc README.rst AUTHORS
%license LICENSE
