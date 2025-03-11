%define debug_package %{nil}

%define Testing 0
%{?_with_Testing:%define Testing 1}

%define name super_mediator

%if %{Testing}
%define version 2.0.0.alpha1
%define release 1
%else
%define version 1.9.0
%define release 1
%endif

Summary:	IPFIX Super Mediator for use with the YAF and SiLK tools
Name:		%{name}
Version:	%{version}
Release:	%{release}%{dist}
Group:		Applications/System
License:	GPLv2
Source:		http://tools.netsa.cert.org/releases/%{name}-%{version}.tar.gz
URL:		http://tools.netsa.cert.org/super_mediator/
BuildRoot:	%{_tmppath}/%{name}-%{version}
Packager:	Emily Sarneso <ecoff@cert.org>
Provides:	super_mediator
Requires:	glib2 >= 2.12.0
Requires:	libfixbuf >= 1.0.0
%if 0%{?centos} >= 8
BuildRequires:	mariadb-devel >= 5.0
%else
BuildRequires:	mysql-devel >= 5.0
%endif
Requires:	silk-ipset-lib >= 3.0
BuildRequires:	silk-ipset-devel >= 3.0
BuildRequires:	silk-devel >= 3.0
BuildRequires:	glib2-devel >= 2.12.0
BuildRequires:	libfixbuf-devel >= 1.0.0
BuildRequires:	byacc
BuildRequires:	lzo-devel
BuildRequires:	snappy-devel
%if 0%{?centos} == 5
Patch1:		%{name}-%{version}-patch-001
%endif
Requires(post):	/sbin/ldconfig, /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(postun): /sbin/ldconfig

%description
super_mediator is an IPFIX mediator for use with the YAF and SiLK tools.
It collects and filters YAF output data to various IPFIX collecting processes
and/or csv files. super_mediator can be configured to perform de-duplication
of DNS resource records, SSL certificates, or HTTP header fields as exported
by YAF.

%prep
%setup -q -n %{name}-%{version}
%if 0%{?centos} == 5
%patch1 -p1
%endif

%build
%if 0%{?fedora} >= 23 || 0%{?centos} >= 8
%ifarch x86_64
export CC="gcc -fPIC"
%endif
%endif
%if %{Testing}
./configure --prefix=%{_prefix}
%else
./configure --prefix=%{_prefix}  --with-skipset
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%makeinstall

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d/
install --mode=0755 etc/init.d/super_mediator $RPM_BUILD_ROOT%{_sysconfdir}/init.d/        
install --mode=0644 etc/super_mediator.conf $RPM_BUILD_ROOT%{_sysconfdir} 

################################################################################################################
# Fix the Shebang problem for Python2 executables
################################################################################################################
for s in %{buildroot}%{_bindir}/*
do
	file $s | grep -q -i 'python script' && sed --in-place '1s=python[^2]*=python2=' $s
done

%post
/sbin/ldconfig
function runlvl(){
    ( /sbin/chkconfig --del $1 || true )
    /sbin/chkconfig --add $1
    /sbin/chkconfig --levels 345 $1 on
    /sbin/chkconfig --levels 016 $1 off
}

%postun -p /sbin/ldconfig

%preun
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del yaf
fi

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc NEWS README
%{_bindir}/super_mediator
%{_bindir}/super_table_creator
%{_mandir}/*
%config(noreplace) %{_sysconfdir}/super_mediator.conf
%attr(755,root,root) %{_sysconfdir}/init.d/super_mediator

%changelog
* Wed Jun  8 2022 Lawrence R. Rogers <lrr@cert.org> 1.9.0-1
* Release 1.9.0-1
	Added support for labeling records based on data from a SiLK IPSet or a SiLK Prefix Map.
	Added support for labeling records with a sensor and flowtype similar to SiLK's rwflowpack tool.
	Added support for OpenSSL 3.0.1.
	Changed JSON output of SSL records for unknown sslObjectType values: For unknown value X, key sslCertObjectIDX is replaced by sslCertIssuerObjectIdX or sslCertSubObjectIdX.
		When X is 1, EmailAddress is used (e.g., sslCertIssuerEmailAddress) and when X is 25 DomainComponent is used.
	Changed the super_mediator.spec file to configure the build using --with FEATURE options to rpmbuild.
	Fixed a small bug in JSON output of rewritten SSL certificates.
	Fixed bugs in TEXT export of very old YAF SSL data.
	Changed the template scopes for the YAF stats template and Tombstone template to match those used by YAF.

%if %{Testing}
* Thu Mar 10 2022 Lawrence R. Rogers <lrr@cert.org> 2.0.0.alpha1-1
* Release 2.0.0.alpha1-1
	Increased the flexibility of super_mediator by eliminating most internal template definitions and having it use the incoming template definitions instead.
	Changed the syntax of the configuration file; previous versions of the files need to be updated.
	Made changes to the command line parsing and eliminated several options. The configuration file is the preferred way to configure super_mediator.
	Enhanced statistics for types of records read from a collector and written to an exporter.
	Temporarily disabled SiLK IPset and MySQL support.
	Note: Exporting as delimited TEXT is lightly tested and contains bugs.
	Updated the fixbuf requirement to libfixbuf-3.0.0.
%endif

* Tue Dec 22 2020 Lawrence R. Rogers <lrr@cert.org> 1.8.0-1
* Release 1.8.0-1
	Added a new switch, --rewrite-ssl-certs, which restructures the template used for TLS/SSL certificates for IPFIX exporters. The template uses specific IEs for some fields in an SSL certificate.
		The --rewrite-ssl-certs switch also allows a super_mediator to read the new SSL template from an upstream super_mediator. Deduplication of the rewritten certificates is not supported.
	Added the ability to read the new SMTP DPI records exported by YAF 2.12.0.
	Added the observation domain ID to JSON output.

* Fri Apr 17 2020 Lawrence R. Rogers <lrr@cert.org> 1.7.1-3
* Release 1.7.1-3
	Rebuilt for silk 3.19.1-1/2

* Fri Feb 28 2020 Lawrence R. Rogers <lrr@cert.org> 1.7.1-2
* Release 1.7.1-2
	Rebuilt for silk 3.19.0-3/4

* Thu Oct 24 2019 Lawrence R. Rogers <lrr@cert.org> 1.7.1-1
* Release 1.7.1-1
	Added ability to preserve observation domain of incoming records.
	Changed scope of Tombstone records to 3 for consistency with YAF.
	Fixed a crash when TCP collector and CLI --input are used concurrently.

* Fri Aug 30 2019 Lawrence R. Rogers <lrr@cert.org> 1.7.0-4
* Release 1.7.0-4
        Rebuilt for libfixbuf-2.4.0.

* Wed Jun 19 2019 Lawrence R. Rogers <lrr@cert.org> 1.7.0-3
* Release 1.7.0-3
        Rebuilt for libfixbuf-2.3.1.

* Fri Apr 19 2019 Lawrence R. Rogers <lrr@cert.org> 1.7.0-2
* Release 1.7.0-2
        Rebuilt for libfixbuf-2.3.1.

* Mon Mar 18 2019 Lawrence R. Rogers <lrr@cert.org> - 1.7.0-1
* Release 1.7.0-1
	Support for FixBuf 2.3.0 added, and is now required.
	New YAF stats messages supported.
	New Tombstone format supported.
	Race condiditon addressed when exporter configured to GZIP and MOVE files.
	Dynamically generated dedup template names added.
	Option record bugfixes.

* Mon Dec 17 2018 Lawrence R. Rogers <lrr@cert.org> - 1.6.0-5
* Release 1.6.0-5
	Rebuilt with silk 3.18.0.

* Tue Dec  4 2018 Lawrence R. Rogers <lrr@cert.org> - 1.6.0-4
* Release 1.6.0-4
	Rebuilt with libfixbuf 2.2.0.

* Tue Nov 27 2018 Lawrence R. Rogers <lrr@cert.org> - 1.6.0-3
* Release 1.6.0-3
	Rebuilt with silk-devel (missing) dependency

* Thu Jul 19 2018 Lawrence R. Rogers <lrr@cert.org> - 1.6.0-2
* Release 1.6.0-2
	Rebuilt with libfixbuf 2.1.0.

* Fri Jun  1 2018 Lawrence R. Rogers <lrr@cert.org> - 1.6.0-1
* Release 1.6.0-1
	Changes
		Support for FixBuf 2.0.0 added, and is now required.
		Derive information elements from included XML files.
		Support for tombstone records added.
		Fixed flow output bugs where information elements were transposed.
		Support for cmake build removed.

* Thu Nov  9 2017 Lawrence R. Rogers <lrr@cert.org> - 1.5.3-2
* Release 1.5.3-2
	Rebuilt with libfixbuf 1.8.0.

* Thu Oct 19 2017 Lawrence R. Rogers <lrr@cert.org> - 1.5.3-1
* Release 1.5.3-1
	Changes
	 1.5.3
 	  Added template metadata (name and description) record output.

* Wed Mar  8 2017 Lawrence R. Rogers <lrr@cert.org> - 1.5.2-1
* Release 1.5.2-1
	Changes
	 1.5.2
 	  Fix compile error introduced in version 1.5.1
	 1.5.1
	  Add --become-user and --become-group command line options
	  Bug Fix for compiling on Alpine Linux

* Thu Jan  5 2017 Lawrence R. Rogers <lrr@cert.org> - 1.5.0-1
* Release 1.5.0-1
	Add support for adding VLAN/Observation IDs to deduplication keys
	Changed format of DEDUP Exporters (added flow start time associated with flow key hash)
	Add ability to insert EXPORTER name in deduplication output records
	Add ability to read gzip'd IPFIX files
	Other Bug Fixes

* Tue Oct  4 2016 Lawrence R. Rogers <lrr@cert.org> - 1.4.0-1
* Release 1.4.0-1
	Add support for multiple protocol deduplication for IPFIX/JSON exporters
	Add post move file option for exporters
	Add PAYLOAD, RPAYLOAD export options to custom field lists
	Empty files are now removed by default
	Bug Fix for uploading MULTI_FILES files to a MySQL database
	Other Bug Fixes

* Tue Mar  8 2016 Lawrence R. Rogers <lrr@cert.org> - 1.3.0-1
* Release 1.3.0-1
	Version 1.3.0 changes
		Add file compression support for EXPORTERS
		Add Base64 Encode support for full certificate export
		Changed default file extension for JSON files to .json
		Bug Fix for ESCAPE_CHARS keyword for DNS_DEDUP Exporters
		Fix bug when command line arguments and config file are present
		Other Bug Fixes
	Version 1.2.2 changes
		Bug Fixes for JSON exporters

* Tue Dec 29 2015 Lawrence R. Rogers <lrr@cert.org> - 1.2.1-1
* Release 1.2.1-1
	Add JSON output option to --output-mode switch
	Bug Fix for JSON exporters (DNS output)

* Tue Dec 22 2015 Lawrence R. Rogers <lrr@cert.org> - 1.2.0-1
* Release 1.2.0-1
	Remove support for fixbuf releases prior to libfixbuf-1.7.0
	Collect and export sslServerName
	Collect, decode, and export full X.509 Certificates
	MD5 hashing of X.509 Certificates with OpenSSL support
	SHA1 hashing of X.509 Certificates with OpenSSL support
	Collect and export list of DHCP options
	Bug Fixes

* Mon Dec  7 2015 Lawrence R. Rogers <lrr@cert.org> - 1.1.3-1
* Release 1.1.3-1
	Bug Fix for logging to syslog
	DNS Deduplication JSON export bug fix
	Update RPM spec file

* Wed Oct 28 2015 Lawrence R. Rogers <lrr@cert.org> - 1.1.2-1
* Release 1.1.2-1
	Bug Fix for TCP/UDP collector(s) that receive minimal data

* Tue Oct 20 2015 Lawrence R. Rogers <lrr@cert.org> - 1.1.1-3
* Release 1.1.1-3
	Rebuilt for silk-ipset-3.11.0.

* Tue Oct 20 2015 Lawrence R. Rogers <lrr@cert.org> - 1.1.1-2
* Release 1.1.1-2
	Rebuilt for libfixbuf 1.7.1.

* Wed Jul  1 2015 Lawrence R. Rogers <lrr@cert.org> - 1.1.1-1
* Release 1.1.1-1
	1.1.1, 2015-Jul-1
		Bug Fix for Custom Field List Text Exporters
		Bug Fix for configuring SSL De-duplication MAX_HIT_COUNT and FLUSH_TIME
		super_table_creator will now create de-duplication tables
		Documentation updates

* Fri Jun 26 2015 Lawrence R. Rogers <lrr@cert.org> - 1.1.0-1
* Release 1.1.0-1
	1.1.0 - 2015-06-26
		Requires libfixbuf 1.4.0 or greater
		SSL Certificate De-duplication
		Advanced SSL field export configuration
		Configurable De-duplication of any DPI Fields
		JSON file export
		Export of unnested DNS Resource Records
		New option to only export DNS Responses
		Add the ability to rotate and compress logs given a valid file directory
		New option to de-duplicate on only particular DNS resource record types
		MULTI_FILES CSV format change
		MySQL schema change for MULTI_FILES
		Bug Fix for Spread Collectors when daemon terminates
		Bug Fixes

	1.0.2 - 2014-10-15
		Bug Fix for Collectors

	1.0.1 - 2014-08-12
		Add support for escaping control characters and the delimiter character in DPI strings
		Bug Fix for DNP 3.0 text export
		Other Minor Bug Fixes.

	1.0.0 - 2014-06-13
		Add support for multiple collectors
		Add support for naming collectors and exporters
		Collector name included in default flow text export

	0.4.0 - 2014-03-04
		Added SCADA protocol and RTP DPI collection
		Added MySQL automatic reconnection capability
		Syslog logging capability
		Added ability to collect, print, and export MPLS labels
		Added ability to collect, print, and export Type of Service fields
		Incoming IPFIX records that use Delta counters will export the same fields
		Bug Fix for variable redeclaration on some operating systems
		Bug Fix for DNS deduplication timeout
		Other Bug Fixes


* Wed Dec 10 2014 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-8
* Release 0.3.0-8
	New release linked with libfixbuf 1.6.2

* Wed Oct 15 2014 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-7
* Release 0.3.0-7
	New release linked with libfixbuf 1.6.1

* Tue Sep 30 2014 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-6
* Release 0.3.0-6
	New release linked with libfixbuf 1.6.0

* Wed Aug 20 2014 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-5
* Release 0.3.0-5
	New release linked with libfixbuf 1.5.0 - CentOS 6 x86_64 omitted by accident.
	This release fixes that and simply recompiles super_mediator for all other 
	supported releases and architecture for consistency.

* Fri Aug 8 2014 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-4
* Release 0.3.0-4
	New release linked with libfixbuf 1.5.0

* Mon Jan 13 2014 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-3
* Release 0.3.0-3
	Patch for Fedora 20

* Fri Dec 13 2013 Lawrence R. Rogers <lrr@cert.org> - 0.2.2-2
* Release 0.2.2-2
	New release linked with libfixbuf 1.4.0

* Fri May 03 2013 Lawrence R. Rogers <lrr@cert.org> - 0.3.0-1
* Release 0.3.0-1
	Added the ability to define new information elements for collection
	New filter fields: INGRESS and EGRESS
	Added the ability to "AND" filters
	Added new YAF 2.4.0 information elements
	Bug Fixes

* Tue Mar 12 2013 Lawrence R. Rogers <lrr@cert.org> - 0.2.2-1
* Release 0.2.2-1
	New release linked with libfixbuf 1.3.0

* Tue Feb 26 2013 Lawrence R. Rogers <lrr@cert.org> - 0.2.2-0
* Release 0.2.2-0
	Bug Fix for GLib version 2.32 or greater
	Added statistics timeout option for logging super_mediator stats
	Other Bug Fixes

* Fri Feb 8 2013 Lawrence R. Rogers <lrr@cert.org> - 0.2.1-1
* Release 0.2.1-1
	Added Custom DPI Field List for Text Exporters
	Added --fields switch to command line arguments
	Bug Fix for Time output on some platforms
	Bug Fix for SSL/TLS Text Export

* Wed Jan 16 2013 Lawrence R. Rogers <lrr@cert.org> - 0.2.0-1
* Release 0.2.0-1
	Retries exporter connections when lost
	Maintains export statistics per exporter
	Bug Fix for polling directory for IPFIX files
	Bug Fix for moving collector files

* Thu Dec 6 2012 Lawrence R. Rogers <lrr@cert.org> - 0.1.9-1
* Release 0.1.9-1
	Added Custom Field Lists for Text Exporters
	Bug Fix for reading from stdin
	Other Bug Fixes
