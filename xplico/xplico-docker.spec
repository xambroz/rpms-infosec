%define debug_package %{nil}

Summary:	Internet traffic decoder and network forensic analysis tool

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		xplico
Version:	1.2.2
%define rel 3
Release:	%{rel}%{?dist}
URL:		http://www.xplico.org/

License:	GPL

Group:		Applications/Forensics Tools
Source0:	https://sourceforge.net/projects/xplico/files/Xplico%20versions/%{version}/xplico-v.%{version}.tar.gz/download#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-docker.sh
Source2:	%{name}-%{version}-docker-dockerfile

BuildRoot:	%{buildroot}
Requires:	docker

%description
The goal of Xplico is extract from an internet traffic capture the
applications data contained.  For example, from a pcap file Xplico
extracts each email (POP, IMAP, and SMTP protocols), all HTTP contents,
each VoIP call (SIP), FTP, TFTP, and so on. Xplico isn’t a network
protocol analyzer. Xplico is an open source Network Forensic Analysis Tool
(NFAT).

%prep
%setup -q -n %{name}-v.%{version}

%build
sed -e "s/NAME/%{name}/" -e "s/VERSION/%{version}/" -e "s/RELEASE/%{rel}/" < %{SOURCE1} > %{name}
cp -p %{SOURCE2} Dockerfile

%install
%{__install} -Dp -m755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc AUTHORS ChangeLog COPYING.CC_BY-NC-SA Dockerfile INSTALL LICENSE COPYING.GPLv2.0 DEPENDENCES README README.md
%attr(0755, root, root)		%{_bindir}/xplico

%changelog
* Fri Aug 20 2021 Lawrence R. Rogers <lrr@cert.org> 1.2.2-3
* Release 1.2.2-3
	Due to changes in PHP, the previous version no longer works.
	This version uses a container based on Ubuntu.
	The container can be found at certlifter/%{name}-%{version}:%{rel}.
	Note that the Dockerfile is provided as part of this package.

* Mon Apr 29 2019 Lawrence R. Rogers <lrr@cert.org> 1.2.2-2
* Release 1.2.2-2
	Removed old version support

* Thu Apr 25 2019 Lawrence R. Rogers <lrr@cert.org> 1.2.2-1
* Release 1.2.2-1
	Version 1.2.2
		CakePHP 2.10.17
		Migration from GeoIP to GeoIP2
		nDPI updated to 2.9

* Mon Apr  8 2019 Lawrence R. Rogers <lrr@cert.org> 1.2.1-2
* Release 1.2.1-2
	Rebuilt for latest python in EPEL.

* Mon Nov 13 2017 Lawrence R. Rogers <lrr@cert.org> 1.2.1-1
* Release 1.2.1-1
	Mehmet D. İNCE from invictuseurope.com discovered several
	vulnerability related to the Xplico software. He identified three
	different vulnerability, two classified as “Hight severity”
	and one as “Medium severity”. The number assigned for this
	vulnerability of Xplico is CVE-2017-16666. More details here.
	Thanks to Mehmet’s detail report and the collaboration
	of  Mehmet and of Doug Burks of Security Onion Solutions,
	vulnerabilities have been resolved.
	This release fix these issues. It is recommended and exhorts to
	upgrade your Xplico installations.

	Thanks again to Mehmet D. İNCE and to Doug Burks.
	Gianluca Costa

* Wed Sep 27 2017 Lawrence R. Rogers <lrr@cert.org> 1.2.0-4
* Release 1.2.0-4
	Added missing README.md file

* Fri Aug  4 2017 Lawrence R. Rogers <lrr@cert.org> 1.2.0-3
* Release 1.2.0-3
	Recompiled for new version of nDPI (2.1)

* Wed May 24 2017 Lawrence R. Rogers <lrr@cert.org> 1.2.0-2
* Release 1.2.0-2
	New version of lame and lame-libs.

* Wed Jan 18 2017 Lawrence R. Rogers <lrr@cert.org> 1.2.0-1
* Release 1.2.0-1
	* This is the 1.2.0 version.
		xplico 1.2.0
		  * Migration from PHP5 to PHP7
		  * CakePHP 2.8
		  * IMAP bug fix
		  * Bugfix: reported on Security Onion

		xplico 1.1.2
		  * IPv4 defragmentation
		  * CapAnalysis dissectors and dispatcher

* Wed Dec  7 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.1-6
* Release 1.1.1-6
	* Created pyc files for Fedora 24 from the 1.1.2 distribution.

* Mon Oct 24 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.1-5
* Release 1.1.1-5
	* The PHP configuration is now also in the start and stop code.

* Fri Oct 21 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.1-4
* Release 1.1.1-4
	* CentOS/RHEL 7 also uses systemctl.

* Fri Oct 21 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.1-3
* Release 1.1.1-3
	* CentOS/RHEL 7 have Python 3.3.

* Sat Jul  9 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.1-2
* Release 1.1.1-2
	* Recompiled for nDPI-1.8.

* Mon Nov  9 2015 Lawrence R. Rogers <lrr@cert.org> 1.1.1-1
* Release 1.1.1-1
	* Whatsapp OS and Phone number
	* Added MGCP dissector
	* IMAP bug fixed
	* Updated for nDPI-1.7.0.

* Tue Aug 18 2015 Lawrence R. Rogers <lrr@cert.org> 1.1.0-4
* Release 1.1.0-4
	Recompiled for nDPI-1.7.0.

* Mon Jun 29 2015 Lawrence R. Rogers <lrr@cert.org> 1.1.0-3
* Release 1.1.0-3
	Recompiled for nDPI-1.6.

* Wed Sep  3 2014 Lawrence R. Rogers <lrr@cert.org> 1.1.0-2
* Release 1.1.0-2
	Changes for CentOS/RHEL 7

* Mon May 12 2014 Lawrence R. Rogers <lrr@cert.org> 1.1.0-1
* Release 1.1.0-1
	xplico 1.1.0
		* Performance improved
		* nDPI updated
		* IRC bug fixed
		* HTTP bug fixed
		* VoIP (SIP, RTP) bug fixed
		* FTP bug fixed
		* changed the FaceBook DB tables
		* Null/Loopback dissector
		* Cisco HDLC dissector
		* Libero.it and RossoAlice webmail decoding
		* Yahoo messenger (web and mobile)
		* Dig using file signatures (unknown flows)

* Thu Apr 24 2014 Lawrence R. Rogers <lrr@cert.org> 1.0.1-5
* Release 1.0.1-5
	For Fedora, there is now a systemd config file and the old /etc/init.d/xplico is now in /usr/sbin.

* Tue Jan 07 2014 Lawrence R. Rogers <lrr@cert.org> 1.0.1-4
* Release 1.0.1-4
	Fix for Fedora 19 and 20 and CentOS/RHEL 6 for setsocketopt in system/dema/session_decoding.c

* Fri Aug 02 2013 Lawrence R. Rogers <lrr@cert.org> 1.0.1-3
* Release 1.0.1-3
	Patch for Fedora 19

* Tue Jul 17 2012 Lawrence Rogers <lrr@cert.org> 1.0.0-2
* Release 1.0.0-2
	For beyond Fedora 16, now starts, stops, and queries the daemon status using systemctl.
	Also, adjusts /etc/php.ini so that xplico starts and runs.

* Fri Feb 10 2012 Lawrence Rogers <lrr@cert.org> 1.0.0-1
* Release 1.0.0-1
	* SQLite dispatcher performance improved
	* added the PPI dissector
	* added the syslog dissector
	* added "Bogus IP length" correction with checksum verification disabled
	* new Facebook Chat dissector for the new Facebook chat protocol
	* SIP dissector improved
	* IMAP dissector improved and bugs fixed
	* DNS dissector PIPI improved
	* Yahoo Webmail bugs fixed
	* Live/Hotmail WebMail Spanish version
	* GeoMap improved
	* PCap-over-IP

* Sun Jan 15 2012 Lawrence Rogers <lrr@cert.org> 0.7.1-1
* Release 0.7.1-1
	* RTP bug fixed
	* dispatcher core functionality bug fixed
	* mfile manipulator bug fixed
	* XI bugs fixed
	* added DB migration tool

* Mon Nov 7 2011 Lawrence Rogers <lrr@cert.org> 0.7.0-1
* Release 0.7.0-1
	* upgraded XI to Cakephp 1.3
	* added the ICMPv6 dissector
	* Ethernet dissector improved (necessary for ICMPv6)
	* deadlock fixed
	* fixed the communication bug from xplico and manipulators
	* SDP dissector bug fixes
	* SIP and TCP dissectors improved
	* WebMail manipulator and all python3 scripts improved (ready to new webmail entry... see pol ;) )
	* added pcap file name on CLI report screen
	* capture modules log improved
	* new GeoIP version: 1.4.8
	* added IPv6 Hop-by-Hop Options
	* Xplico and all Manipulators with dual stack (IPv4, IPv6)
	* XI language localization
	* DNS bugfix
	* added the  MDNS dissector
	* added AOL WebMail
	* added Yahoo! WebMail
	* added Yahoo! Mail for Andorid Mobile
	* added Gmail

* Mon Jun 6 2011 Lawrence Rogers <lrr@cert.org> 0.6.3-1
* Release 0.6.3-1
	* xplico 32/64bit version
	* new decoding manager (DeMa) version 0.3.1
	* mfile manipulator (HTTP file transfare) bug fixes
	* WebMail scripts improved
	* HTTP dissector improved
	* upgraded the XI javascript libraries

* Tue May 3 2011 Lawrence Rogers <lrr@cert.org>  0.6.2-1
* Revision 1: Upgrade to 0.6.2 doing the following:
	l7-patterns for all flows/protocols not decoded by xplico
	Xplico Interface (XI) improved
	python3 porting of many script
	realtime capture module improved
	facebook chat realtime view
	UTC/localtime bug fixes
	l2tp dissector bug fixes
	cli and lite dispatchers bug fixes
	telnet dissector bug fixes

* Tue Mar 1 2011 Lawrence Rogers <lrr@cert.org>  0.6.1-6
* Revision 6: The /etc/init.d/xplico script no longer specific the start and stop levels.
	      These should be done identical to and after httpd, so that xplico is
		set to start after httpd.

* Fri Dec 10 2010 Lawrence Rogers <lrr@cert.org>  0.6.1-5
* Revision 5: Fixed init.d script so that it waits until httpd starts

* Thu Dec 9 2010 Lawrence Rogers <lrr@cert.org>  0.6.1-4
* Revision 4: Fixed init.d script so that it is started after httpd

* Thu Dec 9 2010 Lawrence Rogers <lrr@cert.org>  0.6.1-3
* Revision 3: Stops and restarts the server, if necessary, before adding any tables and PRAGMA values

* Thu Dec 9 2010 Lawrence Rogers <lrr@cert.org>  0.6.1-2
* Revision 2: Changed the postun script to add the msn_chats and paltalk_rooms tables to an existing database.
		Also the foreign_keys PRAGMA was turned on and the auto_vacuum value displayed.`

* Tue Dec 7 2010 Lawrence Rogers <lrr@cert.org>  0.6.1-1
* Revision 1: Version 0.6.1 from www.xplico.org

* Mon Nov 29 2010 Lawrence Rogers <lrr@cert.org> 0.6.0-10
- Revision 10: Improved (fixed?) /etc/init.d/xplico so that it waits longer for httpd to start.
  Also added httpd as a service start dependency.

* Fri Nov 19 2010 Lawrence Rogers <lrr@cert.org> 0.6.0-9
- Revision 9: 

* Thu Nov 18 2010 Lawrence Rogers <lrr@cert.org> 0.6.0-8
- Revision 8: Correctly removes pcl6 and videosnarf as pre-uninstall scripts so that the
  /opt/xplico hierarchy can be completely removed if possible when xplico is removed.

* Thu Nov 18 2010 Lawrence Rogers <lrr@cert.org> 0.6.0-7
- Revision 7: Removed pcl6 and videosnarf and made those packages prerequisites. The needed
  binaries are then copied into the /opt/xplico hierarchy using the post-install script.
  Also, the correct syntax for creating the dabase is used.

* Thu Nov 18 2010 Lawrence Rogers <lrr@cert.org> 0.6.0-6
- Revision 6: Added pcl6 and videosnarf

* Thu Nov 18 2010 Lawrence Rogers <lrr@cert.org>  0.6.0-5
- Revision 5: Fixed permissions to match those of the Debian package
  Also preserves any existing database by creating the database in the post-install script,
  as needed.

* Thu Nov 18 2010 Lawrence Rogers <lrr@cert.org> 0.6.0-4
- Revision 4: Gave execute permissions to everything in the bin directory
