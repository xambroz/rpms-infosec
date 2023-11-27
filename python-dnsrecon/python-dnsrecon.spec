Name:           python-dnsrecon
Version:        1.1.5
License:        GPL-2.0-only
%global         baserelease     1
Summary:        DNS reconnaissance tool
URL:            https://github.com/darkoperator/dnsrecon
VCS:            https://github.com/darkoperator/dnsrecon
#               https://github.com/darkoperator/dnsrecon/releases


%bcond_without  release


%global         gituser         darkoperator
%global         gitname         dnsrecon
%global         gitdate         20230722
%global         commit          6ba17dae59f0640feac319c0d282f274861e73b1
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


%if %{with release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %{baserelease}.git%{gitdate}.%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-cov
Requires:       python%{python3_pkgversion}-hexdump

%global common_description %{expand:
Pure Python parser for recent Windows Event Log files (those with the file
extension ".recon"). The module provides programmatic access to the File
and Chunk headers, record templates, and event entries. For example, you
can use python-dnsrecon to review the event logs of Windows 7 systems from a Mac
or Linux workstation. The structure definitions and parsing strategies were
heavily inspired by the work of Andreas Schuster and his Perl implementation
"Parse-dnsrecon".
}

%description
%common_description


%package -n python%{python3_pkgversion}-dnsrecon
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-dnsrecon}
Provides:       dnsrecon

%description -n python%{python3_pkgversion}-dnsrecon
%common_description


%prep
%if %{with release}
%autosetup -n dnsrecon-%{version}
%else
%autosetup -n dnsrecon-%{commit}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

# Use the configuration globally
mv %{buildroot}%{python3_sitelib}/etc %{buildroot}/



# Not working
# %%pyproject_save_files dnsrecon python_dnsrecon


%files -n python%{python3_pkgversion}-dnsrecon
%license LICENSE
%doc README.md
%{python3_sitelib}/dnsrecon
%{python3_sitelib}/dnsrecon-*.dist-info
%{_bindir}/dnsrecon
%{_sysconfdir}/dnsrecon

%changelog
* Mon Nov 27 2023 Michal Ambroz <rebus _AT seznam.cz> - 1.1.5-1
- Initial package for Fedora
