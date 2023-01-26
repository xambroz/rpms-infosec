# Created by pyp2rpm-3.3.8
%global pypi_name dkimpy
%global pypi_version 1.0.5

Name:           python-%{pypi_name}
Version:        1.0.5
Release:        1%{?dist}
Summary:        DKIM (DomainKeys Identified Mail), ARC (Authenticated Receive Chain), and TLSRPT (TLS Report) email signing and verification

License:        BSD-like
URL:            https://launchpad.net/dkimpy
# Source0:        %%{pypi_source}
Source0:        https://launchpad.net/dkimpy/1.0/%{version}/+download/dkimpy-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(aiodns)
BuildRequires:  python3dist(authres)
BuildRequires:  python3dist(authres)
BuildRequires:  python3dist(py3dns)
BuildRequires:  python3dist(pynacl)
BuildRequires:  python3dist(pynacl)
BuildRequires:  python3dist(setuptools)

%description
dkimpy - DKIM (DomainKeys Identified Mail) fork of: INTRODUCTIONdkimpy is a
library that implements DKIM (DomainKeys Identified Mail) email signing and
verification. Basic DKIM requirements are defined in RFC 6376: VERSIONThis is
dkimpy 1.0.5. REQUIREMENTSDependencies will be automatically included for
normal DKIM usage. The extras_requires feature 'ed25519' will add the
dependencies needed...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

Requires:       python3dist(aiodns)
Requires:       python3dist(authres)
Requires:       python3dist(authres)
Requires:       python3dist(py3dns)
Requires:       python3dist(pynacl)
Requires:       python3dist(pynacl)
Requires:       python3dist(setuptools)
%description -n python%{python3_pkgversion}-%{pypi_name}
dkimpy - DKIM (DomainKeys Identified Mail) fork of: INTRODUCTIONdkimpy is a
library that implements DKIM (DomainKeys Identified Mail) email signing and
verification. Basic DKIM requirements are defined in RFC 6376: VERSIONThis is
dkimpy 1.0.5. REQUIREMENTSDependencies will be automatically included for
normal DKIM usage. The extras_requires feature 'ed25519' will add the
dependencies needed...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test &&

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/arcsign
%{_bindir}/arcverify
%{_bindir}/dkimsign
%{_bindir}/dkimverify
%{_bindir}/dknewkey
%{python3_sitelib}/dkim
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_mandir}/man1/arcsign.1.gz
%{_mandir}/man1/arcverify.1.gz
%{_mandir}/man1/dkimsign.1.gz
%{_mandir}/man1/dkimverify.1.gz
%{_mandir}/man1/dknewkey.1.gz


%changelog
* Mon Dec 12 2022 Michal Ambroz <rebus@seznam.cz> - 1.0.5-1
- Initial package.
