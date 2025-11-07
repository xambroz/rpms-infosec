Name:           python-nose2pytest
Version:        1.0.8
Release:        1%{?dist}
Summary:        Convert nose.tools.assert_ calls found in your Nose test modules into raw asserts for pytest

License:        BSD-3
URL:            https://github.com/schollii/nose2pytest
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%global pypi_name nose2pytest
%global pypi_version %{version}


%description
UNKNOWN



%package -n     python3-nose2pytest
Summary:        %{summary}
%{?python_provide:%python_provide python3-nose2pytest}

Requires:       python3dist(setuptools)
%description -n python3-nose2pytest
UNKNOWN




%prep
%autosetup -n nose2pytest-%{version}
# Remove bundled egg-info
rm -rf nose2pytest.egg-info

%build
%py3_build

%install
%py3_install

%check
%{pytest} -v

%files -n python3-nose2pytest
%license LICENSE.txt
%doc README.rst
%{_bindir}/nose2pytest
%{python3_sitelib}/nose2pytest
%{python3_sitelib}/nose2pytest-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Dec 07 2023 Michal Ambroz <rebus@seznam.cz> - 1.0.8-1
- Initial package.
