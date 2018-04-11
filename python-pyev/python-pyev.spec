Name:           python-pyev
Version:        0.9.0
License:        GPLv3+
Summary:        Python binding for the libev library
Group:          Development/Libraries
URL:            https://github.com/gabrielfalcao/pyev
#               https://code.google.com/archive/p/pyev/


%global         gituser         gabrielfalcao
%global         gitname         pyev
%global         gitdate         20130610
%global         commit          e31d13720916439038290d57d00ee3604298705f
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 7 )
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?fedora} <= 21
 %{!?py2_build:         %global py2_build       %{__python2} setup.py build --executable="%{__python2} -s"}
 %{!?py2_install:       %global py2_install     %{__python2} setup.py install -O1 --skip-build --root %{buildroot}}
 %{!?py3_build:         %global py3_build       %{__python3} setup.py build --executable="%{__python3} -s"}
 %{!?py3_install:       %global py3_install     %{__python3} setup.py install -O1 --skip-build --root %{buildroot}}
%endif

# Build source is github release=1 or git commit=0
%global         build_release    0

%if 0%{?build_release}  > 0
Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.1.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release



BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  libev-devel
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif # if with_python3

# html doc generation
BuildRequires:  python-sphinx


%description
Python binding for the libev library.
The libev is an event loop: you register interest in certain events (such
as a file descriptor being readable or a timeout occurring), and it will
manage these event sources and provide your program with events.



%package -n python2-%{gitname}
Summary:        Python2 binding for the libev library
Group:          Development/Libraries
%{?python_provide:%python_provide python2-%{gitname}}
# Provide also the upstream original name yara-python


%description -n python2-%{gitname}
The libev for Python2 wrapper - This is a Python extension that gives access
to libev library to be called from Python scripts.



%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{gitname}
Summary:        Python3 binding for the libev library
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}



%description -n python%{python3_pkgversion}-%{gitname}
The libev for Python3 wrapper - This is a Python extension that gives access
to libev library to be called from Python scripts.
%endif # with_python3

%prep
%if 0%{?build_release} > 0
# Build from git release version
%autosetup -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup  -n %{gitname}-%{commit}
%endif


%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # with_python3



%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif # with_python3


#check


%files -n python2-%{gitname}
#license LICENSE
%doc README.md
%{python2_sitearch}/%{gitname}*

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{gitname}
#license LICENSE
%doc README.md
%{python3_sitearch}/%{gitname}*
%endif # with_python3


%changelog
* Wed Mar 21 2018 Michal Ambroz <rebus at, seznam.cz> - 0.9.0-0.1
- initial package for Fedora

