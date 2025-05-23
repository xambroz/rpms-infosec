%define debug_package %{nil}
%if 0%{?centos} == 6
%global         with_python2 1
%endif

Summary:	snarf - Structured Network Alert Reporting Framework
Name:		snarf
Version:	0.3.0
Release:	3%{?dist}
Group:		Applications/System
License:	LGPLv2
Source:		snarf-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
URL:		http://tools.netsa.cert.org/snarf
Vendor:		CERT Network Situational Awareness <netsa-help@cert.org>
Provides:	libsnarf = %{version}
Requires:	glib2 >= 2.22
Requires:	protobuf >= 2.3.0
Requires:	protobuf-c >= 1.0.1
Requires:	libyaml
BuildRequires:	pkgconfig >= 0.8
BuildRequires:	glib2-devel > 2.10
BuildRequires:	protobuf-c-devel 
%if 0%{?fedora} >= 26
Requires:	zeromq >= 3.0.0
BuildRequires:	zeromq-devel
%else
Requires:	zeromq3 >= 3.0.0
BuildRequires:	zeromq3-devel
%endif
BuildRequires:	libyaml-devel
BuildRequires:	sendmail
BuildRequires:	doxygen
BuildRequires:	automake

%description
snarf is a distributed alert reporting system. Applications can use snarf's C
and Python APIs to construct and send network alert messages, which can then be
routed to multiple destinations in a configurable manner.

%package devel
Summary: Static libraries and C header files for libsnarf
Group: Development/Libraries
Provides: libsnarf-devel = %{version}
Requires: %{name} = %{version}
Requires: pkgconfig >= 1:0.8

%description devel
Static libraries and C header files for libsnarf.

%if 0%{?with_python2}
%package -n snarf-python
Summary: Python interface to snarf
Group: Development/Libraries
Provides: snarf-python = %{version}
Requires: python >= 2.4
Requires: netsa-python >= 1.3
BuildRequires: netsa-python >= 1.3
%if 0%{?rhel} == 5
BuildRequires:	python26-zmq
%else
%if 0%{?centos} == 8
BuildRequires:	zmq
%else
BuildRequires:	python2-zmq
%endif
%endif

%description -n snarf-python
Python interface to snarf
%endif

%prep
%setup -q -n %{name}-%{version}

%build
%if 0%{?rhel} == 5
PYTHON=python2
export PYTHON
%endif
%configure \
    %{?_with_python} %{?_without_python}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make DESTDIR=%{?buildroot:%{buildroot}} install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
mv $RPM_BUILD_ROOT/%{_datadir}/snarf/snarfd.sysconfig $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/snarfd
mv $RPM_BUILD_ROOT/%{_datadir}/snarf/snarfd.init.d $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/snarfd
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la

################################################################################################################
# Fix the Shebang problem for Python2 executables
################################################################################################################
for s in %{buildroot}%{_bindir}/*
do
	file $s | grep -q -i 'python script' && sed --in-place '1s=python[^2]*=python2=' $s
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{name}
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README.rst dstat_snarf.py
%{_libdir}/libsnarf*.so*
%{_bindir}/snarfd
%{_bindir}/snarfc
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%dir %{_datadir}/snarf
%{_datadir}/snarf/*
%config(noreplace) %{_sysconfdir}/sysconfig/snarfd
%attr(755,root,root) %{_sysconfdir}/init.d/snarfd
%doc %{name}-%{version}.pdf AUTHORS COPYING NEWS README.rst

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsnarf*.a
%{_libdir}/pkgconfig/*

%if 0%{?with_python2}
%files -n snarf-python
%defattr(-, root, root)
%dir %{_prefix}/lib/python?.?/site-packages/snarf
%{_prefix}/lib/python?.?/site-packages/snarf*
%{_bindir}/*.py
%endif

%changelog
* Thu Mar  9 2017 Lawrence R. Rogers <lrr@cert.org> 0.3.0-1
* Release 0.3.0-1
	ZeroMQ 3.x compatibility (no longer compatible with ZeroMQ 2.x)
	protobuf-c 1.0 compatibility (no longer compatible with protobuf-c 0.x)
	IPv6 address field support
	Bug fixes

* Mon Jul  6 2015 Lawrence R. Rogers <lrr@cert.org> 0.2.4-2
* Release 0.2.4-2
	Rebuilt for new version of zeromq.

* Tue Jan  6 2015 Lawrence R. Rogers <lrr@cert.org> 0.2.4-1
* Release 0.2.4-1
	Support non-flow ip address fields in alerts.
	Fix ZeroMQ compatibility problems, now requires ZeroMQ 2.2.x.
	Fix problem with certain GLib2 version / platform combinations.

* Fri Aug 22 2014 Lawrence R. Rogers <lrr@cert.org> 0.2.2-3
* Release 0.2.2-3
	Rebuild to eliminate protobuf-c-devel as a run time dependency (this was an error).

* Wed Aug 20 2014 Lawrence R. Rogers <lrr@cert.org> 0.2.2-2
* Release 0.2.2-2
	Rebuilt to use the lastest libprotobuf-c.so.0

* Wed Jul 3 2013 Lawrence R. Rogers <lrr@cert.org> 0.2.2-1
* Release 0.2.2-1
	Initial release to open source community.
	Additional documentation.
	Bug fixes.

* Tue Feb 5 2013 Lawrence R. Rogers <lrr@cert.org> 0.2.1-1
* Release 0.2.1-1
	Add facility to reload snarf conf file when it's modified.
	Add basic channel statistics (alerts processed per channel) functionality
	Fix segfault when trying to print TCP flags for non-TCP protocols.

* Wed Aug 8 2012 Lawrence R. Rogers <lrr@cert.org> 0.2.0-1
* Release 0.2.0-1
	Move all hard-coded sink configuration into configuration file
	Documentation updates

* Thu Jun 14 2012 Lawrence R. Rogers <lrr@cert.org> 0.1.3-1
* Release 0.1.3-1
	Add sample Python script for writing IP sets
	Fix a couple of memory leaks

* Tue Jun 12 2012 Lawrence R. Rogers <lrr@cert.org> 0.1.3-1
* Release 0.1.2-1
	Add sample Python scripts for producing CEF and IODEF alerts
	Bug fixes

* Tue Jan 31 2012 Lawrence R. Rogers <lrr@cert.org> 0.1.1-1
* Release 0.1.1-1
	Add automated test suite.
	Improve documentation.
	Daemonize snarfd properly.
	Python API improvements.
	Various bug fixes.

* Fri Sep 30 2011 Lawrence R. Rogers <lrr@cert.org> 0.1.0-1
* Release 0.1.0-1
	Initial release of the snarf suite.
