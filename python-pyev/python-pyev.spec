Name:           python-pyev
Version:        0.9.0
%global         baserelease    14
License:        GPL-3.0-or-later
Summary:        Python binding for the libev library
URL:            https://github.com/gabrielfalcao/pyev
#               https://code.google.com/archive/p/pyev/
%if 0%{?rhel}
Group:          Development/Libraries
%endif


%global         gituser         gabrielfalcao
%global         gitname         pyev
%global         gitdate         20130610
%global         commit          e31d13720916439038290d57d00ee3604298705f
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# By default build with python3
%bcond_without python3

# By default build without python2
%bcond_with    python2

# Build python2 only on EPEL7
%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_without    python2
%endif

# By default build from the lates git snapshot, untill the upstream comes with the new release
%bcond_with release_tag

%if %{with release_tag}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1817984
# Reported upstream as PR #2: https://github.com/gabrielfalcao/pyev/pull/2
# Python Version 3.9 brought new function PyModule_AddType, which collides with the name/purpose of
# the PyModule_AddType in this package. Renaming it in this package to PyModule_Utils_AddType
Patch0:         https://github.com/gabrielfalcao/pyev/pull/2.patch#/python-pyev-addtype-collision.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  libev-devel

%if %{with python2}
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# if with_python3
%endif

# html doc generation
BuildRequires:  /usr/bin/sphinx-build


%description
Python binding for the libev library.
The libev is an event loop: you register interest in certain events (such
as a file descriptor being readable or a timeout occurring), and it will
manage these event sources and provide your program with events.



%if %{with python2}
%package -n python2-%{gitname}
Summary:        Python2 binding for the libev library
Group:          Development/Libraries
%{?python_provide:%python_provide python2-%{gitname}}
# Provide also the upstream original name yara-python

%description -n python2-%{gitname}
The libev for Python2 wrapper - This is a Python extension that gives access
to libev library to be called from Python scripts.
%endif



%if %{with python3}
%package -n python%{python3_pkgversion}-%{gitname}
Summary:        Python3 binding for the libev library
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}



%description -n python%{python3_pkgversion}-%{gitname}
The libev for Python3 wrapper - This is a Python extension that gives access
to libev library to be called from Python scripts.
# with_python3
%endif

%prep
%if %{with release_tag}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif


%build
%if %{with python2}
%py2_build
%endif

%if 0%{?with_python3}
%py3_build
%endif


%install
%if %{with python2}
%py2_install
%endif

%if %{with python3}
%py3_install
%endif


#check

%if %{with python2}
%files -n python2-%{gitname}
#license LICENSE
%doc README.md
%{python2_sitearch}/%{gitname}*
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{gitname}
#license LICENSE
%doc README.md
%{python3_sitearch}/%{gitname}*
%endif


%changelog
* Sun May 23 2021 Michal Ambroz <rebus at, seznam.cz> - 0.9.0-0.14.20130610gite31d137
- modernize specfile

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.13.20130610gite31d137
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.12.20130610gite31d137
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.11.20130610gite31d137
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-0.10.20130610gite31d137
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.9.20130610gite31d137
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-0.8.20130610gite31d137
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.7.20130610gite31d137
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.6.20130610gite31d137
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-0.5.20130610gite31d137
- Don't BR python2

* Wed Oct 10 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-0.4.20130610gite31d137
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-0.3.20130610gite31d137
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-0.2.20130610gite31d137
- Rebuilt for Python 3.7

* Wed Mar 21 2018 Michal Ambroz <rebus at, seznam.cz> - 0.9.0-0.1
- initial package for Fedora

