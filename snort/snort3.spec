# $Id: snort3.spec,v 1.23 2022/09/27 10:40:18 repoman Exp repoman $
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

%if %{OpenAppID}
  %define EnableOpenAppId --enable-open-appid
%endif

%if %{OpenAppID}
Name: %{realname}-openappid
Version: 3.1.42.0
Summary: An open source Network Intrusion Detection System (NIDS) with open AppId support
Conflicts: %{realname}
Obsoletes: %{realname}-openappid < 3.0.0.0
BuildRequires: luajit-devel libnghttp2-devel

%if 0%{?fedora} >= 26
BuildRequires: compat-openssl10-devel
%else
BuildRequires: openssl-devel
%endif

Source1: %{realname}-openappid.tar.gz

%else

Name: %{realname}
Version: 3.1.42.0
Summary: An open source Network Intrusion Detection System (NIDS)
Conflicts: %{realname}-openappid
Obsoletes: %{realname} < 3.0.0.0
BuildRequires:	libpcap-devel
BuildRequires:	pcre-devel
BuildRequires:	libdnet-devel
BuildRequires:	hwloc-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	luajit-devel
BuildRequires:	pkgconfig
BuildRequires:	libmnl-devel
BuildRequires:	libunwind-devel
BuildRequires:	xz-devel
BuildRequires:	libuuid-devel
BuildRequires:	hyperscan-devel

%if 0%{?centos} != 8
BuildRequires:	flatbuffers-devel
%endif

BuildRequires:	libsafec libsafec-devel
BuildRequires:	gperftools-devel
BuildRequires:	cmake
%endif

BuildRequires:	gcc-c++
Epoch: 1
Release: %{release}%{?dist}
Group: Applications/Internet
License: GPL
Url: http://www.snort.org/
Source0: https://www.snort.org/downloads/snort/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0
%if 0%{?centos} == 8
%ifarch x86_64
Patch2:	%{realname}-%{version}-patch-002
%endif
%endif
%endif

Packager: Official Snort.org %{for_distro}
Vendor: %{vendor}
BuildRequires: autoconf automake pcre-devel libpcap-devel libdnet-devel zlib-devel flex bison libnfnetlink-devel libnetfilter_queue-devel
BuildRequires: daq-devel >= 3.0.0
%if 0%{?fedora} >= 28 || 0%{?centos} >= 8
BuildRequires: libtirpc-devel
%endif
BuildRequires:	gcc-c++

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
%setup -q -n %{realname}3-%{version}
%if 0
%if 0%{?centos} == 8
%ifarch x86_64
%patch2 -p1
%endif
%endif
%endif

%build
#sudo ln -s /usr/lib64/pkgconfig/safec-3.3.pc %{_prefix}/lib64/pkgconfig/libsafec.pc
sh configure_cmake.sh --prefix=%{_prefix} --enable-tcmalloc --enable-safec \
%if 0
%if 0%{?centos} == 8
%ifarch x86_64
	--with-libpfring-includes=/usr/local/include/ \
	--with-libpfring-libraries=/usr/local/lib \
	--with-libpcap-includes=/usr/include/ \
	--with-libpcap-libraries=/usr/lib \
%endif
%endif
%endif

cd build
%__make -j$(nproc)
#sudo rm %{_prefix}/lib64/pkgconfig/libsafec.pc

%install
cd build
%__make -j$(nproc) DESTDIR=%{buildroot} install

%clean
%__rm -rf $RPM_BUILD_ROOT

%pre
# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
	/usr/sbin/groupadd %{realname} 2> /dev/null || true
	/usr/sbin/useradd -M -d %{_var}/log/%{realname} -s %{noShell} -c "Snort" -g %{realname} %{realname} 2>/dev/null || true
fi

%post
# Make a symlink if there is no link for snort-plain
%if %{OpenAppID}
  if [ -L %{_sbindir}/%{realname} ] || [ ! -e %{_sbindir}/%{realname} ] ; then \
    %__rm -f %{_sbindir}/%{realname}; %__ln_s %{_sbindir}/%{name} %{_sbindir}/%{realname}; fi
%else
  if [ -L %{_sbindir}/%{realname} ] || [ ! -e %{_sbindir}/%{realname} ] ; then \
    %__rm -f %{_sbindir}/%{realname}; %__ln_s %{_sbindir}/%{name}-plain %{_sbindir}/%{realname}; fi
%endif

# We should restart it to activate the new binary if it was upgraded
%{_initrddir}/%{realname}d condrestart 1>/dev/null 2>/dev/null

# Don't do all this stuff if we are upgrading
if [ $1 = 1 ] ; then
	%__chown -R %{realname}.%{realname} %{_var}/log/%{realname}
	/sbin/chkconfig --add %{realname}d
fi


%preun
if [ $1 = 0 ] ; then
	# We get errors about not running, but we don't care
	%{_initrddir}/%{realname}d stop 2>/dev/null 1>/dev/null
	/sbin/chkconfig --del %{realname}d
fi

%postun
# Try and restart, but don't bail if it fails
if [ $1 -ge 1 ] ; then
	%{_initrddir}/%{realname}d condrestart  1>/dev/null 2>/dev/null || :
fi

# Only do this if we are actually removing snort
if [ $1 = 0 ] ; then
	if [ -L %{_sbindir}/%{realname} ]; then
		%__rm -f %{_sbindir}/%{realname}
	fi

	/usr/sbin/userdel %{realname} 2>/dev/null
fi

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root)	%{_bindir}/*
%attr(0644,root,root)	%{_prefix}/etc/%{realname}/*.lua
%attr(0644,root,root)	%{_prefix}/etc/%{realname}/file_magic.rules
%attr(0644,root,root)	%{_includedir}/%{realname}/*/*.h
%attr(0644,root,root)	%{_includedir}/%{realname}/*/*.lua
%attr(0644,root,root)	%{_includedir}/%{realname}/*/*/*.h
%attr(0644,root,root)	%{_defaultdocdir}/%{realname}/*
%attr(0644,root,root)	%{_libdir}/pkgconfig/%{realname}.pc
%attr(0644,root,root)	%{_libdir}/%{realname}/daq/*.so

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
* Mon Sep 26 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.42.0-1
- Release 3.1.42.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.42.0 for the list of changes

* Fri Sep  9 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.41.0-1
- Release 3.1.41.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.41.0 for the list of changes

* Thu Aug 25 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.40.0-1
- Release 3.1.40.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.40.0 for the list of changes

* Fri Aug 12 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.39.0-1
- Release 3.1.39.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.39.0 for a list of changes

* Thu Jul 28 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.38.0-1
- Release 3.1.38.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.38.0 for a list of changes

* Thu Jun 16 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.32.0-1
- Release 3.1.32.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.32.0 for a list of changes

* Thu Jun  2 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.31.0-1
- Release 3.1.31.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.31.0 for a list of changes

* Thu May 19 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.30.0-1
- Release 3.1.30.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.30.0 for a list of changes

* Fri Apr  8 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.27.0-1
- Release 3.1.27.0-1
	See https://github.com/snort3/snort3/releases/tag/3.1.40.0 for a list of changes

* Thu Feb  3 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.21.0-1
- Release 3.1.21.0-1
	See https://blog.snort.org/2022/02/snort-31210-is-now-available-plus-bonus.html

* Wed Jan 12 2022 Lawrence R. Rogers <lrr@cert.org> 3.1.20.0-1
- Release 3.1.20.0-1
	See https://blog.snort.org/2022/01/snort-31200-available-for-download-now.html

* Wed Dec  8 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.18.0-1
- Release 3.1.18.0-1
        See https://blog.snort.org/2021/12/the-newest-version-of-snort-3-is.html

* Tue Nov 23 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.17.0-1
- Release 3.1.17.0-1
	See https://blog.snort.org/2021/11/snort-31170-has-been-released-check-out.html

* Fri Oct 29 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.15.0-1
- Release 3.1.15.0-1
	See https://blog.snort.org/2021/10/snort-31150-has-been-released-check-out.html

* Fri Oct  8 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.14.0-1
- Release 3.1.14.0-1
	See https://blog.snort.org/2021/10/snort-version-31140-released-here-are.html

* Mon Sep 27 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.13.0-1
- Release 3.1.13.0-1
	See https://blog.snort.org/2021/09/snort-version-31130-released-here-are.html

* Thu Sep  9 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.12.0-1
- Release 3.1.12.0-1
	See https://blog.snort.org/2021/09/snort-version-31120-released-here-are.html

* Thu Aug  5 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.9.0-1
- Release 3.1.9.0-1
	See https://blog.snort.org/2021/08/snort-version-3190-available-now.html

* Mon Jun 21 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.6.0-1
- Release 3.1.6.0-1
	See https://blog.snort.org/2021/06/new-version-of-snort-3-out-now-3160.html

* Tue May 25 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.5.0-1
- Release 3.1.5.0-1
	See https://blog.snort.org/2021/05/snort-3-5.html

* Mon May  3 2021 Lawrence R. Rogers <lrr@cert.org> 3.1.4.0-1
- Release 3.1.4.0-1
	See https://blog.snort.org/2021/05/new-snort-3-release-available-here-are.html
