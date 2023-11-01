%global pypi_name openqa_client
Name:           python-%{pypi_name}
Version:        4.0.0
Release:        1%{?dist}
Summary:        Python client library for openQA API

License:        GPLv2+
URL:            https://github.com/os-autoinst/openQA-python-client
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
This package uses tox.ini file with recursive deps (via the -r option).


%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
%{summary}.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# setuptools-git is needed to build the source distribution, but not
# for packaging, which *starts* from the source distribution
# we sed it out to save ourselves a dependency, but that is not strictly required
sed -i -e 's., "setuptools-git"..g' pyproject.toml

# the tests don't actually need mock, they use unittest.mock
# https://github.com/os-autoinst/openQA-python-client/pull/21
sed -i '/mock/d' tests.requires


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
%tox


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.*
%license COPYING
