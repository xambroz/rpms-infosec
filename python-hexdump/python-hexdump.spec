%global         hguser         techtonik
%global         srcname        hexdump
# 2016-08-18
%global         commit         66325cb5fed890df4a345e25ea8f107fd31b60d8
%global         commitdate     20160818
%global         shortcommit    %(c=%{commit}; echo ${c:0:12})


Name:           python-hexdump
Version:        3.4
Release:        0.2.%{commitdate}hg%{shortcommit}%{?dist}
Summary:        Dump binary data to hex format and restore from there

License:        Public Domain
#               https://pypi.python.org/pypi/hexdump
#               https://bitbucket.org/techtonik/hexdump
URL:            https://bitbucket.com/%{hguser}/%{srcname}
Source0:        https://bitbucket.org/%{hguser}/%{srcname}/get/%{shortcommit}.zip#/%{name}-%{version}-%{shortcommit}.zip
Source1:        hexdumpy.1

# Create the /usr/bin/hexdumpy
# https://bitbucket.org/techtonik/hexdump/pull-requests/5/modify-the-setuppy-in-order-to-generate/diff
Patch0:         %{name}-setup.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
Python library to dump binary data to hex format and restore from there



%package -n python2-%{srcname}
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Python library to dump binary data to hex format and restore from there



%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Python library to dump binary data to hex format and restore from there



%prep
%setup -q -n %{hguser}-%{srcname}-%{shortcommit}
%patch0 -p 1 -b .setup
sed -i -e 's|#!/usr/bin/env python|#|' hexdump.py


%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/hexdumpy.1

%files -n python2-%{srcname}
%license UNLICENSE
%doc README.txt
%{python2_sitelib}/*

%files -n python%{python3_pkgversion}-%{srcname}
%license UNLICENSE
%doc README.txt
%{python3_sitelib}/*
%{_bindir}/hexdumpy
%{_mandir}/man1/hexdumpy.1*



%changelog
* Wed Dec 13 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.4-0.1.20160818hg66325cb5fed8
- fixes during the package review, fix versioning, add manpage

* Wed Oct 04 2017 Michal Ambroz <rebus _AT seznam.cz> - 3.3-1
- Initial package for Fedora
