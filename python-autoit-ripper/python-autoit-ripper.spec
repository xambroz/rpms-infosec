Name:           python-autoit-ripper
Version:        1.1.2
Release:        %autorelease
Summary:        Extract AutoIt scripts embedded in PE binaries
License:        None
URL:            https://github.com/nazywam/AutoIt-Ripper

%global pypi_name autoit-ripper
%global pypi_version 1.1.2


Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%global _description %{expand:
 AutoIt-Ripper What is this This is a short python script that allows for
extraction of "compiled" AutoIt scripts from PE executables. References This
script is **heavily** based on 3 resources, definitely check them out if you
want to dig a bit deeper into AutoIt stuff: * * [Github mirror I]( * [Github
mirror II]( * * Supported AutoIt versions
}

%description %_description


%package -n     python%{python3_pkgversion}-autoit-ripper
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-autoit-ripper}

Requires:       python3dist(pefile)
Requires:       python3dist(setuptools)
%description -n python%{python3_pkgversion}-autoit-ripper
 AutoIt-Ripper What is this This is a short python script that allows for
extraction of "compiled" AutoIt scripts from PE executables. References This
script is **heavily** based on 3 resources, definitely check them out if you
want to dig a bit deeper into AutoIt stuff: * * [Github mirror I]( * [Github
mirror II]( * * Supported AutoIt versions


%prep
%autosetup -n autoit-ripper-%{version}
# Remove bundled egg-info
rm -rf autoit-ripper.egg-info

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files autoit_ripper

%files -n python%{python3_pkgversion}-autoit-ripper -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/autoit-ripper

%changelog
%autochangelog
