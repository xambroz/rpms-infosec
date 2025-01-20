Name:           python-vt-py
Version:        0.19.0
Release:        %autorelease
Summary:        The official Python client library for VirusTotal

License:        ...
URL:            https://github.com/VirusTotal/vt-py
Source:         %{pypi_source vt_py}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'vt-py' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-vt-py
Summary:        %{summary}

%description -n python3-vt-py %_description

# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
%pyproject_extras_subpkg -n python3-vt-py test


%prep
%autosetup -p1 -n vt_py-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files ...


%check
%pyproject_check_import


%files -n python3-vt-py -f %{pyproject_files}


%changelog
%{?%autochangelog: %autochangelog }
