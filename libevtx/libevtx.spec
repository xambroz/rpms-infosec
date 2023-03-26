Name:           libevtx
Version:        20221101
Summary:        Library to access the Windows XML Event Log (EVTX) format
Group:          System Environment/Libraries
License:        LGPLv3+
URL:            https://github.com/libyal/libevtx/
%global         baserelease     1

%global         common_description %{expand:
libevtx is a library to access the Windows XML Event Log (EVTX) format
Part of Joachim Metz's libyal set of forensics tools and libraries.
}

%global         gituser         libyal
%global         gitname         libevtx
%global         gitdate         20221101
%global         commit          58e44893ceeaca57dff7380d0f7110caf660b92d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Build with python2 support for RHEL7
%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%bcond_without  python2
%global         pythonopts      -enable-python2
%endif


%if 0%{?fedora}
%bcond_without  python3
%global         pythonopts      -enable-python3
%endif

%if %{with python2} && %{with python3}
%global         pythonopts      -enable-python2 -enable-python3
%endif


# By default build from a release tarball.
# If you want to rebuild from a unversioned commit from git do that with.
# rpmbuild --rebuild libevtx.src.rpm --without release
%bcond_without  release


# Build from git release version
%if %{with release}
Release:       %{baserelease}.alpha%{?dist}
Source0:       https://github.com/%{gituser}/%{gitname}/releases/download/%{version}/%{name}-alpha-%{version}.tar.gz
%else
# Build from git commit baseline
Release:       0.%{baserelease}.%{gitdate}git%{shortcommit}%.alpha.%{?dist}
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif


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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
* Tue Jun 27 2017 Michal Ambroz <rebus _AT seznam.cz> 20160421-2.alpha
- clean-up for Fedora

* Thu Apr 21 2016 Lawrence R. Rogers <lrr@cert.org> 20160421-1
- applied updates
- worked on tests
- 20160109 fixes for rpmbuild

* Thu Jan  7 2016 Lawrence R. Rogers <lrr@cert.org> 20160107-1
- worked on Python 3 support

* Sun Jan  3 2016 Lawrence R. Rogers <lrr@cert.org> 20160103-1
- Worked on format support
- updated libfwnt
- worked on Python bindings

* Mon Sep 28 2015 Lawrence R. Rogers <lrr@cert.org> 20150928-1
- updated m4 scripts
- updated dependencies
- changed version for pypi repacking
- worked on setup.py

* Sat May 30 2015 Lawrence R. Rogers <lrr@cert.org> 20150105-2
- Libuna GCC-5 Patch

* Mon Jan  5 2015 Lawrence R. Rogers <lrr@cert.org> 20150105-1
- updated dependencies
- updated version for release
- worked on Python 3 support
- worked on tests
- code clean up

* Wed Nov 12 2014 Lawrence R. Rogers <lrr@cert.org> 20141112-1
- changes to expose the event identifier qualifiers in the python bindings

* Sun Oct 26 2014 Lawrence R. Rogers <lrr@cert.org> 20141026-1
- changes for deployment
- updated dependencies and corresponding changes
- update Python-bindings tests
- removed README.macosx
- changes for project site move

* Mon Sep  1 2014 Lawrence R. Rogers <lrr@cert.org> 20140901-01
- bug fix in Python-bindings

* Thu Jul 31 2014 Lawrence R. Rogers <lrr@cert.org> 20140731-01
- bug fix in Python-bindings
- updated msvscpp files
- updated dependencies
- worked on Python-bindings
- replaced PackageMaker for pkgbuild
- code clean up
- worked on setup.py
- worked on Python-bindings
- added evtxexport man page
- removed examples

* Sun Jan 12 2014 Joachim Metz <joachim.metz@gmail.com> 20140112-1
- Auto-generated

