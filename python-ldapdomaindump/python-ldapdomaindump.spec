Name:           python-ldapdomaindump
Version:        0.9.4
Release:        1%{?dist}
Summary:        Active Directory information dumper via LDAP
License:        MIT
URL:            https://github.com/dirkjanm/ldapdomaindump/
VCS:            https://github.com/dirkjanm/ldapdomaindump/

%global         pypi_name ldapdomaindump
%global         pypi_version %{version}

Source0:        %{pypi_source}

# Remove unversioned shabeng
Patch0:         https://github.com/dirkjanm/ldapdomaindump/pull/59.patch#/%{name}-59-shabeng.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%global common_description %{expand:
ldapdomaindump is a tool for collecting and parsing information available
via LDAP and outputting it in a human readable HTML format,
as well as machine readable json and csv/tsv/greppable files.
}

%description %common_description



%package -n     python%{python3_pkgversion}-ldapdomaindump
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-ldapdomaindump}

Requires:       python%{python3_pkgversion}-dnspython
Requires:       python%{python3_pkgversion}-future
Requires:       python%{python3_pkgversion}-ldap3

%description -n python%{python3_pkgversion}-ldapdomaindump %common_description


%prep
%autosetup -n ldapdomaindump-%{version} -p 1
# Remove bundled egg-info
rm -rf ldapdomaindump.egg-info

# Get rid of the windows ends of lines
# proposed as https://github.com/dirkjanm/ldapdomaindump/pull/60
sed -i -e 's/\r//g;' Readme.md  ldapdomaindump/__init__.py ldapdomaindump/convert.py setup.py


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files ldapdomaindump

%files -n python%{python3_pkgversion}-ldapdomaindump -f %{pyproject_files}
%license LICENSE
%doc Readme.md
%{_bindir}/ldapdomaindump
%{_bindir}/ldd2bloodhound
%{_bindir}/ldd2pretty

%changelog
* Sun Dec 17 2023 Michal Ambroz <rebus@seznam.cz> - 0.9.4-1
- Initial package.
