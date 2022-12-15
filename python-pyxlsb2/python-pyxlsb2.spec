# with release - build from official release, otherwise build from git
%bcond_with     release

Name:           python-pyxlsb2
Version:        0.0.9
%global         baserelease     0.1
Summary:        Excel 2007+ Binary Workbook (xlsb) parser

License:        Apache License 2.0
URL:            https://github.com/DissectMalware/pyxlsb2
BuildArch:      noarch

%global         gituser         DissectMalware
%global         gitname         pyxlsb2
%global         commit          0a1ff1be329aa282ecbc347ff44fc6c07351685b
%global         gitdate         20220509
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%if %{with release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/%{gitname}_%{pkgver}/%{gitname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz#/%{name}-%{version}-%{gitdate}-%{shortcommit}.tar.gz
%endif




BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%description
pyxlsb2 (a variant of pyxlsb - is an Excel 2007+ Binary Workbook (xlsb) parser
written in Python.pyxslb2 offers the following improvements/changes in
comparison to pyxlsb:1. By default, keeps all data in memory instead of
creating temporary files. This is mainly to speed up the processing and also
not changing the local filesystem during the processing. 2. relies on both
"xl\\workbook.bin" and...

%package -n     python%{python3_pkgversion}-pyxlsb2

Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-pyxlsb2 }

%description -n python%{python3_pkgversion}-pyxlsb2
pyxlsb2 (a variant of pyxlsb - is an Excel 2007+ Binary Workbook (xlsb) parser
written in Python.pyxslb2 offers the following improvements/changes in
comparison to pyxlsb:1. By default, keeps all data in memory instead of
creating temporary files. This is mainly to speed up the processing and also
not changing the local filesystem during the processing. 2. relies on both
"xl\\workbook.bin" and...


%prep
%if %{with release}
%autosetup -n pyxlsb2-%{version}
%else
%autosetup -n pyxlsb2-%{commit}
%endif
# Remove bundled egg-info
rm -rf pyxlsb2.egg-info

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-pyxlsb2
%license LICENSE LICENSE_pyxlsb
%doc README.rst
%{python3_sitelib}/pyxlsb2
%{python3_sitelib}/pyxlsb2-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 14 2022 Michal Ambroz <rebus@seznam.cz> - 0.0.9-1
- Initial package.