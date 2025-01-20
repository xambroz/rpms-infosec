# Created by pyp2rpm-3.3.10
%global pypi_name ldaptor
%global pypi_version 21.2.0

Name:           python-ldaptor
Version:        21.2.0
Release:        %autorelease
Summary:        A Pure-Python Twisted library for LDAP

License:        MIT
URL:            https://github.com/twisted/ldaptor
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(alabaster) >= 0.7.12
BuildRequires:  python3dist(commonmark) >= 0.9.1
BuildRequires:  python3dist(docutils) >= 0.16
BuildRequires:  python3dist(mock) >= 4
BuildRequires:  python3dist(passlib)
BuildRequires:  python3dist(pillow) >= 7.2
BuildRequires:  python3dist(pyparsing)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six) >= 1.7
BuildRequires:  python3dist(sphinx) >= 3.2
BuildRequires:  python3dist(sphinx-rtd-theme) >= 0.5
BuildRequires:  python3dist(twisted) >= 15.5
BuildRequires:  python3dist(sphinx)

%global _description %{expand:
 .. image::
}

%description %_description


%package -n     python%{python3_pkgversion}-ldaptor
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-ldaptor}

Requires:       python3dist(alabaster) >= 0.7.12
Requires:       python3dist(commonmark) >= 0.9.1
Requires:       python3dist(docutils) >= 0.16
Requires:       python3dist(mock) >= 4
Requires:       python3dist(passlib)
Requires:       python3dist(pillow) >= 7.2
Requires:       python3dist(pyparsing)
Requires:       python3dist(setuptools)
Requires:       python3dist(six) >= 1.7
Requires:       python3dist(sphinx-rtd-theme) >= 0.5
Requires:       python3dist(twisted) >= 15.5
%description -n python%{python3_pkgversion}-ldaptor
 .. image::

%package -n python-ldaptor-doc
Summary:        ldaptor documentation
%description -n python-ldaptor-doc
Documentation for ldaptor

%prep
%autosetup -n ldaptor-%{version}
# Remove bundled egg-info
rm -rf ldaptor.egg-info

%build
%pyproject_wheel
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install
%pyproject_save_files ldaptor

%check
%{__python3} setup.py test

%files -n python%{python3_pkgversion}-ldaptor -f %{pyproject_files}
%license LICENSE
%doc README.rst docs/source/examples/addressbook/README.txt
%{_bindir}/ldaptor-fetchschema
%{_bindir}/ldaptor-find-server
%{_bindir}/ldaptor-getfreenumber
%{_bindir}/ldaptor-ldap2dhcpconf
%{_bindir}/ldaptor-ldap2dnszones
%{_bindir}/ldaptor-ldap2maradns
%{_bindir}/ldaptor-ldap2passwd
%{_bindir}/ldaptor-ldap2pdns
%{_bindir}/ldaptor-ldifdiff
%{_bindir}/ldaptor-ldifpatch
%{_bindir}/ldaptor-namingcontexts
%{_bindir}/ldaptor-passwd
%{_bindir}/ldaptor-rename
%{_bindir}/ldaptor-search
%{python3_sitelib}/ldaptor
%{python3_sitelib}/ldaptor-%{version}-py%{python3_version}.egg-info

%files -n python-ldaptor-doc -f %{pyproject_files}
%doc html
%license LICENSE

%changelog
%{?%autochangelog: %autochangelog }
