%define debug_package %{nil}

Name: libevtx
Version: 20160421
Release: 1%{?dist}
Summary: Library to access the Windows XML Event Log (EVTX) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-alpha-%{version}.tar.gz
%if 0%{?centos} == 5
Patch1: %{name}-%{version}-patch-001
%endif
URL: http://code.google.com/p/libevtx/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libevtx is a library to access the Windows XML Event Log (EVTX) format

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
%if 0%{?centos} == 5
%patch1 -p1
%endif

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
%if 0%{?rhel} == 5
sed --in-place 's/^CC.*=.*gcc$/CC = gcc -std=c99/' pyevtx/Makefile
%endif
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libevtx.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/evtxexport
%attr(755,root,root) %{_bindir}/evtxinfo
%{_mandir}/man1/*

%files python
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%{_libdir}/python*/site-packages/*.a
%{_libdir}/python*/site-packages/*.la
%{_libdir}/python*/site-packages/*.so

%changelog
* Thu Apr 21 2016 Lawrence R. Rogers <lrr@cert.org> 20160421-1
* Release 20160421-1
	20160126
	* applied updates
	* worked on tests

	20160109
	* fixes for rpmbuild

* Thu Jan  7 2016 Lawrence R. Rogers <lrr@cert.org> 20160107-1
* Release 20160107-1
	20160107
	* worked on Python 3 support

* Sun Jan  3 2016 Lawrence R. Rogers <lrr@cert.org> 20160103-1
* Release 20160103-1
	20160103
	* 2016 update
	* Worked on format support

	20151221
	* applied updates

	20151206
	* updated libfwnt

	20151205
	* worked on Python bindings

* Mon Sep 28 2015 Lawrence R. Rogers <lrr@cert.org> 20150928-1
* Release 20150928-1
	20150929
	* updated m4 scripts
	* updated dependencies

	20150823
	* changed version for pypi repacking

	20150822
	* worked on setup.py

* Sat May 30 2015 Lawrence R. Rogers <lrr@cert.org> 20150105-2
* Release 20150105-2
	Libuna GCC-5 Patch

* Mon Jan  5 2015 Lawrence R. Rogers <lrr@cert.org> 20150105-1
* Release 20150105-1
	20150105
	* 2015 update

	20141229
	* updated dependencies
	* updated version for release

	20141228
	* updated dpkg files

	20141222
	* worked on Python 3 support

	20141220
	* worked on Python 3 support
	* worked on tests

	20141117
	* code clean up

* Mon Nov 12 2014 Lawrence R. Rogers <lrr@cert.org> 20141112-1
* Release 20141112-1
	20141112
	* changes to expose the event identifier qualifiers in the python bindings


* Sun Oct 26 2014 Lawrence R. Rogers <lrr@cert.org> 20141026-1
* Release 20141026-1
	20141026
	* changes for deployment

	20141019
	* changes for deployment

	20141009
	* updated dependencies and corresponding changes

	20141004
	* update Python-bindings tests

	20140929
	* removed README.macosx
	* changes for project site move

* Mon Sep  1 2014 Lawrence R. Rogers <lrr@cert.org> 20140901-01
* Release 20140901-1
	20140901
	* bug fix in Python-bindings

* Thu Jul 31 2014 Lawrence R. Rogers <lrr@cert.org> 20140731-01
* Release 20140731-1
	20140731
	* bug fix in Python-bindings

	20140723
	* worked on dpkg debug packages support

	20140531
	* updated msvscpp files

	20140530
	* updated dependencies
	* worked on Python-bindings
	* replaced PackageMaker for pkgbuild

	20140402
	* code clean up

	20140323
	* worked on Python-bindings

	20140317
	* updated dependencies
	* worked on setup.py
	* worked on Python-bindings

	20140210
	* added evtxexport man page

	20140131
	* removed examples

* Sun Jan 12 2014 Joachim Metz <joachim.metz@gmail.com> 20140112-1
- Auto-generated

