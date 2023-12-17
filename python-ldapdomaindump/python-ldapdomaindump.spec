# Created by pyp2rpm-3.3.10
%global pypi_name ldapdomaindump
%global pypi_version 0.9.4

Name:           python-ldapdomaindump
Version:        0.9.4
Release:        1%{?dist}
Summary:        Active Directory information dumper via LDAP

License:        MIT
URL:            https://github.com/dirkjanm/ldapdomaindump/
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%global _description %{expand:
}

%description %_description



%package -n     python%{python3_pkgversion}-ldapdomaindump
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-ldapdomaindump}

Requires:       python3dist(dnspython)
Requires:       python3dist(future)
Requires:       (python3dist(ldap3) >= 2.5 with (python3dist(ldap3) < 2.6 or python3dist(ldap3) > 2.6) with (python3dist(ldap3) < 2.5.2 or python3dist(ldap3) > 2.5.2) with (python3dist(ldap3) < 2.5 or python3dist(ldap3) > 2.5))
%description -n python%{python3_pkgversion}-ldapdomaindump



%prep
%autosetup -n ldapdomaindump-%{version}
# Remove bundled egg-info
rm -rf ldapdomaindump.egg-info

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
