Name:           python-vt-py
Version:        0.19.0
Release:        %autorelease
Summary:        The official Python client library for VirusTotal
License:        Apache-2.0
URL:            https://github.com/VirusTotal/vt-py
VCS:            git:https://github.com/VirusTotal/vt-py

%global         pypi_name       vt-py
%global         pypi_version    %{version}

%global         gituser         VirusTotal
%global         gitname         vt-py

# Source0:      https://files.pythonhosted.org/packages/source/v/vt-py/vt_py-%%{version}.tar.gz
# Source0:      %%{pypi_source vt_py}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(aiofiles)
BuildRequires:  python3dist(aiohttp)
BuildRequires:  python3dist(flask)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-runner)
BuildRequires:  python3dist(pytest-asyncio)
BuildRequires:  python3dist(pytest-httpserver)
BuildRequires:  python3dist(setuptools)

%global _description %{expand:
This is the official Python client library for VirusTotal. With this
library you can interact with the [VirusTotal REST API v3]( and automate
your workflow quickly and efficiently. Things you can do with vt-py:
- Scan files and URLs
- Get information about files, URLs, domains, etc
- Perform VirusTotal Intelligence searches
}

%description %_description


%package -n     python%{python3_pkgversion}-vt-py
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-vt-py}

%description -n python%{python3_pkgversion}-vt-py
%{_description}

%prep
%autosetup -p1 -n vt-py-%{version}
# Remove bundled egg-info
rm -rf vt-py.egg-info

%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x test
%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files vt

%check
%pyproject_check_import
%{pytest}

%files -n python%{python3_pkgversion}-vt-py -f %{pyproject_files}
%doc README.md

%changelog
%{?%autochangelog: %autochangelog }

