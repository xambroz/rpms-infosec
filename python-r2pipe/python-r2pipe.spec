Name:           python-r2pipe
Version:        1.9.4
Release:        1%{?dist}
Summary:        Pipe interface for radare2
License:        MIT
URL:            https://rada.re
VCS:            git:

%global         pypi_name r2pipe
%global         pypi_version %{version}

Source0:        %{pypi_source}
BuildArch:      noarch


BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%global _description %{expand:
 r2pipe for PythonInteract with radare2 using the !pipe command or in
standalone scripts that communicate with local or remote r2 via pipe, tcp or
http.
}

%description %_description


%package -n     python%{python3_pkgversion}-r2pipe
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-r2pipe}

%description -n python%{python3_pkgversion}-r2pipe
%{_description}


%prep
%autosetup -n r2pipe-%{version}
# Remove bundled egg-info
rm -rf r2pipe.egg-info

# Used as a test binary during pytest
ln -s /usr/bin/ls test/ls


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files r2pipe


%check
%{pytest} -k "not test_open_successfully_with_params and not test_r2ccal_successfully and not test_r2cmd_json_successfully and not test_r2cmd_successfully and not test_native_rcore"



%files -n python%{python3_pkgversion}-r2pipe -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Tue Sep 03 2024 Michal Ambroz <rebus _AT seznam.cz> - 1.9.4-1
- Initial package.
