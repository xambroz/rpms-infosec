Name:           libevtx
Version:        20240504
Summary:        Library to access the Windows XML Event Log (EVTX) format
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libevtx/
%global         baserelease     1

%global         common_description %{expand:
libevtx is a library to access the Windows XML Event Log (EVTX) format
Part of Joachim Metz's libyal set of forensics tools and libraries.
}

%global         gituser         libyal
%global         gitname         libevtx
%global         gitdate         20240504
%global         commit          d028b4f90886d467b2960b69084aa2485d7e218b
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Build with python2 support for RHEL7
%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%bcond_without  python2
%global         pythonopts      -enable-python2
%endif


%if 0%{?fedora}
%bcond_without  python3
%global         pythonopts      -enable-python
%endif

%if %{with python2} && %{with python3}
%global         pythonopts      -enable-python2 -enable-python
%endif


# By default build from a release tarball.
# If you want to rebuild from a unversioned commit from git do that with.
# rpmbuild --rebuild libevtx.src.rpm --without release
%bcond_without  release


# Build from git release version
%if %{with release}
Release:       %aurorelease
Source0:       https://github.com/%{gituser}/%{gitname}/releases/download/%{version}/%{name}-alpha-%{version}.tar.gz
%else
# Build from git commit baseline
Release:       %aurorelease
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif


BuildRequires:  gcc
BuildRequires:  make

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif


%description
%{common_description}

%package devel
Summary: Header files and libraries for developing applications for libevtx
Group: Development/Libraries
Requires: libevtx = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libevtx.
%{common_description}

%package tools
Summary: Several tools for reading Windows XML Event Log (EVTX) files
Group: Applications/System
Requires: libevtx = %{version}-%{release}

%description tools
Several tools for reading Windows XML Event Log (EVTX) files
%{common_description}

%if %{with python2}
%package python2
Summary: Python2 bindings for libevtx
Group: System Environment/Libraries
Requires: libevtx = %{version}-%{release} python2

%description python2
The python2 bindings for libevtx
%{common_description}
%endif


%if %{with python3}
%package python%{python3_pkgversion}
Summary: Python bindings for libevtx
Group: System Environment/Libraries
Requires: libevtx = %{version}-%{release} python%{python3_pkgversion}

%description python%{python3_pkgversion}
The python3 bindings for libevtx
%{common_description}
%endif

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} %{pythonopts}
%make_build

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

#Fedora not shipping static libraries
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/*.so.*

%files devel
%license COPYING
%{_libdir}/*.so
%{_libdir}/pkgconfig/libevtx.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%license COPYING
%{_bindir}/evtxexport
%{_bindir}/evtxinfo
%{_mandir}/man1/*

%if %{with python2}
%files python2
%license COPYING
%{python2_sitearch}/pyevtx.so
%endif

%if %{with python3}
%files python3
%license COPYING
%{python3_sitearch}/pyevtx.so
%endif

%changelog
%autochangelog
