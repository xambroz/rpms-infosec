%global         gituser         libyal
%global         gitname         libevtx
%global         commit          58e44893ceeaca57dff7380d0f7110caf660b92d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         pythonopts      -enable-python2

%if 0%{?fedora}
%global         with_python3    1
%global         pythonopts      -enable-python2 --enable-python3
%endif


Name:           libevtx
Version:        20160421
Release:        1.alpha%{?dist}
Summary:        Library to access the Windows XML Event Log (EVTX) format
Group:          System Environment/Libraries
License:        LGPLv3+
URL:            https://github.com/libyal/libevtx/
Source:         https://github.com/%{gituser}/%{gitname}/releases/download/%{version}/%{name}-alpha-%{version}.tar.gz

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3


%description
libevtx is a library to access the Windows XML Event Log (EVTX) format
Part of Joachim Metz's libyal set of forensics tools and libraries.

%package devel
Summary: Header files and libraries for developing applications for libevtx
Group: Development/Libraries
Requires: libevtx = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libevtx.

%package tools
Summary: Several tools for reading Windows XML Event Log (EVTX) files
Group: Applications/System
Requires: libevtx = %{version}-%{release}

%description tools
Several tools for reading Windows XML Event Log (EVTX) files

%package python
Summary: Python bindings for libevtx
Group: System Environment/Libraries
Requires: libevtx = %{version}-%{release} python
BuildRequires:  %(basename %{__python})-devel

%description python
Python bindings for libevtx

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} %{pythonopts}
%make_build

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

#Fedora not shipping static libraries
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete


%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%doc AUTHORS COPYING NEWS README ChangeLog
%{_libdir}/*.so
%{_libdir}/pkgconfig/libevtx.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%doc AUTHORS COPYING NEWS README
%{_bindir}/evtxexport
%{_bindir}/evtxinfo
%{_mandir}/man1/*

%files python
%doc AUTHORS COPYING NEWS README
%{_libdir}/python*/site-packages/*.so

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

