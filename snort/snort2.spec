# $Id: snort.spec,v 1.38 2021/12/09 13:43:32 repoman Exp repoman $
# Snort.org's SPEC file for Snort

################################################################
# rpmbuild Package Options
# ========================
#
# See README.build_rpms for more details.
#
# 	--with openappid
# 		include openAppId preprocessor
# See pg 399 of _Red_Hat_RPM_Guide_ for rpmbuild --with and --without options.
################################################################

# Other useful bits
%define SnortRulesDir %{_sysconfdir}/snort/rules
%define noShell /bin/false
%global debug_package %{nil}

# Handle the options noted above.
# Default of no openAppId, but --with openappid will enable it
%define OpenAppID 0
%{?_with_openappid:%define OpenAppID 1}

%define vendor Snort.org
%define for_distro RPMs
%define release 1
%define realname snort

# Look for a directory to see if we're building under cAos 
# Exit status is usually 0 if the dir exists, 1 if not, so
# we reverse that with the '!'
%define caos %([ ! -d /usr/lib/rpm/caos ]; echo $?)

%if %{caos}
  # We are building for cAos (www.caosity.org) and the autobuilder doesn't
  # have command line options so we have to fake the options for whatever
  # packages we actually want here, in addition to tweaking the package
  # info.
  %define vendor cAos Linux 
  %define for_distro RPMs for cAos Linux
  %define release 1.caos
%endif

%if %{OpenAppID}
  %define EnableOpenAppId --enable-open-appid
%endif


%if %{OpenAppID}
Name: %{realname}-openappid
Version: 2.9.19
Summary: An open source Network Intrusion Detection System (NIDS) with open AppId support
Conflicts: %{realname}
BuildRequires: luajit-devel
BuildRequires: libnghttp2-devel
%if 0%{?fedora} == 35
BuildRequires: openssl-devel
%else
%if 0%{?fedora} == 34
%if 0
BuildRequires: openssl1.1-devel
%endif
%else
%if 0%{?fedora} >= 26 
BuildRequires: compat-openssl10-devel
%else
BuildRequires: openssl-devel
%endif
%endif
%endif
Source1: %{realname}-openappid.tar.gz

%else

Name: %{realname}
Version: 2.9.19
Summary: An open source Network Intrusion Detection System (NIDS)
Conflicts: %{realname}-openappid
BuildRequires: luajit-devel
BuildRequires: libnghttp2-devel openssl-devel
%endif
Epoch: 1
Release: %{release}%{?dist}
Group: Applications/Internet
License: GPL
Url: http://www.snort.org/
Source0: https://www.snort.org/downloads/snort/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?centos} == 6 || 0%{?centos} == 7 || 0%{?centos} == 8
%ifarch x86_64
Patch2:	%{realname}-%{version}-patch-002
%endif
%endif

Packager: Official Snort.org %{for_distro}
Vendor: %{vendor}
BuildRequires: autoconf automake pcre-devel libpcap-devel libdnet-devel zlib-devel flex bison libnfnetlink-devel libnetfilter_queue-devel
BuildRequires: daq 
BuildRequires: daq-devel
%if 0%{?fedora} >= 28 || 0%{?centos} >= 8
BuildRequires: libtirpc-devel
%endif

%description
Snort is an open source network intrusion detection system, capable of
performing real-time traffic analysis and packet logging on IP networks.
It can perform protocol analysis, content searching/matching and can be
used to detect a variety of attacks and probes, such as buffer overflows,
stealth port scans, CGI attacks, SMB probes, OS fingerprinting attempts,
and much more.

Snort has three primary uses. It can be used as a straight packet sniffer
like tcpdump(1), a packet logger (useful for network traffic debugging,
etc), or as a full blown network intrusion detection system. 

You MUST edit /etc/snort/snort.conf to configure snort before it will work!

Please see the documentation in %{_docdir}/%{realname}-%{version} for more
information on snort features and configuration.


%prep
%setup -q -n %{realname}-%{version}
%if 0%{?centos} == 6 || 0%{?centos} == 7
%ifarch x86_64
%patch2 -p1
%endif
%endif

# When building from a Snort.org CVS snapshot tarball, you have to run
# autojunk before you can build.
if [ \( ! -s configure \) -a \( -x autojunk.sh \) ]; then
    ./autojunk.sh
fi

# Make sure it worked, or die with a useful error message.
if [ ! -s configure ]; then
    echo "Can't find ./configure.  ./autojunk.sh not present or not executable?"
    exit 2
fi


%build

BuildSnort() {
   %__mkdir "$1"
   cd "$1"
   %__ln_s ../configure ./configure

   if [ "$1" = "plain" ] ; then
       ./configure \
%if 0%{?centos} == 6 || 0%{?centos} == 7 ||  0%{?centos} == 8
%ifarch x86_64
	--with-libpfring-includes=/usr/local/include/ \
	--with-libpfring-libraries=/usr/local/lib \
	--with-libpcap-includes=/usr/include/ \
	--with-libpcap-libraries=/usr/lib \
%endif
%endif
	--disable-open-appid $SNORT_BASE_CONFIG
   fi

   if [ "$1" = "openappid" ] ; then
       ./configure \
%if 0%{?centos} == 6 || 0%{?centos} == 7 ||  0%{?centos} == 8
%ifarch x86_64
	--with-libpfring-includes=/usr/local/include/ \
	--with-libpfring-libraries=/usr/local/lib \
%endif
%endif
       --enable-open-appid --with-openssl-includes=/usr/include/openssl-1.0/ --with-openssl-libraries=/usr/lib/openssl-1.0/ $SNORT_BASE_CONFIG
   fi

%if 0%{?fedora} >= 28 || 0%{?centos} >= 8
   %__make extra_incl="$extra_incl -I/usr/include/tirpc"
%else
   %__make
%endif
   %__mv src/snort ../%{realname}-"$1"
   cd ..
}


CFLAGS="$RPM_OPT_FLAGS -fcommon"
export AM_CFLAGS="-g -O2"
SNORT_BASE_CONFIG="--prefix=%{_prefix} \
                   --bindir=%{_sbindir} \
                   --sysconfdir=%{_sysconfdir}/snort \
                   --with-libpcap-includes=%{_includedir} \
                   --enable-targetbased \
                   --enable-control-socket"

%if %{OpenAppID}
  BuildSnort openappid
%else
  BuildSnort plain
%endif

%install

# Remove leftover CVS files in the tarball, if any...
find . -type 'd' -name "CVS" -print | xargs %{__rm} -rf

InstallSnort() {
   if [ "$1" = "plain" ] || [ "$1" = "openappid" ]; then
	%__rm -rf $RPM_BUILD_ROOT
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sbindir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_bindir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{SnortRulesDir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/snort
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_var}/log/snort
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_initrddir}
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_mandir}/man8
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{realname}-%{version}
	%__install -p -m 0755 %{realname}-"$1" $RPM_BUILD_ROOT%{_sbindir}/%{realname}-"$1"
	%__install -p -m 0755 "$1"/tools/control/snort_control $RPM_BUILD_ROOT%{_bindir}/snort_control
	%__install -p -m 0755 "$1"/tools/u2spewfoo/u2spewfoo $RPM_BUILD_ROOT%{_bindir}/u2spewfoo
	%__install -p -m 0755 "$1"/tools/u2boat/u2boat $RPM_BUILD_ROOT%{_bindir}/u2boat
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicengine
	%__mkdir_p -m 0755 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicpreprocessor
	%__install -p -m 0755 "$1"/src/dynamic-plugins/sf_engine/.libs/libsf_engine.so.0 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicengine
	%__ln_s -f %{_libdir}/%{realname}-%{version}_dynamicengine/libsf_engine.so.0 $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicengine/libsf_engine.so
	%__install -p -m 0755 "$1"/src/dynamic-preprocessors/build%{_prefix}/lib/snort_dynamicpreprocessor/*.so* $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicpreprocessor
	
    for file in $RPM_BUILD_ROOT%{_libdir}/%{realname}-%{version}_dynamicpreprocessor/*.so;  do  
          preprocessor=`basename $file`
          %__ln_s -f %{_libdir}/%{realname}-%{version}_dynamicpreprocessor/$preprocessor.0 $file     
    done   
	
	%__install -p -m 0644 snort.8 $RPM_BUILD_ROOT%{_mandir}/man8

	%__rm -rf $RPM_BUILD_ROOT%{_mandir}/man8/snort.8.gz
	%__gzip $RPM_BUILD_ROOT%{_mandir}/man8/snort.8
	%__install -p -m 0755 rpm/snortd $RPM_BUILD_ROOT%{_initrddir}
	%__install -p -m 0644 rpm/snort.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{realname}
	%__install -p -m 0644 rpm/snort.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/snort
	%__install -p -m 0644 etc/reference.config etc/classification.config \
		etc/unicode.map etc/gen-msg.map \
		etc/threshold.conf etc/snort.conf \
		$RPM_BUILD_ROOT%{_sysconfdir}/snort
	find doc -maxdepth 1 -type f -not -name 'Makefile*' -exec %__install -p -m 0644 {} $RPM_BUILD_ROOT%{_docdir}/%{realname}-%{version} \;

	%__rm -f $RPM_BUILD_ROOT%{_docdir}/%{realname}-%{version}/Makefile.*
   fi
   if [ "$1" = "openappid" ]; then
	%__install -p -m 0755 "$1"/tools/u2openappid/u2openappid $RPM_BUILD_ROOT%{_bindir}/u2openappid
	# This isn't built, it has to be copied from the source tree
        %__install -p -m 0755 tools/appid_detector_builder.sh $RPM_BUILD_ROOT%{_bindir}/appid_detector_builder.sh
   fi
}

# Fix the RULE_PATH
%__sed -e 's;var RULE_PATH ../rules;var RULE_PATH %{SnortRulesDir};' \
	< etc/snort.conf > etc/snort.conf.new
%__rm -f etc/snort.conf
%__mv etc/snort.conf.new etc/snort.conf

# Fix dynamic-preproc paths
%__sed -e 's;dynamicpreprocessor directory \/usr\/local/lib\/snort_dynamicpreprocessor;dynamicpreprocessor directory %{_libdir}\/%{realname}_dynamicpreprocessor;' < etc/snort.conf > etc/snort.conf.new
%__rm -f etc/snort.conf
%__mv etc/snort.conf.new etc/snort.conf

# Fix dynamic-engine paths
%__sed -e 's;dynamicengine \/usr\/local/lib\/snort_dynamicengine;dynamicengine %{_libdir}\/%{realname}_dynamicengine;' < etc/snort.conf > etc/snort.conf.new
%__rm -f etc/snort.conf
%__mv etc/snort.conf.new etc/snort.conf

%if %{OpenAppID}
  InstallSnort openappid
%else
  InstallSnort plain
%endif

cd $RPM_BUILD_ROOT/%{_libdir}
ln -s %{realname}-%{version}_dynamicpreprocessor %{realname}_dynamicpreprocessor
ln -s %{realname}-%{version}_dynamicengine       %{realname}_dynamicengine

%clean
%__rm -rf $RPM_BUILD_ROOT


%pre
# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
	/usr/sbin/groupadd snort 2> /dev/null || true
	/usr/sbin/useradd -M -d %{_var}/log/snort -s %{noShell} -c "Snort" -g snort snort 2>/dev/null || true
fi

%post
# Make a symlink if there is no link for snort-plain
%if %{OpenAppID}
  if [ -L %{_sbindir}/snort ] || [ ! -e %{_sbindir}/snort ] ; then \
    %__rm -f %{_sbindir}/snort; %__ln_s %{_sbindir}/%{name} %{_sbindir}/snort; fi
%else
  if [ -L %{_sbindir}/snort ] || [ ! -e %{_sbindir}/snort ] ; then \
    %__rm -f %{_sbindir}/snort; %__ln_s %{_sbindir}/%{name}-plain %{_sbindir}/snort; fi
%endif

# We should restart it to activate the new binary if it was upgraded
%{_initrddir}/snortd condrestart 1>/dev/null 2>/dev/null

# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
	%__chown -R snort.snort %{_var}/log/snort
	/sbin/chkconfig --add snortd
fi


%preun
if [ $1 = 0 ] ; then
	# We get errors about not running, but we don't care
	%{_initrddir}/snortd stop 2>/dev/null 1>/dev/null
	/sbin/chkconfig --del snortd
fi

%postun
# Try and restart, but don't bail if it fails
if [ $1 -ge 1 ] ; then
	%{_initrddir}/snortd condrestart  1>/dev/null 2>/dev/null || :
fi

# Only do this if we are actually removing snort
if [ $1 = 0 ] ; then
	if [ -L %{_sbindir}/snort ]; then
		%__rm -f %{_sbindir}/snort
	fi

	/usr/sbin/userdel snort 2>/dev/null
fi

%files
%defattr(-,root,root)
%if %{OpenAppID}
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_bindir}/u2openappid
%attr(0755,root,root) %{_bindir}/appid_detector_builder.sh
%else
%attr(0755,root,root) %{_sbindir}/%{name}-plain
%endif
%attr(0755,root,root) %{_bindir}/snort_control
%attr(0755,root,root) %{_bindir}/u2spewfoo
%attr(0755,root,root) %{_bindir}/u2boat
%attr(0644,root,root) %{_mandir}/man8/snort.8.*
%attr(0755,root,root) %dir %{SnortRulesDir}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/classification.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/reference.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/threshold.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/*.map
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/snort
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/snort/snort.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/snort
%attr(0755,root,root) %config(noreplace) %{_initrddir}/snortd
%attr(0755,snort,snort) %dir %{_var}/log/snort
%attr(0755,root,root) %dir %{_sysconfdir}/snort
%attr(0644,root,root) %{_docdir}/%{realname}-%{version}/*
%attr(0755,root,root) %dir %{_libdir}/%{realname}-%{version}_dynamicengine
%attr(0755,root,root) %{_libdir}/%{realname}-%{version}_dynamicengine/libsf_engine.*
%attr(0755,root,root) %dir %{_libdir}/%{realname}-%{version}_dynamicpreprocessor
%attr(0755,root,root) %{_libdir}/%{realname}-%{version}_dynamicpreprocessor/libsf_*_preproc.*
%{_libdir}/%{realname}_dynamicengine
%{_libdir}/%{realname}_dynamicpreprocessor

%dir %{_docdir}/%{realname}-%{version}
%docdir %{_docdir}/%{realname}-%{version}

################################################################
# Thanks to the following for contributions to the Snort.org SPEC file:
#	Henri Gomez <gomez@slib.fr>
#	Chris Green <cmg@sourcefire.com>
#	Karsten Hopp <karsten@redhat.de>
#	Tim Powers <timp@redhat.com>
#	William Stearns <wstearns@pobox.com>
#	Hugo van der Kooij <hugo@vanderkooij.org>
#	Wim Vandersmissen <wim@bofh.be>
#	Dave Wreski <dave@linuxsecurity.com>
#	JP Vossen <jp@jpsdomain.org>
#	Daniel Wittenberg <daniel-wittenberg@starken.com>
#	Jeremy Hewlett <jh@sourcefire.com>
#	Vlatko Kosturjak <kost@linux.hr>

%changelog
* Wed Dec  1 2021 Lawrence R. Rogers <lrr@cert.org> 2.9.19.0-1
- Release 2.9.19.0-1
	https://blog.snort.org/2021/12/open-source-version-of-snort-29190.html

	* src/snort.c :
	  Fixed an issue where verdict will be applied onto next session when timeout occurs in some scenarios.	  
	* rc/file-process/file_service.c :
	  Removed an excessively flooding log.
	* src/dynamic-preprocessors/modbus/modbus_decode.c :
	  Fixed possible integer overflow.
	* src/fpcreate.c :
	  Added fix to GCC compiled snort to use AC-BNFA-Q search-method when Intel-cpm is enabled.
	* src/generators.h
	  src/preprocessors/Stream6/snort_stream_tcp.c :
	  Added fix to not to drop packets when window size is 0 by TCP normalizer and Added new alert with GID 129 and SID 21 when such packets are seen.
	* src/dynamic-preprocessors/appid/detector_plugins/detector_imap.c
	  src/dynamic-preprocessors/appid/detector_plugins/detector_pop3.c :
	  Added support for Appid to detect login success and failure for IMAP and POP3 protocols.
	* src/dynamic-preprocessors/reputation/reputation_config.c
	  src/dynamic-preprocessors/reputation/spp_reputation.c
	  src/dynamic-preprocessors/reputation/spp_reputation.h
	  src/pkt_tracer.c
	  src/snort.c
	  src/util.c :
	  Fixed terminology to be bias-free in log/error messages.
	* src/snort.c :
	  Fixed a potential race condition.

* Tue Aug 17 2021 Lawrence R. Rogers <lrr@cert.org> 2.9.18.1-1
- Release 2.9.18.1-1
	* snort/src/dynamic-preprocessors/dcerpc2/dce2_smb.c:
	  Fixed possible memory corruption in SMB preprocessor.

* Tue Jun 15 2021 Lawrence R. Rogers <lrr@cert.org> 2.9.18-1
- Release 2.9.18-1

	* src/file-process/file_service.c,
	  src/generators.h,
	  src/preprocessors/HttpInspect/event_output/hi_eo_log.c,
	  src/preprocessors/HttpInspect/include/hi_eo_events.h,
	  src/preprocessors/HttpInspect/server/hi_server.c,
	  src/preprocessors/snort_httpinspect.c,
	  src/preprocessors/snort_httpinspect.h :
	  Added range field support in HTTP preprocessor.

	* src/preprocessors/HttpInspect/client/hi_client.c :
	  Added alert for http chunk size mismatch.

	* src/detection-plugins/detection_leaf_node.c :
	  Fixed a condition in which alert would not be generated.

	* src/dynamic-preprocessors/appid/service_plugins/service_snmp.c :
	  Added support to detect snmp 'report pdu'.

	* src/dynamic-preprocessors/dcerpc2/dce2_paf.c,
	  src/dynamic-preprocessors/dcerpc2/dce2_smb.h :
	  Fixed possible memory corruption in smb preprocessor.

	* src/preprocessors/Stream6/snort_stream_icmp.c,
	  src/preprocessors/Stream6/stream_common.h,
	  src/preprocessors/spp_stream6.c :
	  Fixed handling ICMP error code -4.

	* src/dynamic-preprocessors/dcerpc2/dce2_memory.c,
	  src/dynamic-preprocessors/dcerpc2/spp_dce2.c,
	  src/memory_stats.c :
	  Added additional stats for SMB preprocessor.

	* src/dynamic-preprocessors/appid/appInfoTable.c :
	  Fixed an error when debugmsgs option enabled in compilation.

* Fri Mar 19 2021 Lawrence R. Rogers <lrr@cert.org> 2.9.17.1-1
- Release 2.9.17.1-1
	* src/preprocessors/Stream6/snort_stream_tcp.c : Fixed wrong reference to configuration during reload.

	* src/dynamic-preprocessors/appid/fw_appid.c : Fixed possible memleak in appid.
	
	* src/detect.c, src/preprocessors/snort_httpinspect.c : Fixed a race-condition in http preproc and IPS.

	* configure.in : Fixed compilation issues when intel-soft-cpm is enabled.

	* src/preprocessors/Stream6/snort_stream_tcp.c, src/preprocessors/Stream6/stream_common.h, src/preprocessors/spp_stream6.c : Fixed a race-condition in stream preproc.

* Thu Dec 17 2020 Lawrence R. Rogers <lrr@cert.org> 2.9.17.0-2
- Release 2.9.17.0-2
	Added symlinks where:
		*  /usr/lib64/snort_dynamicpreprocessor points to /usr/lib64/snort-%{version}_dynamicpreprocessor 
		*  /usr/lib64/snort_dynamicengin points to /usr/lib64/snort-%{version}_dynamicengin 
	And the distributed snort.conf file uses the generic name instead of the version-specific name.

* Fri Oct 30 2020 Lawrence R. Rogers <lrr@cert.org> 2.9.17.0-1
- Release 2.9.17.0-1
	New Additions
		Added support for s7Commplus protocol.
		Support for allowing common names across rule options.
		Added support to detect TCP Fast Open packets. 
	Improvements / Fix
		Added support for HTTP range field parsing to detect if HTTP response/request is indeed partial or full content.
		Fixed TCP segment queue hole issue as per the RFC793 recommendation for OOO Ack packet handling.
		Fixed multiple static analysis issues.
		Miscellaneous SMB bug fixes.

* Mon Aug 24 2020 Lawrence R. Rogers <lrr@cert.org> 2.9.16.1-2
- Release 2.9.16.1-2
	Version 2.9.16.1 enables OpenAppID by default and it needs to be explicitly disabled.

* Fri Jul 24 2020 Lawrence R. Rogers <lrr@cert.org> 2.9.16.1-1
- Release 2.9.16.1-1
	New Additions
		Added support for GCC version 10.1.1.
	Improvements / Fix
		Added packet counters to make sure flows with one-way data don't pend forever.
		Fixed potential race condition between reload and exit path.

* Mon Apr 13 2020 Lawrence R. Rogers <lrr@cert.org> 2.9.16-1
- Release 2.9.16-1
	New Additions
		Added support for early inspection of HTTP payload before flushing in pre-ack mode.
		  This feature can be enabled using fast_blocking in http inspect configuration.
		Added 64-bit support for Windows 10 operating system.
		Added support for glibc version 2.30.
	Improvements and fixes
		Fixed file policy not working with character prefix in chunk size.
		Updated the file magic to detect ALZ file types.
		Addressed an issue when out-of-order FIN is received by dropping it.
		Normalize randomly encoded nulls interspersed in the HTTP server response to UTF-8.

* Fri Mar 27 2020 Lawrence R. Rogers <lrr@cert.org> 2.9.15.1-2
- Release 2.9.15.1-2
	Added PF_Ring support for CentOS/RHEL 8.

* Sun Dec 15 2019 Lawrence R. Rogers <lrr@cert.org> 2.9.15.1-1
- Release 2.9.15.1-1
	New Additions
		Added support for glibc version 2.30.
	Improvements / Fix
		Fixed snort core seen during ssl re-configuration.
		Fixed file access issues on files from SMB share.

* Thu Oct 10 2019 Lawrence R. Rogers <lrr@cert.org> 2.9.15-1
- Release 2.9.15-1
	 New Additions
		Added new debugs to print detection, file_processing and Preproc time consumption info and verdict.
		Added support to detect new Korean file formats .egg and .alg in the file preprocessor.
		Added support to detect new RAR file-type in the file preprocessor.
	Improvements / Fix
		Fix to generate ALERT if TEID value is zero in GTP v1 and v2 packets.
		Fix to whitelist ftp data sessions when no file policy exists.
		Fix RTF file magic to a more generic value to prevent evasions.
		Added debug logs during HTTP reload
		Added rule SID check during validation
		Fix an issue where HTTP was processing non-HTTP traffic on port 443
		Added new debugs to print detection, file processing, and Prepro time consumption info and verdicts

* Fri Aug  2 2019 Lawrence R. Rogers <lrr@cert.org> 2.9.14.1-1
- Release 2.9.14.1-1
	New Additions
		Added support for wild card port numbers in host cache and overwriting port service AppId.
		Added support for new STLS client patterns to help better detect POP3S over SSL.
		Added support for detecting Mac based SMTP Microsoft Outlook client application.
		Added a new preprocessor alert 120:27 to alert if there is no proper end of header.
	Improvements / Fix
		Improved appId detection for proxied traffic.
		Fix for enabling flow profiling mode without restarting snort detection engine.
		Fixed packet drop scenario.

* Mon Apr 22 2019 Lawrence R. Rogers <lrr@cert.org> 2.9.13.0-1
- Release 2.9.13.0-1
	New Additions
		Snort now supports reload on snort rules update.
		Addition of a scenario to add a packet to blacklist verdict to ensure the new session will be allowed.
		Handled a new pre-processor alert in case of the improper end of t HTTP header.
	Improvements
		Modified the calculation of file hash for FTP/HTTP with offset values.
		Fixed portal authentication connection stuck in half closed state.
		Updated UDP global timeout for a non-standard port.

* Thu Oct 11 2018 Lawrence R. Rogers <lrr@cert.org> 2.9.12-1
- Release 2.9.12-1
	New Additions
		Parsing HTTP CONNECT to extract the tunnel IP and port information.
		Alerting and dechunking for chunked encoding in HTTP1.0 request and response.
	Improvements
		Fixed an issue where, if we have a junk line before HTTP response header, the header was wrongly parsed.
		Fixed GZIP evasions where an HTTP response with content-encoding:gzip contains a body that has a GZIP-related anomaly.
		Fixed an issue in certain scenarios where a BitTorrent pattern is seen only on the third packet of the session, causing us to miss our client detection.
		SMB improvements for file detection and processing.

* Mon Mar 19 2018 Lawrence R. Rogers <lrr@cert.org> 2.9.11.1-2
- Release 2.9.11.1-2
	Added PF Ring for CentOS 6 and 7 for the x86_64 architecture.

* Wed Dec  6 2017 Lawrence R. Rogers <lrr@cert.org> 2.9.11.1-1
- Release 2.9.11.1-1
	New Additions
		* Added support to block portscan. In addition to tracking the scanning packets, action(drop/sdrop/reject) will be taken for all the packets,
		  which means Snort will block the packet and generate logs.
		* Added support to re-evaluate reputation after reputation update for all flows except those that have already been blacklisted.

	Improvements
		* Fixed issue to detect RTP up to two SSRC switches in each traffic direction.
		* Fixed issues related to HTTP POST header flushing, calling file processing directly if it is not a multipart header and changes to avoid expensive
		  copy of segment data by not splitting them when flushing headers.
		* Fixed issue of triggering protocol sweep alert when there are multiple destinations from single source ip protocol scan.
		* Added changes to fix IP portscan for protocol other than ICMP and fixed issue of bad fragment size event not being generated for oversized packets.
		* Added changes to use raw data in case of PDF and SWF files during file processing for SHA calculation and Malware Cloud Lookup.
		* Fixed issue of correct session matching for TCP SYN packets without window scale option so that FTP data channels match the same rule as FTP control channels.
		* Fixed issue of applying new configuration in file inspection after Snort reload.

* Tue Sep  5 2017 Lawrence R. Rogers <lrr@cert.org> 2.9.11-1
- Release 2.9.11-1

	* src/build.h : updating build number to 125.

	* src/preprocessors/: spp_session.c, Stream6/snort_stream_tcp.c :
	  Fixed issue with updation of global IPS id before packet processing.

	* src/output-plugins/spo_unified2.c : 
	  Added changes to display AppId for IPv6 unified events.

	* src/: dynamic-preprocessors/Makefile.am,
	  reload-adjust/appdata_adjuster.c,
	  sfutil/sfmemcap.c, sfutil/sfmemcap.h : 
	  Fixed dynamic preprocessor compilation failure in OpenBSD platform.

	* src/: parser.c, snort.h, detection-plugins/sp_replace.c : 
	  Fixed issues while parsing rules in snort reload path.

	* src/: appIdApi.h, dynamic-preprocessors/appid/appId.h,
	  dynamic-preprocessors/appid/appIdApi.c,
	  dynamic-preprocessors/appid/appIdConfig.h,
	  dynamic-preprocessors/appid/appInfoTable.c,
	  dynamic-preprocessors/appid/flow.h,
	  dynamic-preprocessors/appid/fw_appid.c,
	  dynamic-preprocessors/appid/hostPortAppCache.c,
	  dynamic-preprocessors/appid/hostPortAppCache.h :
	  Added implementation of hostPortCache versioning for unknown flows in AppID to detect and block BitTorrent.

	* src/preprocessors/spp_normalize.c :
	  Fixed incorrect usage of snort configuration in snort reload path.

	* src/dynamic-preprocessors/appid/: flow.c, flow.h, fw_appid.c : 
	  Fixed issues with printing of messages for out-of-order packets.

	* src/: mempool.c, mempool.h, reg_test.h, reload.c,
	  control/sfcontrol.c, control/sfcontrol.h,
	  preprocessors/spp_session.c,
	  preprocessors/Stream6/snort_stream_tcp.c : 
	  Added support for forced allocation of TCP protocol memory pool after maximum limit is reached.

	* src/reload.c :
	  Fixed synchronisation issue during snort reload.  

	* src/sfutil/: sf_ip.h, sf_ipvar.c, sf_ipvar.h :
	  Added changes to improve performance of ipvar list comparison.

	* src/: dynamic-output/plugins/output_lib.h,
	  dynamic-output/plugins/output_plugin.c,
	  dynamic-preprocessors/dcerpc2/dce2_smb.c,
	  dynamic-preprocessors/dcerpc2/dce2_smb.h,
	  dynamic-preprocessors/dcerpc2/dce2_smb2.c,
	  dynamic-preprocessors/dcerpc2/spp_dce2.c,
	  dynamic-preprocessors/file/file_event_log.c,
	  file-process/file_api.h, file-process/file_service.c,
	  file-process/file_stats.c, file-process/file_stats.h,
	  sfutil/sf_textlog.c, sfutil/sf_textlog.h : 
	  Added support for storing filenames in unicode format for SMB protocol.

	* src/dynamic-preprocessors/appid/detector_plugins/detector_smtp.c : 
	  Enhanced SMTP client detection by allowing line folding and all authentication methods.

	* src/: fpcreate.c, sfutil/sfthd.c, sfutil/sfxhash.c :
	  Fixed issue in detection filter counter when rule is used in multiple configurations.

* Wed Dec 14 2016 Lawrence R. Rogers <lrr@cert.org> 2.9.9.0-1
- Release 2.9.9.0-1

	New additions
	 *  New rule option for byte_math. See the Snort manual for details.
	 *  Added bitmask and from_end operations to byte_test. See the Snort manual for details.
	 *  Added a Buffer Dump utility to trace all of the buffers used by snort during inspection.
	    Enable this by --enable-buffer-dump option to configure prior to building. See the Snort manual for details.
	 *  Added new HTTP preprocessor alerts to detect multiple content encoding and multiple content length.
	 *  Added support for SMTP Traffic detection over SSL (SMTPS).
	Improvements
	 *  Fixed an issue which reduces extra service discovery to improve performance.
	 *  Fixed multiple issues in AppID.
	      - Reconstructed the call to port-service detection.
	      - Fixed issue where AppId for Facebook over SPDY/HTTP 1.1 was incorrect.
	      - Preventing third-party application identification for expected connections.
	 *  Stability improvement for Stream preprocessor. 
	      - Addressed incorrect flushing of packets whose size is greater than MAXIMUM_PAF_MAX.
	      - Fixed an issue where incorrect length argument in memcpy caused out of bound memory access.
	 *  Fixed multiple issues in HttpInspect preprocessor.
	      - Handling chunk encoding followed by \r\r\r\n and \n\n\n\r\r\n.
	      - Fixed an issue with LZMA flash decompression.
	 *  Fixed mime data processing issue in SMTP stateless inspection.
	 *  Added support to decode packets that contains VLAN with Secure Group Tag (SGT).
	 *  Fixed Issue related to DLL-Load in Snort on windows platforms for CVE-2016-1417. 

* Tue Apr 26 2016 Lawrence R. Rogers <lrr@cert.org> 2.9.8.3-1
- Release 2.9.8.3-1

	2016-04-26 Rahul Burman <rahburma@cisco.com>
	Snort 2.9.8.3
	* src/build.h: updating build number to 383
	* configure.in, src/preprocessors/HttpInspect/server/hi_server.c:
	  Modified Http header parsing of multiline content-encoding header.
	* src/preprocessors/: snort_httpinspect.c,
          HttpInspect/server/hi_server.c:
          Fixed an issue where file position pointer was incorrectly set for HTTP response
          containing chunked and gzip data.
        * src/preprocessors/Stream6/: snort_stream_tcp.c
          Added sanity check to TCP trimming in out-of-order FIN case.
        * src/parser.c:
          Disabled port groups that are not useful unless adapative profiling is enabled.
        * src/: dynamic-preprocessors/sdf/spp_sdf.c, obfuscation.c:
          Fixed an issue of incorrect masking of sensitive data.

	2016-03-18 Gaurav Nagare <gnagare@cisco.com>
	Snort 2.9.8.2
	* src/build.h: updating build number to 335
	* src/dynamic-plugins/: sf_engine/examples/detection_lib_meta.h,
	  sf_dynamic_meta.h:
          Updated detection API version to 2.6 to use the latest snort SO rules.
        * src/: dynamic-preprocessors/sdf/spp_sdf.c,
	  preprocessors/Stream6/snort_stream_tcp.c, obfuscation.c:
          Fixed several issues with SDF and obfuscation.
	* src/: profiler.h, preprocessors/perf_indicators.c,
	  preprocessors/perf_indicators.h: 
          Resolved snort build issue with "--disable-perfprofiling" configure 
          option.
	* src/: decode.c, decode.h: 
          Added Double VLAN tagging support.
	* src/file-process/file_mime_process.c:
          Enhanced mime parsing by adding support for detecting files
          after unknown headers and no headers.
	* src/preprocessors/HttpInspect/server/hi_server.c:
          Fixed memory leak.
        * src/preprocessors/HttpInspect/utils/hi_paf.c:
          Fixed issue with gzip decompression. If the server response specifies
          Content-Encoding as GZIP, but no Content-Length field for HTTP version 1.0.
	* doc/snort_manual.pdf, src/preprocessors/snort_httpinspect.c,
	  src/preprocessors/spp_httpinspect.c:
          Fixed Snort memory leak in parsing HTTP xff options.
	* src/preprocessors/spp_httpinspect.c: 
          Fixed Coverity issues.
	* src/preprocessors/: snort_httpinspect.c, snort_httpinspect.h,
	  HttpInspect/include/hi_paf.h, HttpInspect/server/hi_server.c,
	  HttpInspect/utils/hi_paf.c: 
          Improved End of Header(EOH) identification for response header spanning multiple
	  reassembled packets.
	* src/preprocessors/: HttpInspect/utils/hi_paf.c,
	  Stream6/snort_stream_tcp.c, Stream6/stream_paf.c:
	  Improved packet reassembly for HTTP, added code to purge segment correctly when 
	  PAF decides to ignore packet upon reaching paf_max.
        * src/fpdetect.c:
          Fixed to use outer header callback functions when checking IP rule against outer IPs 
	  and inner header callback when checking against inner IPs.
        * src/preprocessors/spp_httpinspect.c:
          Fixed an issue where http_inspect current and default config had 
          different file depth.
        * src/dynamic-preprocessors/appid/detector_plugins/detector_dns.c:
          Handled malformed DNS host in AppId.
        * src/file-process/: file_api.h, file_segment_process.c, file_service.c:
          Prevented access to file contexts which are pruned when memcap is 
          reached.
        * src/dynamic-preprocessors/appid/: app_forecast.c, app_forecast.h,
          flow.h, fw_appid.c, spp_appid.c, thirdparty_appid_types.h:
          Performance improvements to AppID.
        * src/dynamic-preprocessors/appid/luaDetectorApi.c:
          Created a future-flow API for lua detector.
          Exposed DNS API to lua detector.
        * src/dynamic-preprocessors/ftptelnet/pp_ftp.c:
          Fixed an issue where unexpected SSL negotiation starts for FTP
          with explicit SSL.
        * src/preprocessors/HttpInspect/utils/hi_paf.c:
          Updated HTTP PAF to accept all tokens between method and version
          string in request URI.
	* src/preprocessors/HttpInspect/files/file_decomp_SWF.c:
	  Fixed Flash LZMA decompression issue.
	* src/preprocessors/spp_httpinspect.c:
	  Fixed file_depth intialization issue during Snort reload. 

* Tue Nov 17 2015 Lawrence R. Rogers <lrr@cert.org> 2.9.8.0-1
- Release 2.9.8.0-1
	[*] New additions
	 *  SMBv2/SMBv3 support for file inspection.
	 *  Port override for metadata service in IPS rules.
	 *  AppID Lua detector performance profiling.
	 *  Perfmon dumps stats at fixed intervals from absolute time.
	 *  New preprocessor alert (120:18) to detect SSH tunneling over HTTP
	 *  New config option |disable_replace| to disable replace rule option.
	 *  New Stream configuration |log_asymmetric_traffic| to control logging to syslog.
	 *  New shell script in tools to create simple Lua detectors for AppID.
	[*] Improvements
	 *  sfip_t refactored to use struct in6_addr for all ip addresses.
	 *  Post-detection callback for preprocessors.
	 *  AppID support for multiple server/client detectors evaluating on same flow.
	 *  AppID API for DNS packets.
	 *  Memory optimizations throughout.
	 *  Support sending UDP active responses.
	 *  Fix perfmon tracking of pruned packets.
	 *  Stability improvements for AppID.
	 *  Stability improvements for Stream6 preprocessor.
	 *  Added improved support to block malware in FTP preprocessor.
	 *  Added support to differentiate between active and passive FTP connections.
	 *  Improvements done in Stream6 preprocessor to avoid having duplicate packets 
	    in the DAQ retry queue.
	 *  Resolved an issue where reputation config incorrectly displayed 'blacklist' in
	    priority field even though 'whitelist' option was configured.
	 *  Added support for multiple expected sessions created per packet
	 *  Active response now supports MPLS

* Thu Aug 13 2015 Lawrence R. Rogers <lrr@cert.org> 2.9.7.6-1
- Release 2.9.7.6-1
    * src/build.h:
	  updating build number to 285

    * src/dynamic-preprocessors/reputation/reputation_config.c:
          Fixed unexpected behaviour in reputation config where blacklist is displayed
	  in priority field even though whitelist option is set [reported by Mike Cox].	

    * src/preprocessors/Stream6/snort_stream_tcp.c:
	  Fixed issue where XFF/ExtraData is not always logged when 'drop' rules trigger [reported by Mike Cox].
	  Fixed issue in TCP session deletion when being called from Stream5 HA.

    * src/: active.h, file-process/file_service.c:
	  ACTIVE_DROP is changed to ACTIVE_FORCE_DROP when file_verdict is pending.

    * src/dynamic-preprocessors/appid/fw_appid.c:
	  Fixed issue where openappid does not provide the Content-Type field for use with CHPAddAction.

    * doc/snort_manual.tex:
	  Corrected errors in snort_manual.tex [reported by Gabriel Corre].
	  
    * preproc_rules/preprocessor.rules
	  src/preprocessors/: session_api.h, snort_httpinspect.c,
	  HttpInspect/event_output/hi_eo_log.c, HttpInspect/include/hi_eo_events.h
	  Stream6/snort_stream_tcp.c:
	  Enhancement done to detect 'SSH tunneling over HTTP'.

    * src/sfutil/sfportobject.c:
	  Fixed Memory leaks [reported by Bill Parker].

    * doc/snort_manual.tex:
	  Corrected the information about unified2 record structure [reported by Avery Rozar].
	
    * etc/snort.conf, src/preprocessors/snort_httpinspect.c,
          src/preprocessors/snort_httpinspect.h,
          src/preprocessors/HttpInspect/client/hi_client.c,
          src/preprocessors/HttpInspect/server/hi_server.c,
          src/preprocessors/Stream6/stream_paf.c:
	  Fixed issue where original client IP in intrusion event is incorrectly
	  populated with XFF of the last GET request.

    * src/preprocessors/: snort_httpinspect.c, snort_httpinspect.h,
          HttpInspect/server/hi_server.c,
          snort_httpinspect.c, snort_httpinspect.h,
          HttpInspect/server/hi_server.c:
	  Http unlimited decompression will now decompress the entire stream.

    * src/decode.c:
	  Added a check so that min_ttl decoder do not drop packet in alert mode.
	  
    * etc/snort.conf, src/preprocessors/snort_httpinspect.c,
          src/preprocessors/snort_httpinspect.h,
          src/preprocessors/HttpInspect/client/hi_client.c,
          src/preprocessors/HttpInspect/server/hi_server.c
	  Fixed issue where original client IP in intrusion event is incorrectly populated with XFF of the last GET request.		

* Wed Jul  1 2015 Lawrence R. Rogers <lrr@cert.org> 2.9.7.5-1
- Release 2.9.7.5-1
    * src/build.h:
      updating build number to 262

    * src/preprocessors/Stream6/snort_stream_tcp.c: 
      Improved handling of asymmetric traffic

    * src/active.c: 
      Active responses no longer set the FIN flag on the last segment
      transmitted

    * src/dynamic-preprocessors/appid/luaDetectorApi.c:
      Added sanity checks to client api
      
    * doc/snort_manual.pdf,
      src/: dynamic-preprocessors/dcerpc2/dce2_paf.c,
      dynamic-preprocessors/dnp3/dnp3_paf.c,
      dynamic-preprocessors/ftptelnet/snort_ftptelnet.c,
      dynamic-preprocessors/imap/imap_paf.c,
      dynamic-preprocessors/pop/pop_paf.c,
      dynamic-preprocessors/sip/sip_paf.c,
      dynamic-preprocessors/smtp/smtp_paf.c,
      preprocessors/session_api.h, preprocessors/spp_stream6.c,
      preprocessors/stream_api.h,
      preprocessors/HttpInspect/utils/hi_paf.c,
      preprocessors/Session/session_common.h,
      preprocessors/Stream6/snort_stream_tcp.c,
      preprocessors/Stream6/snort_stream_tcp.h,
      preprocessors/Stream6/stream_paf.c,
      preprocessors/Stream6/stream_paf.h: 
      Multiple PAF clients can Read/Write to the same user data

    * src/: file-process/file_api.h, file-process/file_mail_common.h,
      file-process/file_mime_process.c,
      sfutil/sf_email_attach_decode.c, sfutil/sf_email_attach_decode.h: 
      Fixed filename parsing from Mime body for UUencoded MIME

    * src/preprocessors/perf-base.c,
      src/preprocessors/Stream6/snort_stream_tcp.c: 
      Prunes triggered by timeouts are now accounted by perfmonitor.

    * src/preprocessors/spp_session.c: 
      Log warning instead of Fatal Error
      if a stream5_global config is in a non-default policy
      
    * src/detection-plugins/sp_base64_decode.c: 
      Removed unused checks
      
    * src/snort.c:
      Improved reliability of configuration reloads

    * src/preprocessors/snort_httpinspect.c: 
      Fixed issue in http
      file processing where SHAs may not always be correct.

    * doc/snort_manual.pdf,
      src/sfutil/sf_email_attach_decode.c: 
      Fixed handling new line chars in QP encoding
      

    * src/preprocessors/snort_httpinspect.c: 
      Fixed inconsistent behavior when configuring "max_gzip_mem -1"

* Wed Apr 22 2015 Lawrence R. Rogers <lrr@cert.org> 2.9.7.3-1
- Release 2.9.7.3-1
    * src/build.h:
      updating build number to 217

    * src/: decode.h, detection-plugins/sp_clientserver.c,
      dynamic-plugins/sf_engine/sf_snort_packet.h,
      dynamic-plugins/sf_engine/sf_snort_plugin_api.c,
      dynamic-preprocessors/dcerpc2/dce2_session.h,
      dynamic-preprocessors/sdf/spp_sdf.c,
      preprocessors/HttpInspect/server/hi_server.c,
      preprocessors/Stream6/snort_stream_tcp.c,
      preprocessors/snort_httpinspect.c, preprocessors/spp_normalize.c:
      Added mode safety checks to normalization.
      Fixed an issue in PAF where the start of the PDU after flushing was not
      being set correctly in some case.
      Improved Stream reassembly of HTTPS sessions

    * src/dynamic-preprocessors/ftptelnet/snort_ftptelnet.c:
      Stability improvements for ftp_telnet preprocessor

    * doc/snort_manual.pdf, doc/snort_manual.tex,
      src/detection-plugins/sp_base64_decode.c,
      src/detection-plugins/sp_base64_decode.h,
      src/detection-plugins/sp_file_data.c:
      Improved performance for file preprocessor
      Documentation changes

    * src/dynamic-preprocessors/appid/: service_plugins/service_base.c,
      service_state.c:
      Various OpenAppId improvements

    * configure.in:
      Fixed issue with configure script handling of -Werror compiler flags

    * src/decode.c:
      Improved decoding of IPv6 extensions

    * src/detection-plugins/detection_options.c:
      Fixed an issue where the protected_content rule option was not
      backtracking correctly in some cases

    * src/snort.c:
      Fixed snort handling of PID files

    * tools/: u2openappid/u2openappid.c, u2spewfoo/u2spewfoo.c:
      Fixed usage info.

    * src/dynamic-preprocessors/sip/: Makefile.am, sf_sip.dsp, sip_dialog.c,
      sip_parser.c, spp_sip.c:
      Added PAF support for TCP traffic

    * src/: log_text.c, log_text.h, output-plugins/spo_alert_fast.c,
      output-plugins/spo_alert_full.c:
      Extended support for OpenAppId logging to cmg and console output loggers

    * src/dynamic-preprocessors/appid/service_plugins/service_ssl.c:
      Improved SSLv3 handling for OpenAppId

* Mon Mar 23 2015 Lawrence R. Rogers <lrr@cert.org> 2.9.7.2-2
- Release 2.9.7.2-2
	Added the following tools to /usr/bin
		u2openappid
		u2streamer
		snort_dump_packets_control

* Wed Dec 24 2014 Lawrence R. Rogers <lrr@cert.org> 2.9.7.2-1
- Release 2.9.7.2-1
	Snort 2.9.7.2
	    * src/build.h:
	      updating build number to 177

	    * src/preprocessors/Stream6/snort_stream_tcp.c:
	      Documentation: Fixed issue in which TCP trim normalization would occur when it was not necessary.

	    * src/decode.c, src/encode.c:
	      Added support for Cisco FabricPath decoding/encoding.
	      Ensure flow_id is copied into the DAQ_PktHdr_t.

	    * src/snort.h, src/sfutil/sfrt.c, src/sfutil/sfrt.h
	      src/target-based/sftarget_reader.c:
	      Moved ntohl conversion inside of the sfrt api for both IPv4 and IPv6.

	    * src/target-based/sftarget_protocol_reference.c
	      Lookup application protocol id only after the session is established.
	      Assign application protocol id to the session when using host attribute table.

	    * src/util.c:
	      Changes for suppressing configuration logging.

	    * src/file-process/file_service.c:
	      Assign the file config to a file context prior to checking if HTTP continuation.

* Fri Oct 10 2014 Lawrence R. Rogers <lrr@cert.org> 2.9.7.0-1
- Release 2.9.7.0-1
	See https://github.com/jasonish/snort/blob/master/ChangeLog for the list of changes.

* Wed Jul 09 2014 Lawrence R. Rogers <lrr@cert.org> 2.9.6.2-1
- Release 2.9.6.2-1
        * src/build.h:
          updating build number to 77

        * src/: encode.c, encode.h :
          Fixed handling of ICMPv6 traffic.

        * src/preprocessors/Stream5/snort_stream5_tcp.c :
          Fixed inline stream reassembly during file processing.

        * src/preprocessors/spp_perfmonitor.c :
          Fixed race condition in performance monitor.

        * src/preprocessors/:
          snort_httpinspect.c,
          HttpInspect/client/hi_client.c,
          HttpInspect/include/hi_client.h,
          HttpInspect/include/hi_ui_config.h,
          HttpInspect/user_interface/hi_ui_config.c :
          Added the ability to specify additional custom 'x-forwarder-for'
          http field names. A new http inspection configuration element is used to
          specify a set of field names and their respective precedence order.

        * src/preprocessors/Stream5/snort_stream5_session.c :
          Add cache flow timeout for ip.

* Thu Jul 03 2014 Dilbagh Chahal <dchahal@cisco.com> 2.9.7
- added --with openappid command line option

* Wed Apr 23 2014 Lawrence R. Rogers <lrr@cert.org> 2.9.6.1-1
- Release 2.9.6.1-1
	See http://www.snort.org/downloads/2895 for a list of changes.

* Mon Dec 30 2013 Lawrence R. Rogers <lrr@cert.org> 2.9.6.0-1
- Release 2.9.6.0-1
	See http://www.snort.org/downloads/2771 for a list of changes.

* Tue Sep 03 2013 Lawrence R. Rogers <lrr@cert.org> 2.9.5.5-1
- Release 2.9.5.5-1
	See http://www.snort.org/downloads/2539 for a list of changes.

* Wed Jul 03 2013 Lawrence R. Rogers <lrr@cert.org> 2.9.5.3-1
- Release 2.9.5.3-1
	See http://www.snort.org/downloads/2469 for a list of changes.

* Thu Apr 18 2013 Lawrence R. Rogers <lrr@cert.org> 2.9.4.6-1
- Release 2.9.4.6-1
    * src/build.h: 
      updating build number to 73

    * doc/README.counts, doc/snort_manual.pdf, doc/snort_manual.tex, src/decode.c, src/parser.c, src/snort.h: 
      Added config tunnel_verdicts and tunnel bypass for whitelist and blacklist verdicts for 6in4 or 4in6 encapsulated traffic.

    * src/preprocessors/spp_frag3.c: 
      Don't update IP options length and count in frag3 after allocating option buffer when receiving duplicate 0 offset fragments with IP options.

* Wed Apr 03 2013 Lawrence R. Rogers <lrr@cert.org> 2.9.4.5-1
- Release 2.9.4.5-1
    * src/build.h:
      updating build number to 71

    * src/preprocessors/Stream5/snort_stream5_tcp.c:
      prevent pruning when dup'ing a seglist node to avoid broken flushed packets

    * src/detection-plugins/detection_options.c:
      recursively search patterns within the HTTP uri buffers until the buffer ends.

    * src/preprocessors/HttpInspect/: client/hi_client.c,
      client/hi_client_norm.c, include/hi_client.h:
      Remove proxy information from the normalized URI buffer.  Thanks to L0rd Ch0de1m0rt for reporting the issue.

    * src/: control/sfcontrol.c, preprocessors/Stream5/snort_stream5_tcp.c:
      fix logging of unified2 packet data when alerting on a packet containing multiple HTTP PDUs

* Tue Feb 19 2013 Lawrence R. Rogers <lrr@cert.org> 2.9.4.1
- See http://www.snort.org/downloads/2209 for a list of changes.

* Wed May 09 2012 Todd Wease <twease@sourcefire.com> 2.9.3
- Removed --enable-decoder-preprocessor-rules since this is now the default
-	behavior and not configurable.

* Fri Apr 27 2012 Russ Combs <rcombs@sourcefire.com> 2.9.3
- Removed schemas related foo.

* Fri Mar 30 2012 Steve Sturges <ssturges@sourcefire.com> 2.9.3
- Removed --with flexresp, --with inline, database output specific builds.

* Wed Apr 02 2008 Steve Sturges <ssturges@sourcefire.com> 2.8.3
- Added --enable-targetbased --enable-decoder-preprocessor-rules by default.

* Wed Apr 02 2008 Steve Sturges <ssturges@sourcefire.com> 2.8.1
- Added ssl

* Fri Aug 03 2007 Russ Combs <rcombs@sourcefire.com> 2.8.0
- Removed README.build_rpms from description
- Removed 2nd "doc/" component from doc install path
- Changed doc file attributes to mode 0644
- Moved schemas from doc to data dir
- Added installation of schemas/create_*
- Removed redundant '/'s from mkdir path specs
- Eliminated find warning by moving -maxdepth ahead of -type
- Fixed "warning: File listed twice: ..." for libsf so files

* Wed Feb 28 2007 Steve Sturges <ssturges@sourcefire.com> 2.7.0
- Removed smp flags to make command

* Wed Jan 17 2007 Steve Sturges <ssturges@sourcefire.com> 2.7.0
- Updated version to 2.7.0

* Tue Nov 07 2006 Steve Sturges <ssturges@sourcefire.com> 2.6.0
- Updated version to 2.6.1 

* Thu Aug 31 2006 Steve Sturges <ssturges@sourcefire.com> 2.6.0
- Added dynamic DNS preprocessor

* Wed May 24 2006 Steve Sturges <ssturges@sourcefire.com> 2.6.0
- Updated to version 2.6.0

* Fri Apr 14 2006 Justin Heath <justin.heath@sourcefire.com> 2.6.0RC1
- Added conf fix for dynamic engine paths
- Added conf fix for dynamic preprocessors paths
- Added dynamic attributes in file list
- Added epoch to Requires for postgres, oracle and unixodbc
- Removed rule/signature references as these are not distributed with this tarball

* Thu Apr 13 2006 Steve Sturges <ssturges@sourcefire.com> 2.6.0RC1
- Updated to 2.6.0RC1
- Added targets for dynamic engine
- Added targets for dynamic preprocessors

* Sun Dec 11 2005 Vlatko Kosturjak <kost@linux.hr> 2.6.0RC1
- Added unixODBC support

* Sun Oct 16 2005 Marc Norton <mnorton@sourcefire.com> 2.4.3
- Fixed buffer overflow in bo preprocessor
- Added alert for potential buffer overflow attack against snort
- Added noalert and drop options for all bo preprocessor events

* Fri Jul 22 2005 Martin Roesch <roesch@sourcefire.com> 2.4.0
- Modified to reflect rules not being distributed with Snort distros

* Tue May 03 2005 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.4.0RC1
- Removed more Fedora-specific options 
- Renamed spec from snort.org.spec to snort.spec
- Removed CHANGES.rpms file since we have a changelog here no sense
-	in maintaining two of them
- Replaced a ton of program names with macros to make more portable
- Removed all references to rpms@snort.org since it just gets used
-	for spam so the address is being nuked
- Updates to inline support for 2.4.0 Release and fedora changes
- Replaced initDir with system-provided _initdir macro for more portability
- Added Epoch back in so that way upgrades will work correctly.  It will be
- 	removed at some point breaking upgrades for that version

* Tue Mar 29 2005 Jeremy Hewlett <jh@sourcefire.com>
- Added Inline capability to RPMs. Thanks Matt Brannigan
-        for helping with the RPM foo.

* Fri Mar 25 2005 Jeremy Hewlett <jh@sourcefire.com>
- Add schemas to rpm distro
- Add sharedscripts to logrotate
- Remove installing unnecessary contrib remnants

* Sun Mar 13 2005 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Updates to conform to new Fedora Packageing guidelines

* Wed Dec 1 2004 Jeff Ball <zeffie@zeffie.com>
- Added initDir and noShell for more building compatibility.

* Wed Nov 17 2004 Brian Caswell <bmc@snort.org> 2.3.0RC1
- handle the moving of RPM and the axing of contrib

* Thu Jun 03 2004 JP Vossen <jp@jpsdomain.org>
- Bugfix for 'snortd condrestart' redirect to /dev/null in %postun

* Wed May 12 2004 JP Vossen <jp@jpsdomain.org>
- Added code for cAos autobuilder
- Added buildrequires and requires for libpcap

* Thu May 06 2004 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Added JP's stats option to the standard rc script

* Sat Mar 06 2004 JP Vossen <jp@jpsdomain.org>
- Added gen-msg.map and sid-msg.map to /etc/snort

* Sat Feb 07 2004 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Applied postun/snortd patches from Nick Urbanik <nicku@vtc.edu.hk

* Mon Dec 22 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Added threshold.conf, unicode.map and generators to /etc/snort thanks
- 	to notes from Nick Urbanik <nicku@vtc.edu.hk>

* Sat Dec 20 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.1.0-2
- Added condrestart option to rc script from patch by
-       Nick Urbanik <nicku@vtc.edu.hk>
- Fixed condrestart bug for installs
- Fixed gzip bug that happens on some builds

* Wed Dec 10 2003 JP Vossen <jp@jpsdomain.org>
- Removed flexresp from plain rpm package description
- Added a line about pcre to the package description
- Trivial tweaks to package description

* Sat Nov 29 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.1.0-1
- Applied some updates from rh0212ms@arcor.de
- Applied some updates from Torsten Schuetze <torsten.schuetze@siemens.com>
- Applied some updates from Nick Urbanik <nicku@vtc.edu.hk>
- Fixed ALERTMODE rc script error reported by DFarino@Stamps.com
- Fixed CONF rc script error reported by ??
- Gzip signature files to save some space
- Added BuildRequires pcre-devel and Requires pcre
- Re-did %post <package> sections so the links are added and removed
-	correctly when you add/remove various packages 

* Fri Nov 07 2003 Daniel WIttenberg <daniel-wittenberg@starken.com> 
- Updated snort.logrotate

* Thu Nov 06 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.0.4
- Minor updates for 2.0.4

* Tue Nov 04 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.0.3
- Updated for 2.0.3
- Removed 2.0.2 patch
- Remove flexresp2 as it caused too many build problems and doesn't work
-       cleanly with 2.0.3 anyway
- Minor documentation updated for 2.0.3

* Mon Oct 20 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.0.2-6
- New release version
- Changed /etc/rc.d/init.d to /etc/init.d for more compatibility

* Fri Oct 17 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Changed as many hard-coded references to programs and paths to use
- 	standard defined macros

* Fri Oct 10 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Include SnortRulesDir in %%files section
- Added classification.config and reference.config in %%files section
- Minor cleanup of the for_fedora macro

* Sat Oct 04 2003 Dainel Wittenberg <daniel-wittenberg@starken.com> 
- Nuked post-install message as it caused too many problems
- Changed default ruledir to /etc/snort/rules
- Fixed problem with non-snort-plain symlinks getting created

* Fri Oct 03 2003 Dainel Wittenberg <daniel-wittenberg@starken.com> 
- Somehow the snort.logrotate cvs file got copied into the build tree
-	and the wrong file got pushed out
- snort.logrotate wasn't included in the %%files section, so added
-	it as a config(noreplace) file

* Thu Oct 02 2003 Dainel Wittenberg <daniel-wittenberg@starken.com> 2.0.2-5
- Added --with fedora for building Fedora RPM's
- Removed references to old snort config patch
- Added noreplace option to /etc/rc.d/init.d/snortd just in case
- Gzip the man page to save (a small tiny) amount of space and make it
-	more "standard"
- Added version number to changelog entries to denote when packages were
-       released

* Wed Oct 01 2003 Dainel Wittenberg <daniel-wittenberg@starken.com>
- Fixed permission problem with /etc/snort being 644
- Added noreplace option to /etc/sysconfig/snort

* Fri Sep 26 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Fixed incorrect Version string in cvs version of the spec
- Added snort logrotate file
- Removed |more from output as it confuses some package managers

* Tue Sep 23 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.0.2-4
- Released 2.0.2-3 and then 2.0.2-4

* Sat Sep 20 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Added --with flexresp2 build option

* Fri Sep 19 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.0.2-2
- Gave into JP and changed version back to stable :)

* Fri Sep 19 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Fixed problems in snortd with "ALL" interfaces working correctly
- Removed history from individual files as they will get too big
- 	and unreadable quickly

* Thu Sep 18 2003 Daniel Wittenberg <daniel-wittenberg@starken.com> 2.0.2-1
- Updated for 2.0.2 and release 2.0.2-1 

* Tue Aug 26 2003 JP Vossen <jp@jpsdomain.org>
- Added code to run autojunk.sh for CVS tarball builds

* Mon Aug 25 2003 JP Vossen <jp@jpsdomain.org>
- Added missing comments to changelog

* Wed Aug 20 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Moved snortd and snortd.sysconfig to contrib/rpm
- Changed contrib install to a cp -a so the build stops complaining

* Mon Aug 11 2003 JP Vossen <jp@jpsdomain.org>
- Removed the commented patch clutter and a TO DO note
- Fussed with white space

* Sun Aug 10 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- Fixed a couple minor install complaints
- userdel/groupdel added back into %%postun
- useradd/groupadd added to %%pre

* Sat Aug  9 2003 JP Vossen <jp@jpsdomain.org>
- Doubled all percent signs in this changelog due to crazy RH9 RPM bug.
-     http://www.fedora.us/pipermail/fedora-devel/2003-June/001561.html
-     http://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=88620
- Turn off rpm debug due to RH9 RPM issue
-     http://www.cs.helsinki.fi/linux/linux-kernel/2003-15/0763.html
- Removed unnecessary SourceX: since they will be in the tarball

* Thu Aug  7 2003 JP Vossen <jp@jpsdomain.org>
- Changed perms from 755 to 644 for %%{_mandir}/man8/snort.8*

* Sun Aug  3 2003 JP Vossen <jp@jpsdomain.org>
- Removed the conf patch (again) as we moved the funcationality
- Added sed to buildrequires and sed it to fix RULE_PATH
- Removed Dan's SPEC code that made a default sysconfig/snort file.

* Sun Aug  3 2003 JP Vossen <jp@jpsdomain.org>
- Trivial changes and additions to documentation and references
- Added --with flexresp option
- Changed libnet buildrequires per Chris
- Added docs and contrib back in, and moved sig docs out of doc.
- Moved CSV and signature 'fixes' into %%install where they should have
-     been. Also fixed them.
- Added Dan's new snortd and snort.sysconfig
- Commented out alternate method of creating /etc/sysconfig/snort
- Created %%{OracleHome}
- Added BuildRequires: findutils
- Uncommented the patch and added the patch file

* Sat Jul 26 2003 Daniel Wittenberg <daniel-wittenberg@starken.com>
- commented out the patch for now since it doesn't exist
- if doing a new install echo "INTERFACE=eth0" > /etc/sysconfig/snort
- changed --with-libpcap-includes=/usr/include/pcap to /usr/include since
-     that is where the libpcap-snort rpm Chris sent puts things
- added missing " at the end of the SNORT_BASE_CONFIG
- minor change to the ./configure for plain so it actually works
- during an rpm -e of snort do a rm -f to make it a little more quiet in
-     case of problems
- massive re-write of multi-package build system
- initial support for compiling with Oracle

* Sun Jul 20 2003 JP Vossen <jp@jpsdomain.org>
- Took over maintenance of Snort.org RPM releases just before v2.0.1
- Various cleanup of SPEC file and changes to support building from tarball
- Removed some old packages (like SNMP and Bloat), per Chris
- First attempt at using --with option for multi-package build system
- Added a patch to snort.conf for $RULE_PATH and default output plugins

* Wed Sep 25 2002 Chris Green <cmg@sourcefire.com>
- updated to 1.9.0

* Tue Nov  6 2001 Chris Green <cmg@uab.edu>
- merged in Hugo's changes
- updated to 1.8.3
- fixing symlinks on upgrades

* Tue Nov  6 2001 Hugo van der Kooij <hugo@vanderkooij.org>
- added libpcap to the list as configure couldn't find it on RedHat 7.2
- added several packages to the build requirements

* Fri Nov  2 2001 Chris Green <cmg@uab.edu>
- updated to 1.8.2-RELEASE
- adding SQL defines
- created tons of packages so that all popular snort configs are accounted for

* Sat Aug 18 2001 Chris Green <cmg@uab.edu>
- 1.8.1-RELEASE
- cleaned up enough to release to general public

* Tue May  8 2001 Chris Green <cmg@uab.edu>
- moved to 1.8cvs
- changed rules files
- removed initial configuration

* Mon Nov 27 2000 Chris Green <cmg@uab.edu>
- removed strip
- upgrade to cvs version
- moved /var/snort/dev/null creation to install time

* Tue Nov 21 2000 Chris Green <cmg@uab.edu>
- changed to %%{SnortPrefix}
- upgrade to patch2

* Mon Jul 31 2000 Wim Vandersmissen <wim@bofh.st>
- Integrated the -t (chroot) option and build a /home/snort chroot jail
- Installs a statically linked/stripped snort
- Updated /etc/rc.d/init.d/snortd to work with the chroot option

* Tue Jul 25 2000 Wim Vandersmissen <wim@bofh.st>
- Added some checks to find out if we're upgrading or removing the package

* Sat Jul 22 2000 Wim Vandersmissen <wim@bofh.st>
- Updated to version 1.6.3
- Fixed the user/group stuff (moved to %%post)
- Added userdel/groupdel to %%postun
- Automagically adds the right IP, nameservers to /etc/snort/rules.base

* Sat Jul 08 2000 Dave Wreski <dave@linuxsecurity.com>
- Updated to version 1.6.2
- Removed references to xntpd
- Fixed minor problems with snortd init script

* Fri Jul 07 2000 Dave Wreski <dave@linuxsecurity.com>
- Updated to version 1.6.1
- Added user/group snort

* Sat Jun 10 2000 Dave Wreski <dave@linuxsecurity.com>
- Added snort init.d script (snortd)
- Added Dave Dittrich's snort rules header file (ruiles.base)
- Added Dave Dittrich's wget rules fetch script (check-snort)
- Fixed permissions on /var/log/snort
- Created /var/log/snort/archive for archival of snort logs
- Added post/preun to add/remove snortd to/from rc?.d directories
- Defined configuration files as %%config

* Tue Mar 28 2000 William Stearns <wstearns@pobox.com>
- Quick update to 1.6.
- Sanity checks before doing rm-rf in install and clean

* Fri Dec 10 1999 Henri Gomez <gomez@slib.fr>
- 1.5-0 Initial RPM release

