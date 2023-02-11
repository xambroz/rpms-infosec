# Created by pyp2rpm-3.3.8
%global pypi_name boofuzz
%global pypi_version 0.4.1

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        A fork and successor of the Sulley Fuzzing Framework

License:        None
URL:            https://github.com/jtpereyda/boofuzz
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(attrs)
BuildRequires:  python3dist(black)
BuildRequires:  python3dist(check-manifest)
BuildRequires:  python3dist(click)
BuildRequires:  python3dist(colorama)
BuildRequires:  python3dist(flake8)
BuildRequires:  python3dist(flask)
BuildRequires:  python3dist(funcy)
BuildRequires:  python3dist(future)
BuildRequires:  python3dist(ipaddress)
BuildRequires:  python3dist(mock)
BuildRequires:  python3dist(netifaces)
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(pydot)
BuildRequires:  python3dist(pygments) >= 2.4
BuildRequires:  python3dist(pygments) >= 2.4
BuildRequires:  python3dist(pyserial)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-bdd)
BuildRequires:  python3dist(pytest-cov)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  python3dist(tornado)
BuildRequires:  python3dist(tox)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(sphinx)

%description
 :width: 60%boofuzz: Network Protocol Fuzzing for Humans :target:

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(attrs)
Requires:       python3dist(click)
Requires:       python3dist(colorama)
Requires:       python3dist(flask)
Requires:       python3dist(funcy)
Requires:       python3dist(future)
Requires:       python3dist(psutil)
Requires:       python3dist(pydot)
Requires:       python3dist(pygments) >= 2.4
Requires:       python3dist(pyserial)
Requires:       python3dist(setuptools)
Requires:       python3dist(six)
Requires:       python3dist(sphinx)
Requires:       python3dist(sphinx-rtd-theme)
Requires:       python3dist(tornado)
%description -n python3-%{pypi_name}
 :width: 60%boofuzz: Network Protocol Fuzzing for Humans :target:

%package -n python-%{pypi_name}-doc
Summary:        boofuzz documentation
%description -n python-%{pypi_name}-doc
Documentation for boofuzz

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
# Exclude tests requiring root permissions and networking
%pytest -k "not test_raw_l2 and not test_raw_l3 and not test_udp_broadcast_client"


%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{_bindir}/boo
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE.txt

%changelog
* Sat Feb 11 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.4.1-1
- Initial package.
