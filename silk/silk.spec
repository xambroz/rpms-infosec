%bcond_with libipa

%if 0%{?centos}0%{?amzn} == 70
%define python3_pkgversion 36
%endif

%define debug_package %{nil}

%define name    silk
%define version 3.19.2

%define Testing 0
%{?_with_Testing:%define Testing 1}

%if %{Testing}
%if %{with libipa}
	%define release 102
%else
	%define release 101
%endif
%else
%if %{with libipa}
	%define release 2
%else
	%define release 1
%endif
%endif

Name:			silk
Version:		%{version}
Release:		%{release}%{?dist}
Summary:		SiLK: A network flow collection and analysis package
License:		GPLv2
Vendor:			CERT Network Situational Awareness <netsa-help@cert.org>
URL:			http://tools.netsa.cert.org/silk/
Source:			%{name}-%{version}.tar.gz
Group:			Applications/System
Prefix:			/usr
Requires:		adns
BuildRequires:		adns-devel
Requires:		libfixbuf >= 1.0.0 gnutls >= 1.4.1 lzo libpcap zlib
Requires(post):		/sbin/ldconfig, /sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(postun):	/sbin/ldconfig
Requires:		filesystem
BuildRequires:		libfixbuf-devel >= 1.0.0 gnutls-devel >= 1.4.1 lzo-devel libpcap-devel zlib-devel
BuildRequires:		libselinux
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if 0%{?fedora} >= 19
BuildRequires:		perl-podlators
%endif
%if 0%{?fedora} >= 18
BuildRequires:		perl-Pod-Parser
%endif
%if %{with libipa}
%if 0%{?fedora} >= 17 || 0%{?centos} >= 7
%define PGSQL_BASE		%{prefix}
%define PGSQL_PKG_CONFIG        %{PGSQL_BASE}/bin/pkg-config
%define PGSQL_PKG_CONFIG_FILE   %{_libdir}/pkgconfig/libpq.pc
%define IPA_PKG_CONFIG_FILE     %{_libdir}/pkgconfig/libipa.pc
BuildRequires:			postgresql-devel libipa-devel
Requires:       		postgresql-libs  libipa
BuildRequires:			python%{python3_pkgversion}-devel 
Requires:			python%{python3_pkgversion}
%endif
%endif

BuildRequires:			python%{python3_pkgversion} python%{python3_pkgversion}-devel
BuildRequires:			snappy-devel

# To apply a patch to the SiLK sources: (1)put the patch file into the
# SOURCES directory, (2)uncomment the 'Patch0:' line below, (3)add the
# name of the patch file after the 'Patch0:', (4)uncomment the
# '%patch0' line in the 'prep' section below.
#
# To apply a second patch, repeat the process using 'Patch1:' and
# '%patch1' in place of 'Patch0:' and '%patch0'.
#
#Patch0:
#Patch1:
#Patch2:
#Patch3:
#Patch4:

%define data_rootdir    /data
%define with_PYTHON     1
%ifarch x86_64
%define py_sitepkg      %{nil}%{python3_sitearch}
%define py_sitepkg_silk %{nil}%{python3_sitearch}/silk
%endif

# This file contains the list of files that comprise the silk-analysis
# RPM.  It is created during the 'install' phase.
%define sk_analysis_file   analysis-list.txt
%define sk_analysis_path   $RPM_BUILD_DIR/%{name}-%{version}/%{sk_analysis_file}

# This file is empty or contains the list of packing-logic plug-ins
# for the silk-rwflopack RPM.  It is created during 'install'.
%define sk_rwflowpack_file rwflowpack-list.txt
%define sk_rwflowpack_path $RPM_BUILD_DIR/%{name}-%{version}/%{sk_rwflowpack_file}

#######################################################################
# RCSIDENT("$SiLK: silk.spec.in d298f6bb5a90 2013-05-31 21:16:48Z mthomas $")
#######################################################################

%description
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

SiLK consists of two sets of tools: a packing system and analysis
suite. The packing system receives network flow information from
Netflow v5 or any IPFIX-based flowmeter and converts them into a more
space efficient format, recording the packed records into
service-specific, binary flat files. The analysis suite consists of
tools which can read these flat files and then perform various query
operations, ranging from per-record filtering to statistical analysis
of groups of records. The analysis tools interoperate using pipes,
allowing a user to develop a relatively sophisticated query from a
simple beginning.

%prep
echo Building %{name}-%{version}-%{release}
%setup -q
#
# To apply patches, see description near 'Patch0:' above.
#
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1

%build
%if %{with libipa}
export LIBIPA_CFLAGS="%(echo `if [ -e %{PGSQL_PKG_CONFIG_FILE} ]; then %{PGSQL_PKG_CONFIG} --cflags libpq; fi; if [ -e %{IPA_PKG_CONFIG_FILE} ]; then pkg-config --cflags libipa; fi`)"
export LIBIPA_LIBS="%(  echo `if [ -e %{PGSQL_PKG_CONFIG_FILE} ]; then %{PGSQL_PKG_CONFIG} --libs   libpq; fi; if [ -e %{IPA_PKG_CONFIG_FILE} ]; then pkg-config --libs   libipa; fi`)"
echo LIBIPA_CFLAGS=$LIBIPA_CFLAGS LIBIPA_LIBS==$LIBIPA_LIBS=
%endif
%configure --enable-data-rootdir=%{data_rootdir}  --disable-assert --enable-asa-zero-packet-hack --enable-ipv6 --enable-output-compression=lzo1x --without-c-ares \
	%{?_with_libipa} --with-python=python3 --disable-static --enable-ipset-compatibility
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
	make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
mv $RPM_BUILD_ROOT/%{_datadir}/silk/etc/*.conf $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
for sk_initd in $RPM_BUILD_ROOT/%{_datadir}/silk/etc/init.d/* ; do \
    sed 's,^\(DEFAULT_SCRIPT_CONFIG_LOCATION=\),\1%{_sysconfdir}/sysconfig,' $sk_initd > /$RPM_BUILD_ROOT/%{_sysconfdir}/init.d/`basename $sk_initd` ; \
    rm -f $sk_initd ; \
done
rmdir $RPM_BUILD_ROOT/%{_datadir}/silk/etc/init.d
rmdir $RPM_BUILD_ROOT/%{_datadir}/silk/etc
rm -f $RPM_BUILD_ROOT/%{_libdir}/silk/*.la
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/silk

# build the file list to use for the silk-analysis RPM
rm -f %{sk_analysis_path}
touch %{sk_analysis_path}
echo '%defattr(-,root,root)' >> %{sk_analysis_path}
echo '%{_datadir}/silk/addrtype-templ.txt' >> %{sk_analysis_path}

find $RPM_BUILD_ROOT/%{_bindir} -type f -print | \
    grep -v rwfileinfo | \
    grep -v rwsiteinfo | \
    grep -v silk_config | \
    sed "s!$RPM_BUILD_ROOT/*!/!" >> %{sk_analysis_path}
find $RPM_BUILD_ROOT/%{_mandir}/man1 -type f -print | \
    grep -v rwfileinfo | \
    grep -v rwsiteinfo | \
    grep -v silk_config | \
    sed "s!$RPM_BUILD_ROOT/*!/!" | \
    sed 's/$/*/' >> %{sk_analysis_path}
find $RPM_BUILD_ROOT/%{_mandir}/man3 -type f -print | \
    grep -v silk-plugin | \
    sed "s!$RPM_BUILD_ROOT/*!/!" | \
    sed 's/$/*/' >> %{sk_analysis_path}
find $RPM_BUILD_ROOT/%{_libdir}/silk -name '*.so' -type f -print | \
    grep -v packlogic | \
    sed "s!$RPM_BUILD_ROOT/*!/!" >> %{sk_analysis_path}

%if %{with_PYTHON}
rm -f $RPM_BUILD_ROOT/%{py_sitepkg_silk}/*.a
rm -f $RPM_BUILD_ROOT/%{py_sitepkg_silk}/*.la
# netsa_silk is packaged by netsa python
rm -f $RPM_BUILD_ROOT/%{py_sitepkg}/*.py* 
rm -f $RPM_BUILD_ROOT/%{py_sitepkg}/__pycache__/*.py* 
rmdir $RPM_BUILD_ROOT/%{py_sitepkg}/__pycache__
echo '%dir '%{py_sitepkg_silk} >> %{sk_analysis_path}
echo %{py_sitepkg_silk}'/*' >> %{sk_analysis_path}
%endif


# build the list of plug-ins to use as part of the silk-rwflowpack
# RPM.  This is empty if static packing logic is used.
rm -f %{sk_rwflowpack_path}
touch %{sk_rwflowpack_path}
find $RPM_BUILD_ROOT/%{_libdir}/silk -name 'packlogic*.so' -type f -print | \
    sed "s!$RPM_BUILD_ROOT/*!/!" >> %{sk_rwflowpack_path}

################################################################################################################
# Fix the Shebang problem for Python3 executables
################################################################################################################
for s in %{buildroot}%{_bindir}/*
do
	file $s | grep -q -i 'python script' && sed --in-place -e '1s=python[^2]*=python3=' -e '1s/python33/python3/' $s
done

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


#  ###################################################################
#  silk-common

%package common
Group: Applications/System
Summary: SiLK Toolset: Common Libraries and Configuration Files
%if %{with_PYTHON}
Provides: netsa_silk_impl
%endif

%description common
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-common package contains the libraries and configuration files
required by the other parts of SiLK Toolset, as well as generally
useful utilities.

%files common
%defattr(-,root,root)
%{_bindir}/rwfileinfo
%{_mandir}/man1/rwfileinfo.1*
%{_bindir}/rwsiteinfo
%{_mandir}/man1/rwsiteinfo.1*
%{_libdir}/*.so.*
%dir %{_libdir}/silk
%{_mandir}/man5/*
%{_mandir}/man7/*
%dir %{_datadir}/silk
%{_datadir}/silk/*-silk.conf
%{_datadir}/silk/silk.magic

%post common
/sbin/ldconfig

%postun common
/sbin/ldconfig


#  ###################################################################
#  silk-analysis

%package analysis
Group: Applications/System
Summary: SiLK Toolset: The Analysis Suite
Requires: silk-common

%description analysis
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-analysis package contains the analysis tools that query the
SiLK Flow data collected by rwflowpack (contained in the
silk-rwflowpack package) and summarize that data in various ways.

# The file list gets generated at install time.  This list contains
# almost everything except:
# -- packlogic-*.so files used by rwflowpack (silk-rwflowpack RPM)
# -- rwfileinfo (silk-common RPM)
# -- rwsiteinfo (silk-common RPM)
# -- silk_config (silk-devel RPM)
%files analysis -f %{sk_analysis_file}


#  ###################################################################
#  silk-rwflowpack

%package rwflowpack
Group: Applications/System
Summary: SiLK Toolset: The Packer
Requires: silk-common

%description rwflowpack
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-rwflowpack package converts NetFlow v5 or IPFIX (Internet
Protocol Flow Information eXport) data to the SiLK Flow record format,
categorizes each flow (e.g., as incoming or outgoing), and stores the
data in binary flat files within a directory tree, with one file per
hour-category-sensor tuple.  Use the tools from the silk-analysis
package to query this data.  rwflowpack may capture the data itself,
or it may process files that have been created by flowcap (see the
silk-flowcap package).

%files rwflowpack -f %{sk_rwflowpack_file}
%defattr(-,root,root)
%{_sbindir}/rwflowpack
%{_sbindir}/rwguess
%{_sbindir}/rwpackchecker
%dir %{_mandir}/man8
%{_mandir}/man8/rwflowpack.8*
%{_mandir}/man8/rwguess.8*
%{_mandir}/man8/rwpackchecker.8*
%config(noreplace) %{_sysconfdir}/sysconfig/rwflowpack.conf
%attr(755,root,root) %{_sysconfdir}/init.d/rwflowpack
%attr(750,root,root) %dir %{_localstatedir}/silk

%post rwflowpack
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

runlvl rwflowpack

%preun rwflowpack
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del rwflowpack
fi


#  ###################################################################
#  silk-flowcap

%package flowcap
Group: Applications/System
Summary: SiLK Toolset: Remote Flow Collection
Requires: silk-common

%description flowcap
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-flowcap package contains flowcap, a daemon to capture NetFlow
v5 or IPFIX flows (Internet Protocol Flow Information eXport), to
store the data temporarily in files on its local disk, and to forward
these files over the network to a machine where rwflowpack processes
the data.  flowcap is typically used with an rwsender-rwreceiver pair
to move the files across the network.

%files flowcap
%defattr(-,root,root)
%{_sbindir}/flowcap
%dir %{_mandir}/man8
%{_mandir}/man8/flowcap.8*
%config(noreplace) %{_sysconfdir}/sysconfig/flowcap.conf
%attr(755,root,root) %{_sysconfdir}/init.d/flowcap
%attr(750,root,root) %dir %{_localstatedir}/silk

%post flowcap
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

runlvl flowcap

%preun flowcap
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del flowcap
fi


#  ###################################################################
#  silk-rwflowappend

%package rwflowappend
Group: Applications/System
Summary: SiLK Toolset: Remote Data Storage Appending Daemon
Requires: silk-common

%description rwflowappend
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-rwflowappend package is used when the final storage location
of SiLK data files is on a different machine than that where the files
are created by the rwflowpack daemon (see the silk-rwflowpack
package).  rwflowappend watches a directory for SiLK data files and
appends those files to the final storage location where the SiLK
analysis tools (from the silk-analysis package) can process them.  To
move the files from rwflowpack to rwflowappend, an rwsender-rwreceiver
pair is typically used.

%files rwflowappend
%defattr(-,root,root)
%{_sbindir}/rwflowappend
%dir %{_mandir}/man8
%{_mandir}/man8/rwflowappend.8*
%config(noreplace) %{_sysconfdir}/sysconfig/rwflowappend.conf
%attr(755,root,root) %{_sysconfdir}/init.d/rwflowappend
%attr(750,root,root) %dir %{_localstatedir}/silk

%post rwflowappend
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

runlvl rwflowappend

%preun rwflowappend
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del rwflowappend
fi


#  ###################################################################
#  silk-rwreceiver

%package rwreceiver
Group: Applications/System
Summary: SiLK Toolset: File Transfer Receiver
Requires: silk-common

%description rwreceiver
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-rwreceiver package contains a program (rwreceiver) which
receives files over the network from one or more rwsender programs.
rwsender-rwreceiver pairs are used to move files from a machine
running flowcap and one running rwflowpack, or from the rwflowpack
machine to machine(s) running rwflowappend.

%files rwreceiver
%defattr(-,root,root)
%{_sbindir}/rwreceiver
%dir %{_mandir}/man8
%{_mandir}/man8/rwreceiver.8*
%config(noreplace) %{_sysconfdir}/sysconfig/rwreceiver.conf
%attr(755,root,root) %{_sysconfdir}/init.d/rwreceiver
%attr(750,root,root) %dir %{_localstatedir}/silk

%post rwreceiver
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

runlvl rwreceiver

%preun rwreceiver
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del rwreceiver
fi


#  ###################################################################
#  silk-rwsender

%package rwsender
Group: Applications/System
Summary: SiLK Toolset: File Transfer Sender
Requires: silk-common

%description rwsender
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-rwsender package contains a program (rwsender) which
transmits files over the network to one or more rwreceiver programs.
rwsender-rwreceiver pairs are used to move files from a machine
running flowcap and one running rwflowpack, or from the rwflowpack
machine to machine(s) running rwflowappend.

%files rwsender
%defattr(-,root,root)
%{_sbindir}/rwsender
%dir %{_mandir}/man8
%{_mandir}/man8/rwsender.8*
%config(noreplace) %{_sysconfdir}/sysconfig/rwsender.conf
%attr(755,root,root) %{_sysconfdir}/init.d/rwsender
%attr(750,root,root) %dir %{_localstatedir}/silk

%post rwsender
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

runlvl rwsender

%preun rwsender
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del rwsender
fi


#  ###################################################################
#  silk-rwpollexec

%package rwpollexec
Group: Applications/System
Summary: SiLK Toolset: Batch Command Executor
Requires: silk-common

%description rwpollexec
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-rwpollexec package contains a program (rwpollexec) which
monitors a directory for incoming files.  For each file, rwpollexec
executes a user-specified command.  If the command completes
successfully, the file is either moved to an archive directory or
deleted.

%files rwpollexec
%defattr(-,root,root)
%{_sbindir}/rwpollexec
%dir %{_mandir}/man8
%{_mandir}/man8/rwpollexec.8*
%config(noreplace) %{_sysconfdir}/sysconfig/rwpollexec.conf
%attr(755,root,root) %{_sysconfdir}/init.d/rwpollexec
%attr(750,root,root) %dir %{_localstatedir}/silk

%post rwpollexec
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

runlvl rwpollexec

%preun rwpollexec
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del rwpollexec
fi


#  ###################################################################
#  silk-devel

%package devel
Group: Development/Libraries
Summary: The SiLK Toolset development files

%description devel
SiLK, the System for Internet-Level Knowledge, is a collection of
traffic analysis tools developed by the CERT Network Situational
Awareness Team (CERT NetSA) to facilitate security analysis of large
networks. The SiLK tool suite supports the efficient collection,
storage and analysis of network flow data, enabling network security
analysts to rapidly query large historical traffic data sets. SiLK is
ideally suited for analyzing traffic on the backbone or border of a
large, distributed enterprise or mid-sized ISP.

The silk-devel package contains the development libraries and headers
for SiLK.  This package is required to build additional applications
or to build shared libraries for use as plug-ins to the SiLK analysis
tools.

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/*.so
%{_libdir}/*.la
%{_bindir}/silk_config
%{_mandir}/man1/silk_config.1*
%{_mandir}/man3/silk-plugin.3*


%changelog
%if %{Testing}
* Thu Mar 10 2022 2022 Lawrence R. Rogers <lrr@cert.org> 3.19.2-101/102
* Release 3.19.2-101/102
	Rebuilt with of libfixbuf 3.0.0.alpha1
%endif

* Thu Mar  3 2022 Lawrence R. Rogers <lrr@cert.org> 3.19.2-1/2
* Release 3.19.2-1/2
	PySiLK
		Fix compatibility with Python 3.9 and later.
	Building
		Add support for libfixbuf-3.0.0 (v1.7.0 and later are supported).
		When building with static packing-logic, include the appropriate configure flag in the generated silk.spec file.

* Mon Jan  4 2021 Lawrence R. Rogers <lrr@cert.org> 3.19.1-3/4
* Release 3.19.1-3/4
	Rebuilt for libfixbuf-2.4.1.

* Thu Apr 16 2020 Lawrence R. Rogers <lrr@cert.org> 3.19.1-1/2
* Release 3.19.1-1/2
	Add the SilkFile.skip() method to PySiLK.
	Fix PySiLK compatiblity with Python 3.7 and 3.8.
	Fix a compilation error when building SiLK without libfixbuf.

* Mon Oct 28 2019 Lawrence R. Rogers <lrr@cert.org> 3.19.0-3/4
* Release 3.19.0-3/4
	Bug fixes on 2019-10-24 release. Fixed in 2019-10-28 release.

* Thu Oct 24 2019 Lawrence R. Rogers <lrr@cert.org> 3.19.0-1/2
* Release 3.19.0-1/2
	rwaggbag, rwaggbagbuild, rwaggbagcat, rwaggbagtool
		Support using country codes as key fields.
	rwflowpack, flowcap
		Support a show-templates log-flag value in the sensors.conf file which enables printing of templates for specific probes.

* Thu Aug 29 2019 Lawrence R. Rogers <lrr@cert.org> 3.18.3-1/2
* Release 3.18.3-1/2
	Quiet a warning message when using libfixbuf-2.4.0.

* Thu May 23 2019 Lawrence R. Rogers <lrr@cert.org> 3.18.2-1/2
* Release 3.18.2-1/2
	Remove unintentionally-enabled debugging statements from rwflowpack.

* Fri Apr 19 2019 Lawrence R. Rogers <lrr@cert.org> 3.18.1-3/4
* Release 3.18.1-3/4
	Rebuilt for libfixbuf-2.3.1.

* Thu Mar 21 2019 Lawrence R. Rogers <lrr@cert.org> 3.18.1-1/2
* Release 3.18.1-1/2
	Add support for logging tombstone records created by YAF 2.11.

* Thu Dec 13 2018 Lawrence R. Rogers <lrr@cert.org> 3.18.0-1/2
* Release 3.18.0-1/2
	rwsetcat
		When --ip-format includes zero-padded and CIDR prefixes are being printed, also apply zero-padding to the prefix.
		Fix a bug when using --ip-format=decimal,zero-padded that caused an extra leading 0 to appear for IPv6 addresses.
	rwbagcat
		When --key-format includes zero-padded and CIDR prefixes are being printed, also apply zero-padding to the prefix.
		Fix a bug when using --key-format=decimal,zero-padded that caused an extra leading 0 to appear for IPv6 addresses.
	rwpmapcat, rwpmaplookup
		When --ip-format includes zero-padded and CIDR prefixes are being printed, also apply zero-padding to the prefix.
		Fix a bug when using --ip-format=decimal,zero-padded that caused an extra leading 0 to appear for IPv6 addresses.
		Fix a bug when using --ip-format=unmap-v6 where the prefix for IPs in the ::ffff:0:0/96 netblock was not adjusted to IPv4.
	rwcut, rwrecgenerator, rwstats, rwuniq
		Fix a bug when using --ip-format=decimal,zero-padded that caused an extra leading 0 to appear for IPv6 addresses.
	rwsender, rwreceiver
		Change optional TLS support to require GnuTLS-2.12.0 or later.
		Add a --tls-priority switch to set the priority (preference order) of ciphers, key exchange, etc.
		Add a --tls-security switch to set the security level of GnuTLS which determines cryptographic key sizes and security parameters.
		Add a --tls-crl switch to set a certificate revocation list.
		Add a --tls-debug-level to set the debugging level of GnuTLS.
		Not setting RWSENDER_TLS_PASSWORD/RWRECEIVER_TLS_PASSWORD is now treated as a NULL password, not an empty password.
		Exit with an error when any of the switches --tls-ca, --tls-cert, --tls-key, or --tls-pkcs12 are specified multiple times.
		Use GnuTLS's socket reading/writing functions instead of our own.
	rwflowpack
		Fix a bug that could cause rwflowpack to crash when multiple probes were processing IPFIX files.

* Tue Dec  4 2018 Lawrence R. Rogers <lrr@cert.org> 3.17.2-5/6
* Release 3.17.2-5/6
	Rebuilt for libfixbuf-2.2.0.

* Thu Jul 19 2018 Lawrence R. Rogers <lrr@cert.org> 3.17.2-3/4
* Release 3.17.2-3/4
	Rebuilt for libfixbuf-2.1.0.

* Thu Jun 28 2018 Lawrence R. Rogers <lrr@cert.org> 3.17.2-1/2
* Release 3.17.2-1/2
	rwgeoip2ccmap
		Add a --fields switch that gives the user control over which country-code value(s) are used when reading a GeoIP2 file.
	rwuniq
		Use a 64-bit integer for storing a bin's record count.
	rwstats
		Use a 64-bit integer for storing a bin's record count.
	rwaddrcount
		Use 64-bit integers for storing a bin's packet count and record count.
	rwflowpack
		In sensor.conf, add a new quirk, nf9-out-is-reverse, to simulate the behavior of libfixbuf-1.7.1; i.e., to treat the NetFlow v9 elements OUT_BYTES and OUT_PKTS as reverse-volume values.
		When parsing the sensor.conf file, allow double-quoted strings for the path names of IPset files.
	flowcap
		In sensor.conf, add a new quirk, nf9-out-is-reverse, to simulate the behavior of libfixbuf-1.7.1; i.e., to treat the NetFlow v9 elements OUT_BYTES and OUT_PKTS as reverse-volume values.

* Mon Apr 23 2018 Lawrence R. Rogers <lrr@cert.org> 3.17.1-1/2
* Release 3.17.1-1/2
	3.17.1
		Fix a compilation failure on RedHat EL6, CentOS 6, and other systems.
	3.17.0
		Add support in rwaggbagtool for removing rows when a value is above or below a threashold or when an 
			IP address is in or is not in an IPset.
		Change how rwsetcat displays IPv4 addresses in an IPset containing both IPv4 and IPv6 addresses.
		Add support for millisecond timestamps in rwuniq and rwstats.
		Add support for the GeoIP2 version of MaxMind's country code comma-separated value files and binary files.
			(Binary file support requires libmaxminddb library support.)

* Thu Feb 15 2018 Lawrence R. Rogers <lrr@cert.org> 3.16.1-1/2
* Release 3.16.1-1/2
	rwstats
		Fix a bug that occurred when using a large amount of memory and could result in corrupted output.
	rwuniq
		Fix a bug that occurred when using a large amount of memory and could result in corrupted output.
	rwbagcat
		Fix bugs that occur when using the --network-structure switch with an IPv4-specific argument and bag file contains addresses in the ::ffff:0:0/96 netblock.
	rwsetcat
		Print an error message when rwsetcat is unable to read an IPset.
	rwsender, rwreceiver
		Fix an issue when using installations of GnuTLS that do not provide support for thread locking.
	rwflowpack, flowcap
		Fix a bug where NetFlow v9 records were being ignored because the application was decoding them with the wrong internal template.
	Building
		Fix issues when determining compilation flags necessary for Python support.

* Thu Nov  9 2017 Lawrence R. Rogers <lrr@cert.org> 3.16.0-3/4
* Release 3.16.0-3/4
	Rebuilt with libfixbuf 1.8.0.

* Thu Jun 29 2017 Lawrence R. Rogers <lrr@cert.org> 3.16.0-1/2
* Release 3.16.0-1/2
	rwstats
		When the primary value is a distinct count, compute the number of distinct items across all bins and print each bin's percentage of the total distinct count.
		Fix bugs that may occur when computing distinct counts and not all distinct counts fit into memory.
	rwuniq
		Fix bugs that may occur when computing distinct counts and not all distinct counts fit into memory.
	flowrate plug-in
		Change how the flowrate plug-in handles flow records whose duration is zero in order to fix bizarre looking output in rwstats. The plug-in now assumes each of these flow records has a duration of 400 microseconds (0.4 milliseconds).
		Add the --flowrate-zero-duration switch which allows the user to set the duration that the plug-in uses for flow records whose given duration is zero.
	rwrandomizeip
		Read flow records from the standard input if the number of non-switch arguments is zero.
		Write the flow records to the standard output if the number of non-switch arguments is zero or one.
	rwswapbytes
		Read flow records from the standard input if the number of non-switch arguments is zero.
		Write the flow records to the standard output if the number of non-switch arguments is zero or one.
	rwflowpack, flowcap
		Change processing of NetFlow v9 records so that, when SiLK is compiled against libfixbuf 1.8.0, the OUT_BYTES and OUT_PKTS values are used when the IN_BYTES and IN_PKTS values are 0.
	flowcap
		Print the probe definitions to the log file when the log-level is set to debug.
	rwflowpack, rwflowappend, flowcap, rwsender, rwreceiver, rwpollexec
		Change how daemons invoke subprocesses in order to avoid creating subprocesses that deadlock and never complete.
		Modify start-up scripts to be more in line with the rules in the Linux Standard Base.
	Plug-ins
		Add manual pages for the cutmatch, conficker-c, and app-mismatch plug-ins.
		No longer install the uniq-distproto plug-in since its functionality is available as --values=distinct:protocol.

* Fri Mar 24 2017 Lawrence R. Rogers <lrr@cert.org> 3.15.0-1/2
* Release 3.15.0-1/2
	rwaggbag
		Create a new tool similar to rwbag: a tool to bin SiLK Flow records using a key and counter that support multiple fields and store the results in a binary Aggregate Bag file.
	rwaggbagbuild
		Create a new tool to create an Aggregate Bag file from text.
	rwaggbagcat
		Create a new tool to print the contents of an Aggregate Bag file as text.
	rwaggbagtool
		Create a new tool to manipulate binary Aggregate Bag files and create a new Aggregate Bag file.
	flowkey
		Add a new plug-in that uses the same algorithm as YAF to compute a 32-bit flow key hash.
	rwpmapcat
		Add the --output-path switch to specify the output file.
		POTENTIAL INCOMPATIBILITY. Note that the shortest unique prefix for the --output-type switch is now "--output-t".
	rwfileinfo
		Add the --xargs switch to read input file names from a file.
	rwsetcat
		Add the --output-path switch to specify the output file.
		Do not use the the pager when the output contains only the count of the number of IPs in a singe IPset.
	rwsiteinfo
		Add the --output-path switch to specify the output file.
	rwtuc
		Add the --xargs switch to read input file names from a file.
		Allow multiple fields in the input to be ignored.
		At shutdown, print the number of input lines that were not parsed unless --verbose is given or an error occurs.
		Remove the --bad-input-lines file when it is empty (in accordance with the manual page).
		Fix a bug that treated white space after the final delimiter as another field.
		Fix issues in parsing the title line when --fields is given.
	rwbagcat
		Add the --site-config-file switch to select the silk.conf file.
		Do not invoke the pager when --print-statistics is the only output and a destination argument is given to the switch.
	rwip2cc
		Do not use the pager when the --output-path switch is given.
	rwscanquery
		Fix a bug that prevented use of the SQLite database driver on a case-sensitive file system and caused "make check" to fail.
	Building
		Fix a compilation error in rwsiteinfo on Ubuntu.
		Remove support for fixbuf releases prior to libfixbuf-1.7.0.

* Thu Nov 17 2016 Lawrence R. Rogers <lrr@cert.org> 3.14.0-1/2
* Release 3.14.0-1/2
	IPset changes
		Add a new file format, record-version=5, for IPsets containing IPv6 addresses that should be more
		compact than record-version=4. Unless the default file format is changed at configure time, the new
		format must be explicitly requested using --record-version switch or via the SILK_IPSET_RECORD_VERSION
		environment variable.
		Fix a bug when working with IPsets that contain IPv6 addresses and have more than 44,739,242
		internal nodes. The bug may cause the tool to crash or to loop endlessly.
		Reduce how quickly memory grows when building an IPset that contains IPv6 addresses.
		Perform additional integrity checks when reading an IPset file from disk.
	rwsetbuild
		Fix a bug introduced in SiLK-3.11.0 that may occur when computing the intersection or difference of
		an IPv4 IPset with an IPv6 IPset that is in record-version=4 format. Addresses in the ::ffff:0:0/96
		netblock of the IPv6 IPset were ignored when the IPset contained clusters of addresses less then
		::ffff:0:0.
	rwsetcat
		Allow computing the count of IP addresses in an IPset without loading the IPset into memory.
	rwbag
		Fix a bug when creating a bag whose key is attributes that causes the bag to appear to have duplicate keys.
	rwfileinfo
		Rename the title of the compression field. The title was changed unintentionally in SiLK 3.12.2 and caused iSiLK to fail.
	rwstats, rwuniq
		Do not limit the maximum hash table size to a 32-bit value on a 64-bit platform.
	flowcap, rwflowpack
		In the sensor.conf file, add support for a quirk to handle NetFlow v9 records generated by a
		SonicWall device where the router up-time is reported in seconds instead of milliseconds.
	Building
		Add a configure switch, --enable-ipset-compatibility, that allows changing the default IPset
		file format written by SiLK. The argument is the version of SiLK with which IPsets are to be
		compatible. The IPset file format changes at 3.7.0 and 3.14.0.

* Thu Sep 29 2016 Lawrence R. Rogers <lrr@cert.org> 3.13.0-1/2
* Release 3.13.0-1/2
	Change across all tools
		Add support for compressing files with "Snappy" compression when the Snappy library and header are found during configuration.
		Add support for the SILK_COMPRESSION_METHOD environment variable that provides a default value for the --compression-method switch.
	rwcount
		Do not limit the maximum array size to a 32-bit value on 64-bit platforms.
	rwsettool
		Add a --symmetric-difference switch to compute the set of IP addresses that occur in only one of two input IPsets.
	rwfileinfo
		Disable printing of the record count when the file's compression method is not available.
	rwfilter, rwfglob
		Fix a file-selection bug where a --start-date specified in epoch seconds that fell on a day boundary would return files
		 for that entire day instead of for that single hour.
	PySiLK
		Fix memory leaks.
		Fix a bug in the silk.site.repository_iter() where an epoch-based start-date value that fell on a day boundary would
		 return files for that entire day instead of for that single hour.
	rwsender
		Change the log messages that are written when scanning the incoming and processing directories.

* Thu Jun 23 2016 Lawrence R. Rogers <lrr@cert.org> 3.12.2-1/2
* Release 3.12.2-1/2
	rwgeoip2ccmap
		Restore support for binary input that was removed in SiLK 3.12.0.
	rwbagcat
		Sort the output using the value of each key's counter when the --sort-counters switch is given.
	rwbag
		Copy the invocation history and the notes from the source files to the output file(s).
	rwbagtool
		When inverting a bag, set the key-type of the output to the counter-type of the input. Previously it was set to custom.
	rwfileinfo
		Add a --help-fields switch.
		Expand the description of rwfileinfo's output on the manual page.
	rwfilter, rwfglob, rwsiteinfo
		Fix an unexpected fatal error that would occur when the silk.conf file contained a class that did not contain any types.
		Check the validity of the silk.conf file and report such errors.
	rwipfix2silk
		Write additional log messages when --log-destination is specified.
	rwpdu2silk
		Write additional log messages when --log-destination is specified.
	rwflowpack
		Change when record counts are reported in the log file: Report the number of records written to each output file only when the files are flushed.
		Fix a bug processing the reverse side a YAF bi-flow that stored the egressInterface in both the input and output fields.
		Fix a bug processing a bi-flow record that reversed the vlan interfaces on the forward record.
	flowcap
		Fix a bug when processing the reverse side a YAF bi-flow that stored the egressInterface in both the input and output fields.
		Fix a bug processing a bi-flow record that reversed the vlan interfaces on the forward record.
	rwflowappend
		Add locking of incremental files to prevent multiple rwflowappend invocations from processing the same file.

* Thu May  5 2016 Lawrence R. Rogers <lrr@cert.org> 3.12.1-1/2
* Release 3.12.1-1/2
	rwbagcat
		Fix a bug where the pager was not invoked when displaying keys as IPs or integers.
	rwflowpack, flowcap
		Make substantial changes to the handling of IPFIX and NetFlow v9 records to decrease per-record processing time.

* Thu Mar 31 2016 Lawrence R. Rogers <lrr@cert.org> 3.12.0-1/2
* Release 3.12.0-1/2
	rwbag
		Add a new switch --bag-file that replaces the numerous bag creation switches that previously existed. Deprecate the previous bag creation switches.
		Expand the list of keys that rwbag supports (e.g., start-time, sensor, TCP flags).
		Add support for creating a bag that contains country codes.
		Add support for creating a bag whose key is derived from a prefix map that maps either IP-addresses or protocol-port pairs.
		Add a header to the Bag file that stores the command line used to create the file.
	rwbagcat
		POTENTIAL INCOMPATIBILITY. Display a key whose type represents a time using a human-readable timestamp. Using --key-format=epoch displays the integer value.
		POTENTIAL INCOMPATIBILITY. Display a key whose type represents a SiLK sensor using the the sensor name. Using --key-format=decimal displays the integer value.
		POTENTIAL INCOMPATIBILITY. Display a key whose type represents TCP flags using the standard FSRPAUEC letters. Using --key-format=decimal displays the integer value.
		POTENTIAL INCOMPATIBILITY. Display a key whose type represents SiLK attributes using the standard TCFS letters. Use --key-format=decimal to display the integer value.
		Display a key whose type represents a country code using the two letter abbreviation.
		Require a prefix map to be specified via the --pmap-file switch when attempting to display a key whose type represents a mapping from a prefix map. Require the type of the prefix map to match the key-type specified in the Bag.
		Allow the --key-format switch to accept time-formatting and timezone arguments when printing a key that represents a time. Exit with an error when a time-format is used on a Bag whose key-type is neither a time nor 'custom'.
		POTENTIAL INCOMPATIBILITY. Exit with an error when a --key-format for an IP address is used on a Bag whose key-type is neither an IP address nor 'custom'.
		POTENTIAL INCOMPATIBILITY. Exit with an error when the --network-structure switch is used on a Bag whose key-type is neither an IP address nor 'custom'.
		POTENTIAL INCOMPATIBILITY. Exit with an error when the --mask-ips switch is using on a Bag whose key-type is neither an IP address nor 'custom'.
	rwbagbuild
		Add support for creating a bag that contains country codes.
		Add support for creating a bag whose key is derived from a prefix map that maps either IP-addresses or protocol-port pairs.
		When mapping from a protocol-port pair to a prefix map value, allow the delimiter between the protocol and port to be different than that between the port and the counter.
		Add a header to the Bag file that stores the command line used to create the file.
	rwgeoip2ccmap
		Use the first line of input to determine whether to create an IPv4 or IPv6 country code map.
		Add a header to the Bag file that stores the command line used to create the file.
		Modify the tool to more closely follow other SiLK tools.
		POTENTIAL INCOMPATIBILITY. Do not read the binary form of the Legacy GeoIP country code map. Only accept the comma separated value form.
	rwstats
		Allow the --count switch to accept an argument of 0 which indicates that it should print all bins.
		Allow the --percentage switch to accept a floating point value.
	rwsort
		Do not limit the maximum sort-buffer size to a 32-bit value on 64-bit platforms.
	rwdedupe
		Do not limit the maximum sort-buffer size to a 32-bit value on 64-bit platforms.
	rwcombine
		Do not limit the maximum sort-buffer size to a 32-bit value on 64-bit platforms.
	rwpmapbuild
		Add a header to the prefix map file that stores the command line used to create the file.
	rwsilk2ipfix
		Use multiple IPFIX templates when converting SiLK flow records.
		Add a --single-template switch to mimic the previous behavior.
	rwbagtool
		Fix an issue where the --compression-method switch was not applied to the IPset created by --coverset.
	rwflowpack, flowcap
		Fix a call to abort() that would occur when processing IPFIX records and a byte-count or packet-count of zero occurred in an unexpected place.
		Fix a bug that prevented creating a TCP IPFIX listener and a UDP IPFIX listener on the same port number.
	rwsender
		Attempt to resend any file that is not transferred unless the file is explicitly rejected by the rwreceiver.
		Add the --send-attempts switch that allows setting the number of attempts that are made to transfer a file.
		If sending a file fails and another attempt is to be made, append the file's name onto the back of the send queue.
		Allow setting of the --send-attempts switch from the configuration file and system initialization script.
		Fix a memory leak that may occur when rwsender is processing a file for an rwreceiver and their network connection ends.
		Support partial reads of a message header when GnuTLS is used.
		Log the GnuTLS error message that causes a connection to close.
	rwreceiver
		Support partial reads of a message header when GnuTLS is used.
		Log the GnuTLS error message that causes a connection to close.
	Building
		Fix several "make check" failures on OS X when System Integrity Protection is enabled.
		Remove use of pthread_atfork that preventing compilation on some systems.

* Thu Oct  8 2015 Lawrence R. Rogers <lrr@cert.org> 3.11.0.1-1/2
* Release 3.11.0.1-1/2
	3.11.0.1
		Fix linking issue on Ubuntu when PySiLK support is enabled.
	3.11.0
		Allow rwsiteinfo to report on date ranges of files in a SiLK repository.
		Provide a way to set the default textual timestamp format and timezone from the environment.
		Provide a way to set the default textual IP format from the environment.
		Compile the PySiLK plug-in into the tools that can use it.
		Remove support for fixbuf releases prior to libfixbuf-1.6.0.
		Make additional changes and bug fixes.

* Mon Jul  6 2015 Lawrence R. Rogers <lrr@cert.org> 3.10.2-3/4
* Release 3.10.2-3/4
	Rebuild for libfixbuf-1.7.0.

* Thu May 21 2015 Lawrence R. Rogers <lrr@cert.org> 3.10.2-1/2
* Release 3.10.2-1/2
	Remove support for fixbuf releases prior to libfixbuf-1.4.0.
	Fix several bugs related to IPv6 addresses.

* Thu Feb 26 2015 Lawrence R. Rogers <lrr@cert.org> 3.10.1-1/2
* Release 3.10.1-1/2
	rwstats and rwuniq
		Change how rwstats and rwuniq use temporary files when distinct counts are being computed to fix the issue where the tool
		  would sometimes exit with "Error merging values from temporary file".
		Use compression when writing to temporary files.
	rwsort, rwcombine, and rwdedupe
		Use compression when writing to temporary files.
	rwappend
		Fix a bug that could cause rwappend to remove /dev/null when run as root.
	flowcap
		Allow accept-from-host in sensor.conf to take multiple arguments.
	rwflowpack
		Allow accept-from-host in sensor.conf to take multiple arguments.
		Fix a potential crash when using --input-mode=respool and rwflowpack runs out of file descriptors.
	Building
		Fix a bug in the "Requires:" line of the generated silk.spec file when multiple optional dependencies are not available.
		Do not install rwscanquery when configure fails to find Perl's DBI module.

* Thu Dec 18 2014 Lawrence R. Rogers <lrr@cert.org> 3.10.0-1/2
* Release 3.10.0-1/2
	Important bug fixes in rwfilter and rwsetmember.
	rwflowpack can categorize flow records using an IPset.
	Several changes to logging in rwflowpack and flowcap, including a new default value.
	Additional changes and bug fixes.

* Wed Dec 10 2014 Lawrence R. Rogers <lrr@cert.org> 3.9.0-9/10
* Release 3.9.0-9/10
	Rebuild for libfixbuf-1.6.2.

* Wed Oct 15 2014 Lawrence R. Rogers <lrr@cert.org> 3.9.0-7/8
* Release 3.9.0-7/8
	Rebuild for libfixbuf-1.6.1.

* Wed Oct 8 2014 Lawrence R. Rogers <lrr@cert.org> 3.9.0-5/6
* Release 3.9.0-5/6
	Removed Obsoletes clause.

* Mon Sep 29 2014 Lawrence R. Rogers <lrr@cert.org> 3.9.0-3/4
* Release 3.9.0-3/4
	Rebuild for libfixbuf-1.6.0.

* Thu Sep 25 2014 Lawrence R. Rogers <lrr@cert.org> 3.9.0-1
* Release 3.9.0-1
	New tool rwcombine creates a single flow record from multiple records that represent a single, long-lived session.
	Several enhancements to rwmatch.
	Support for collecting sFlow v5 records (uses libfixbuf-1.6.0).
	Additional enhancements and bug fixes.

* Thu Jul 31 2014 Lawrence R. Rogers <lrr@cert.org> 3.8.3-1
* Release 3.8.3-1
	rwstats and rwuniq
		Fix a bug when --fields contained "dPort" followed by "icmpTypeCode" that caused the "dPort" field to display as 0.
	Additional changes and bug fixes

* Thu Apr 24 2014 Lawrence R. Rogers <lrr@cert.org> 3.8.2-1
* Release 3.8.2-1
	Add multiple thread support to rwflowappend.
	Support logging of IPFIX and NetFlow v9 templates received by rwflowpack and flowcap.
	Revision 1 - without IPA
	Revision 2 - with IPA

* Mon Mar 17 2014 Lawrence R. Rogers <lrr@cert.org> 3.8.1-2
* Release 3.8.1-2
	Took the time to make the build process cleaner so that it does not try to use programs that aren't installed.

* Thu Jan 30 2014 Lawrence R. Rogers <lrr@cert.org> 3.8.1-1
* Release 3.8.1-1
	See http://tools.netsa.cert.org/silk/releasenotes.html#release-3.8.1 for the changes in this release.

* Thu Nov 21 2013 Lawrence R. Rogers <lrr@cert.org> 3.8.0-1
* Release 3.8.0-1
	Allow rwpmaplookup to print the range that contains the key
	Improve handling of records from some devices that export NetFlow v9
	Add support for libfixbuf-1.4.0 and remove support for releases prior to libfixbuf-1.2.0

* Sun Aug 18 2013 Lawrence R. Rogers <lrr@cert.org> 3.7.2-1
* Release 3.7.2-1
	PySiLK changes
		Add IPSet.is_ipv6() and IPSet.convert() methods.
		Fix a bug when saving an IPv6-IPset that contains only IPv4 addresses.
	IPset bug fixes
		Fix bugs when computing the union or intersection of an IPv4-IPset and an IPv6-IPset that contains only IPv4 addresses.
	rwfilter bug fixes
		Fix a spurious warning when loading an IPset.
		Fix a memory issue during shutdown when an argument to one of the --*cidr switches (--scidr, --dcidr, etc) is mistyped.
	rwflowpack, flowcap bug fixes
		Fix a bug where the daemon failed to read TCP flags contained in a SubTemplateMultiList when reading IPFIX data over the network.
		Fix a memory leak when receiving IPFIX data containing a SubTemplateList or a SubTemplateMultiList.
* Thu May 30 2013 Lawrence R. Rogers <lrr@cert.org> 3.7.1-1
* Release 3.7.1-1
	rwpmaplookup enhancement
		Add --ipset-files switch that supports using IPsets to query prefix maps.
	rwdedupe bug fix
		Fix a crash that would occur when using --xargs with an empty list of files.
	rwsort bug fix
		Create a valid SiLK Flow file when using --xargs with an empty list of files.
	rwcut bug fix
		Print the title line when using --xargs with an empty list of files.
	rwrecgenerator bug fix
		Fix a bug when using --sensor-prefix-map that would set either the source or destination address to a random value.
	Building
		Fix a small issue in the silk.spec file when the dist RPM macro was not defined.

* Thu May 30 2013 Lawrence R. Rogers <lrr@cert.org> 3.7.0-1
* Release 3.7.0-1
	Add a new IPset file format which requires less disk space.
	Add new --ip-format switch to control how IPs are displayed.
	Add new --any-index and --any-cc switches to rwfilter.
	Add manual pages for rwflowpack's packing-logic plug-ins.
	Change how rwflowpack and flowcap report out-of-sequence NetFlow V5 packets.

* Tue Apr 23 2013 Lawrence R. Rogers <lrr@cert.org> 3.6.1-1
* Release 3.6.1-1
	Fix a bug in rwflowpack that caused the --pack-interfaces switch to be ignored.

* Thu Apr 11 2013 Lawrence R. Rogers <lrr@cert.org> 3.6.0-1
* Release 3.6.0-1
	Use the smaller SiLK-2 IPset memory representation for IPsets that contain only IPv4 addresses.
	Change sending output-mode in rwflowpack. Add a new incremental-files output-mode to rwflowpack.
	Have rwflowpack and flowcap record lost NetFlowV9 packets (requires libfixbuf-1.3.0).
	Add ability for rwreceiver to monitor disk usage.
	Verify that the --post-command switch and similar switches do not contain any unrecognized %-conversions.
	Many additional changes and bug fixes.

* Tue Mar 12 2013 Lawrence R. Rogers <lrr@cert.org> 3.5.1-2
* Release 3.5.1-2
	New release linked with libfixbuf 1.3.0

* Thu Dec 20 2012 Lawrence R. Rogers <lrr@cert.org> 3.5.1-1
* Release 3.5.1-1
	Fix bug in the IPset library that made it impossible to store very large IPset files.
	Various changes to rwsiteinfo.
	Fix issue in rwreceiver that could cause it to close valid connections.

* Thu Nov 1 2012 Lawrence R. Rogers <lrr@cert.org> 3.5.0-1
* Release 3.5.0-1
	Add country code support for IPv6 addresses.
	Fix issue in rwreceiver that could cause it to close valid connections.
	Fix a bug on 32-bit platforms when reading files compressed with LZO that could cause memory corruption.
	Modify how rwflowappend determines the hourly file in which flow records are to be stored.
	Several additional bug fixes.

* Thu Sep 27 2012 Lawrence R. Rogers <lrr@cert.org> 3.4.1-1
* Release 3.4.1-1
	Add new --tail-recs switch to rwcut.
	Fix issue where receiving incorrect data from a previously rejected UDP client could case rwflowpack or flowcap to exit.

* Thu Sep 13 2012 Lawrence R. Rogers <lrr@cert.org> 3.4.0-1
* Release 3.4.0-1
	Modify how SiLK decodes the ICMP type and code stored in certain SiLK Flow records.
	Provide the new configure option --disable-silk3-ipsets which causes SiLK to use the IPset library as it
		existed in SiLK-2. When this switch is used, IPsets cannot store IPv6 addresses.
	Add support for libfixbuf-1.2.0, which allows multiple NetFlow v9 sources to connect to the same port.
	Add enhancements to rwsetcat, rwsetmember, rwscan.
	Fix bugs in rwuniq, rwstats, rwcut, rwipfix2silk.

* Wed Aug 1 2012 Lawrence R. Rogers <lrr@cert.org> 3.3.4-1
* Release 3.3.4-1
	* Fix bug where rwscanquery would attempt to write a file beginning and ending with a quote character.
	* Fix potentional issue in rwsender when attempting to exit after encountering an unexpected condition.

* Thu Jul 19 2012 Lawrence R. Rogers <lrr@cert.org> 3.3.3-1
* Release 3.3.3-1
	* Fix bug in log file locking and rotation.

* Thu Jul 12 2012 Lawrence R. Rogers <lrr@cert.org> 3.3.2-1
* Release 3.3.2-1
	* Fixes in the IPset and Bag tools.

* Thu Jun 14 2012 Lawrence R. Rogers <lrr@cert.org> 3.3.0-1
* Release 3.3.0-1
	* Critical fixes in rwuniq, rwstats, and the IPset tools.
	* Enhancements to rwscanquery
	* In flowcap, new log messages record the number of record processed for IPFIX probes and NetFlow v9 probes.

* Thu Apr 26 2012 Lawrence R. Rogers <lrr@cert.org> 3.2.1-1
* Release 3.2.1-1
	* Fix an issue when using multiple compressed IPsets in rwfilter on MPI.
	* Make rwflowpack and flowcap more robust with respect to error codes returned by libfixbuf.
	* Fix issues that prevented daemons from shutting down cleanly on some BSD OSes.

* Tue Mar 20 2012 Lawrence R. Rogers <lrr@cert.org> 3.2.0-1
* Release 3.2.0-1
	* Fix an issue when creating files on MPI where the compression was set to "default" or "best".
	* Additional bug fixes.

* Wed Feb 15 2012 Lawrence R. Rogers <lrr@cert.org> 3.1.0-1
* Release 3.1.0-1
	* rwflowappend uses advisory write locks to prevent multiple rwflowappend processes from each attempting to write to the same file.
	* Fix several issues in handling IPFIX.
	* Ignore IPFIX records that report a byte or packet count of zero.

* Fri Sep 30 2011 Lawrence R. Rogers <lrr@cert.org> 3.0.0-1
* Release 3.0.0-1
	* Support for IPv6 addresses in IPsets, Bags, and Prefix Maps.
	* New tools: rwsiteinfo, rwpmaplookup, rwpdu2silk
	* Improved IPFIX support, including allowing collection from multiple sources on a single TCP port. libfixbuf-1.0.0 is now required.

