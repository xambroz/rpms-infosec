%define debug_package %{nil}

%define name    silk-ipset
%define version 3.18.0
%define release 1

Name:		%{name}
Version:	%{version}
Release:	%{release}%{?dist}
Summary:	SiLK IPset: Library and tools for manipulating sets of IP Addresses
License:	GPLv2
Vendor:		CERT Network Situational Awareness <netsa-help@cert.org>
URL:		http://tools.netsa.cert.org/silk-ipset/index.html
Source:		%{name}-%{version}.tar.gz
%if 0%{?centos} == 6
Patch1:		%{name}-%{version}-patch-001
%endif
Group:		Applications/System
Prefix:		/usr
Requires:	lzo, zlib
Requires:	filesystem
BuildRequires:	lzo-devel, zlib-devel
BuildRequires:	snappy, snappy-devel
BuildRequires:  autoconf automake libtool
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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

%define enable_applications 1
%if %{enable_applications}
%define config_enable_applications --enable-applications
%else
%define config_enable_applications --disable-applications
%endif

#######################################################################
# RCSIDENT("$SiLK: silk-ipset.spec.in 52399a63ee72 2013-06-21 19:04:55Z mthomas $")
#######################################################################

%description
The SiLK IPset packages contain a library and a set of command line
tools to build and manipulate IPset files, which are binary files
containing a set of IP addresses.

The SiLK IPset packages are derived from the SiLK traffic analysis
tools developed by the CERT Network Situational Awareness Team (CERT
NetSA).  Since the SiLK IPset packages contain a small subset of the
tools in the SiLK package, there is no need to install the SiLK IPset
packages when the SiLK packages are installed.

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
%if 0%{?centos} == 6
%patch1 -p1
%endif
autoreconf -fiv

%build
%configure  %{config_enable_applications} --disable-static --enable-ipset-compatibility
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/silk/*.la
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/silk

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


#  ###################################################################
#  silk-ipset-tools

%if %{enable_applications}
%package tools
Group:		Applications/System
Summary: The SiLK IPset command line applications
Requires: silk-ipset-lib
Conflicts: silk-analysis

%description tools
The silk-ipset-tools package contains the user applications to build
and manipulate IPsets (binary files containing a set of IP addresses).

The SiLK IPset packages are derived from the SiLK traffic analysis
tools developed by the CERT Network Situational Awareness Team (CERT
NetSA).  Since the SiLK IPset packages contain a small subset of the
tools in the SiLK package, there is no need to install the SiLK IPset
packages when the SiLK packages are installed.
%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%endif


#  ###################################################################
#  silk-ipset-lib

%package lib
Group: System Environment/Libraries
Summary: The SiLK IPset library

%description lib 
The silk-ipset-lib package contains the library needed to manipulate
IPsets (binary files containing a set of IP addresses).

The SiLK IPset packages are derived from the SiLK traffic analysis
tools developed by the CERT Network Situational Awareness Team (CERT
NetSA).  Since the SiLK IPset packages contain a small subset of the
tools in the SiLK package, there is no need to install the SiLK IPset
packages when the SiLK packages are installed.
%files lib
%defattr(-,root,root)
%{_libdir}/*.so.*

%post lib
/sbin/ldconfig

%postun lib
/sbin/ldconfig


#  ###################################################################
#  silk-ipset-devel

%package devel
Group: Development/Libraries
Summary: The SiLK IPset development files
Requires: silk-ipset-lib

%description devel
The silk-ipset-devel package contains the development libraries and
headers for SiLK IPset.  This package can be used to build
applications that use the SiLK IPset library.

The SiLK IPset packages are derived from the SiLK traffic analysis
tools developed by the CERT Network Situational Awareness Team (CERT
NetSA).  Since the SiLK IPset packages contain a small subset of the
tools in the SiLK package, there is no need to install the SiLK IPset
packages when the SiLK packages are installed.
%files devel
%defattr(-,root,root)
%{_includedir}/silk-ipset
%{_libdir}/*.so
%{_libdir}/*.la

%changelog
* Thu Dec 13 2018 Lawrence R. Rogers <lrr@cert.org> - 3.18.0-1
* Release 3.18.0-1
	rwsetcat
		When --ip-format includes zero-padded and CIDR prefixes are being printed, also apply zero-padding to the prefix.
		Fix a bug when using --ip-format=decimal,zero-padded that caused an extra leading 0 to appear for IPv6 addresses.
	libskipset changes
		Add function skipaddrCidrString() to get a string representation of an IP address and its CIDR designation.
		Add function skipaddrCidrStringMaxlen() to compute column width.
		Add macro SKIPADDR_CIDR_STRLEN for defining minimum buffer size.

* Sun Apr 29 2018 Lawrence R. Rogers <lrr@cert.org> - 3.17.0-1
* Release 3.17.0-1
	rwsetcat
		POTENTIAL INCOMPATIBILITY. Default to using the IPv4 format for IPv6-addresses in the ::ffff:0:0/96 netblock.
		Add new values to the --ip-format switch and change how some values (zero-padded) work.
	libskipset changes
		Add new values to skipaddr_flags_t.
		Add function skipaddrStringMaxlen() to compute column width.
		Mark the num2dot0() and num2dot0_r() functions as deprecated.
		Do not export the structures used by SiLK header entries.

* Thu Feb 15 2018 Lawrence R. Rogers <lrr@cert.org> - 3.16.1-1
* Release 3.16.1-1
	rwsetcat
		Print an error message when rwsetcat is unable to read an IPset.

* Fri Jun 30 2017 Lawrence R. Rogers <lrr@cert.org> - 3.16.0-1
* Release 3.16.0-1
	libskipset changes
		Internal changes
	rwsetbuild, rwsetcat, rwsetmember, rwsettool
		Enhance the manual pages.

* Sat Mar 25 2017 Lawrence R. Rogers <lrr@cert.org> - 3.15.0-1
* Release 3.15.0-1
	libskipset changes
		Add a second argument to skOptionsIPFormatRegister().
		Remove functions that operate on an IPset Header Entry.
		Fix a potential bug in skIPSetWrite() by ensuring that the IPset file's header is set to use native byte order.
	rwsetcat
		Add the --output-path switch to specify the output file.
		Do not use the the pager when the output contains only the count of the number of IPs in a singe IPset.

* Thu Nov 17 2016 Lawrence R. Rogers <lrr@cert.org> - 3.14.0-1
* Release 3.14.0-1
	libskipset changes
		Add a new file format, record-version=5, for IPsets that contain IPv6 addresses.
		Fix a bug when working with IPsets that contain IPv6 addresses and have more than 44,739,242
		 internal nodes. The bug may cause the tool to crash or to loop endlessly.
		Reduce how quickly memory grows when building an IPset that contains IPv6 addresses.
		Perform additional integrity checks when reading an IPset file from disk.
		Add support for printing a more detailed error message when attempting to read an IPset file. The
		 message is printed when the SILK_IPSET_PRINT_READ_ERROR environment variable is set.
	rwsetbuild
		Fix a bug introduced in SiLK IPset-3.11.0 that may occur when computing the intersection or
		 difference of an IPv4 IPset with an IPv6 IPset that is in record-version=4 format. Addresses in
		 the ::ffff:0:0/96 netblock of the IPv6 IPset were ignored when the IPset contained clusters of
		 addresses less then ::ffff:0:0.
	rwsetcat
		Add support for counting the IP addresses in an IPset without loading the IPset into memory.
		Fix a bug where a completely full IPv6 IPset would report it contained 0 IPs.
	Building
		Add a configure switch, --enable-ipset-compatibility, that allows changing the default IPset file
		 format written by the tools. The argument is the version of SiLK IPset with which IPsets are to
		 be compatible. New file formats were added at 3.7.0 and 3.14.0.

* Thu Sep 29 2016 Lawrence R. Rogers <lrr@cert.org> - 3.13.0-1
* Release 3.13.0-1
	Change across all tools
		Add support for compressing files with "Snappy" compression when the Snappy library and header are found during configuration.
		Add support for the SILK_COMPRESSION_METHOD environment variable that provides a default value for the --compression-method switch.
	rwsettool
		Add a --symmetric-difference switch to compute the set of IP addresses that occur in only one of two input IPsets.
		Add more examples to the manual page.
	rwsetcat
		Add many more examples to the manual page.
	libskipset
		Rename functions sksiteCompmethod...() to skCompMethod...().
		Rename functions sksiteFileformat...() to skFileFormat...().
		Remove some skHeader...() functions from the public headers.

* Thu Mar 31 2016 Lawrence R. Rogers <lrr@cert.org> - 3.12.0-1
* Release 3.12.0-1
	ibskipset
		Fix a bug in the code that copies an memory-mapped IPset prior to modifying it.

* Wed Sep 30 2015 Lawrence R. Rogers <lrr@cert.org> - 3.11.0-1
* Release 3.11.0-1
	libskipset
		Add functions to process an IPset without reading it into memory.
		Change definition of skipset_iterator_t.
		Change some skIPTree* APIs from macros to functions and vice versa.
		Fix a bug in skIPSetIteratorNext() and skIPSetWalk() when visiting the individual IPs of an IPv6 IPset and numeric prefix of the current leaf is 64 or less.
		Additional changes.
	rwsetcat
		Add support for the SILK_IP_FORMAT environment variable that provides a default value for the --ip-format switch.
		Allowing printing of IPset contents without reading the IPset into memory.
	rwsettool
		Avoid reading an IPset into memory when possible.
	rwsetbuild
		Print an error and exit when the --ip-ranges delimiter is set to the comment character('#'), newline, or the empty string.

* Thu May 21 2015 Lawrence R. Rogers <lrr@cert.org> - 3.10.2-1
* Release 3.10.2-1
	libskipset
		Change skipaddrString() when flags is SKIPADDR_FORCE_IPV6 so that a single 16-bit 0 field is not shortened (RFC5952).
	rwsetcat
		Change the printing of IPs when the --ip-format is 'force-ipv6' so that a single 16-bit 0 field is not shortened (RFC5952).
		Fix a bug in the output of --network-structure when reading an IPv4 IPset file and the --ip-format was 'force-ipv6' where the net block prefix was not adjusted for the move into IPv6.
		Fix a bug in the output of --network-structure=v4:... when reading an IPv6 IPset file that produced net blocks counts that were incorrect and sometimes impossibly large.
		Fix a display bug of a narrow IP column when processing an IPv4 IPset file and the --ip-format was 'force-ipv6'.

* Thu Dec 18 2014 Lawrence R. Rogers <lrr@cert.org> - 3.10.0-1
* Release 3.10.0-1
	libskipset bug fixes
		Fix a bug in skIPTreeCheckIntersectIPWildcard() where intersections with CIDR blocks sized /17 to /26 are not found.
			This bug could affect rwsetmember when the --count switch is not given causing it to report false instead of true.
		Fix a potential read of uninitialized memory in skIPTreeCIDRBlockIteratorReset(). The read could occur after removing IPs such that a /16 becomes empty.
	Building
		Add a --disable-applications switch to configure to disable building of the command lines tools so only the SiLK IPset library is built and installed.
		Do not build the static library libskipset.a by default. Specify the --enable-static switch to configure for static libraries.
		Require at least autoconf-2.64 and automake-1.12 to rebuild the configure script and Makefile.in files.

* Thu Sep 25 2014 Lawrence R. Rogers <lrr@cert.org> - 3.9.0-1
* Release 3.9.0-1
	libskipset bug fix
		Fix a bug where the IPv6 wildcard "x:x:x:x:x:x:x:x" was being treated as the single IP "::" instead of as all of IPv6 space
		 in skIPSetInsertIPWildcard() and skIPSetCheckIPWildcard(). This change affects the rwsetbuild and rwsetmember tools.
	rwsetmember
		Improve performance when the --count switch is not specified.
	rwsettool
		Improve performance in the --mask and --intersect operations.
		Fix a bug where rwsettool would report an error and not produce output when using the --sample switch with an IPv6 IPset.

* Thu Apr 24 2014 Lawrence R. Rogers <lrr@cert.org> - 3.8.2-1
* Release 3.8.2-1
	libskipset bug fix
		Fix an assertion that may cause the application to abort.
	Building
		Fix small bugs in the silk-ipset.spec file.

* Thu Jan 30 2014 Lawrence R. Rogers <lrr@cert.org> - 3.8.1-1
* Release 3.8.1-1
	libskipset bug fix
		Change parsing of (textual) IPv6 address to be more strict (e.g., fix a bug that treated embedded whitespace as a colon).
		Fix a potential memory leak when intersecting IPsets.

* Thu Aug 15 2013 Lawrence R. Rogers <lrr@cert.org> - 3.7.2-1
* Release 3.7.2-1
	ibskipset bug fix
		Fix bugs when computing the union or intersection of an IPv4-IPset
		 and an IPv6-IPset that contains only IPv4 addresses.

* Fri Jun 21 2013 Lawrence R. Rogers <lrr@cert.org> - 3.7.1-1
* Release 3.7.1-1
	rwsetcat
		Do a better job of reporting errors caused by problems reading IPset files.
	rwsetmember
		Do a better job of reporting errors caused by problems reading IPset files.
	Building
		Fix a small issue in the silk-ipset.spec file when the dist RPM macro was not defined.

* Thu May 30 2013 Lawrence R. Rogers <lrr@cert.org> - 3.7.0-1
* Release 3.7.0-1
	This release corresponds to the SiLK 3.7.0 release.
	As of SiLK IPset 3.6.0, the library uses the SiLK-2 memory representation of the IPset
		code when working with IPsets that contain only IPv4 addresses.

* Thu Apr 11 2013 Lawrence R. Rogers <lrr@cert.org> - 3.6.0-1
* Release 3.6.0-1
	This release corresponds to the SiLK 3.6.0 release.
	As of SiLK IPset 3.6.0, the library uses the SiLK-2 memory representation of the IPset code when working with IPsets that contain only IPv4 addresses.

