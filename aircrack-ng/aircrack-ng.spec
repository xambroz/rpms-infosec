%global _hardened_build 1
%global alphatag rc4

Name:           aircrack-ng
Version:        1.2
#Release:        4%{?dist}
Release:        0.16%{alphatag}%{?dist}
Summary:        802.11 (wireless) sniffer and WEP/WPA-PSK key cracker

Group:          Applications/System

License:        GPLv2+
URL:            http://www.aircrack-ng.org/
Source0:        http://download.aircrack-ng.org/aircrack-ng-%{version}-%{alphatag}.tar.gz
#Source0:        http://download.aircrack-ng.org/aircrack-ng-%{version}%{alphatag}.tar.gz
# Created with
# svn export http://trac.aircrack-ng.org/svn/trunk aircrack-ng-1.1.20130402svn
# tar cvjf aircrack-ng-1.1.20130402svn.tar.bz2 aircrack-ng-1.1.20130402svn/
#Source0:        aircrack-ng-%{version}%{alphatag}.tar.bz2
#Source0:        http://download.aircrack-ng.org/aircrack-ng-%{version}-%{alphatag}.tar.gz
#Source0:        aircrack-ng-%{version}-%{alphatag}.tar.gz
#Source1:        %{name}-tarball
#Source2:        aircrack-ng-ptw.cap
#Source2:        http://dl.aircrack-ng.org/ptw.cap
#Source3:        aircrack-ng-test.ivs
#Source3:       http://download.aircrack-ng.org/wiki-files/other/test.ivs
# License unclear:
#Source4:        http://standards.ieee.org/regauth/oui/oui.txt

# from upstream
Patch1: altarches.patch
# from upstream
Patch2: 0001-Fixed-compilation-with-OpenSSL-1.1.0-Closes-1711.patch

BuildRequires:  sqlite-devel openssl-devel libnl3-devel
BuildRequires:  pcre-devel
# for besside-ng-crawler
BuildRequires:  libpcap-devel
# Used by airmon-ng
Requires: rfkill


%description
aircrack-ng is a set of tools for auditing wireless networks. It's an
enhanced/reborn version of aircrack. It consists of airodump-ng (an 802.11
packet capture program), aireplay-ng (an 802.11 packet injection program),
aircrack (static WEP and WPA-PSK cracking), airdecap-ng (decrypts WEP/WPA
capture files), and some tools to handle capture files (merge, convert, etc.).


%prep
%autosetup -p 1 -q -n aircrack-ng-%{version}-%{alphatag}

%build
#grep '(hex') %{SOURCE4} > airodump-ng-oui.txt
# License unclear
touch airodump-ng-oui.txt
#touch --reference %{SOURCE4} airodump-ng-oui.txt

%set_build_flags
# experimental=true needed for wesside-ng, easside-ng, buddy-ng and tkiptun-ng
# (also needed in make install)
%make_build sqlite=true experimental=true pcre=true


%install
#FIXME: enable scripts, requires python
#make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} mandir=%{_mandir}/man1 sqlite=true unstable=true ext_scripts=true
%make_install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} mandir=%{_mandir}/man1 sqlite=true experimental=true pcre=true
install -p -m 644 -D airodump-ng-oui.txt  $RPM_BUILD_ROOT%{_sysconfdir}/aircrack-ng/airodump-ng-oui.txt


%check
make check

# WEP checks, that are not wanted by upstream:
# http://trac.aircrack-ng.org/ticket/533
#cp %{SOURCE2} test/ptw.cap
#cp %{SOURCE3} test/test.ivs
#src/aircrack-ng -K -b 00:11:95:91:78:8C -q test/test.ivs | grep 'KEY FOUND! \[ AE:5B:7F:3A:03:D0:AF:9B:F6:8D:A5:E2:C7 \]'
#src/aircrack-ng -q -e Appart -z test/ptw.cap | grep 'KEY FOUND! \[ 1F:1F:1F:1F:1F \]'


%files
%doc AUTHORS ChangeLog README VERSION
%doc test/*.cap test/*.pcap test/password.lst test/*.py patches/
%license LICENSE
%{_bindir}/aircrack-ng
%{_bindir}/airdecap-ng
%{_bindir}/airdecloak-ng
%{_bindir}/airolib-ng
%{_bindir}/besside-ng-crawler
%{_bindir}/buddy-ng
%{_bindir}/ivstools
%{_bindir}/kstats
%{_bindir}/makeivs-ng
%{_bindir}/packetforge-ng
%{_bindir}/wpaclean
%{_sbindir}/airbase-ng
%{_sbindir}/aireplay-ng
%{_sbindir}/airmon-ng
%{_sbindir}/airodump-ng
%{_sbindir}/airodump-ng-oui-update
%{_sbindir}/airserv-ng
%{_sbindir}/airtun-ng
%{_sbindir}/besside-ng
%{_sbindir}/easside-ng
%{_sbindir}/tkiptun-ng
%{_sbindir}/wesside-ng
%{_mandir}/man1/aircrack-ng.1*
%{_mandir}/man1/airdecap-ng.1*
%{_mandir}/man1/airdecloak-ng.1*
%{_mandir}/man1/airolib-ng.1*
%{_mandir}/man1/besside-ng-crawler.1*
%{_mandir}/man1/buddy-ng.1*
%{_mandir}/man1/ivstools.1*
%{_mandir}/man1/kstats.1*
%{_mandir}/man1/makeivs-ng.1*
%{_mandir}/man1/packetforge-ng.1*
%{_mandir}/man1/wpaclean.1*
%{_mandir}/man8/airbase-ng.8*
%{_mandir}/man8/aireplay-ng.8*
%{_mandir}/man8/airmon-ng.8*
%{_mandir}/man8/airodump-ng.8*
%{_mandir}/man8/airodump-ng-oui-update.8*
%{_mandir}/man8/airserv-ng.8*
%{_mandir}/man8/airtun-ng.8*
%{_mandir}/man8/besside-ng.8*
%{_mandir}/man8/easside-ng.8*
%{_mandir}/man8/tkiptun-ng.8*
%{_mandir}/man8/wesside-ng.8*

%dir %{_sysconfdir}/aircrack-ng
%config(noreplace) %{_sysconfdir}/aircrack-ng/airodump-ng-oui.txt


%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.16rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 27 2017 Till Maas <opensource@till.name> - 1.2-0.15
- Fix building against OpenSSL 1.1 (Thank you Xose Vazquez Perez for fetching the patch)
- Update BRs (spotted by Xose Vazquez Perez)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.14rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.13rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.12rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-0.11.rc4
- Fix build on aarch64/Power64

* Fri Mar 18 2016 Till Maas <opensource@till.name> - 1.2-0.10.rc4
- Update to new release
- Add airmon-ng dependency

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.9rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 02 2015 Till Maas <opensource@till.name> - 1.2-0.8rc2
- Do not package binary test suite

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.7rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Till Maas <opensource@till.name> - 1.2-0.6.rc2
- Update to new release
- Use %%license

* Mon Nov 03 2014 Till Maas <opensource@till.name> - 1.2-0.5.rc1
- Update to new release to address CVE-2014-8324, CVE-2014-8321, CVE-2014-8323
  and CVE-2014-8322

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.3.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Till Maas <opensource@till.name> - 1.2-0.2.beta2
- Update to new release

* Sun Oct 13 2013 Till Maas <opensource@till.name> - 1.2-0.1.beta1
- Update to new release
- harden build
- Run testsuite
- fix bogus date in changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8.20130402svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Till Maas <opensource@till.name> - 1.1-7
- Updated to new SVN snapshot (Red Hat Bugzilla #881342)
- Updated manpages locations
- Add new BR: libpcap-devel

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6.20120904svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Till Maas <opensource@till.name> - 1.1-5
- Update to SVN snapshot to make it work better
- Remove upstreamed patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 26 2010 Till Maas <opensource@till.name> - 1.1-1
- Update to new release
- remove upstreamed patches and patches from upstream

* Sat May 29 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.0-3
- CVE-2010-1159 aircrack-ng: remote denial of service, RH Bug #582416

* Sun Mar 28 2010 Till Maas <opensource@till.name> - 1.0-2
- Include patch against eapol overflow from upstream, RH Bug #577654

* Wed Sep 16 2009 Till Maas <opensource@till.name> - 1.0-1
- Update to stable release
- Include airodump-ng-oui-update
- prepare shipping of oui database
- fix paths for oui database in airodump-ng-oui-update and airodump-ng
- add missing #include <types.h>

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0-0.10.rc3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.9.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Till Maas <opensource@till.name> - 1.0-0.8.rc3
- Update to new release
- Enable patch to make parallel make work on x86_64

* Tue Feb 24 2009 Till Maas <opensource@till.name> - 1.0-0.7.20090224svn
- Update to new svn snapshot to make it compile again

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.20081109svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Till Maas <opensource@till.name> - 1.0-0.5.20081109svn
- Update to new svn snapshot

* Sun Nov 09 2008 Till Maas <opensource@till.name> - 1.0-0.4.20081109svn
- Update to new svn snapshot

* Sat Nov 08 2008 Till Maas <opensource@till.name> - 1.0-0.3.20081108svn
- Update to new svn snapshot that fixes some issues with tkiptun-ng

* Fri Nov 07 2008 Till Maas <opensource@till.name> - 1.0-0.2.20081107svn
- Update to current svn snapshot
- remove gz suffix from manpages
- add new airdecloack-ng tool
- remove partly upstreamed patch

* Fri Oct 31 2008 Till Maas <opensource@till.name> - 1.0-0.1.20081031svn
- Update to current svn snapshot
- Add sqlite-devel BR and add airolib-ng
- Add patch to do some testing of aircrack-ng
- Add openssl-devel BR

* Sat Mar 01 2008 Till Maas <opensource till name> - 0.9.3-1
- update to latest version
- remove patch that was merged upstream

* Wed Feb 13 2008 Till Maas <opensource till name> - 0.9.2-1
- update to latest version
- remove patch that was merged upstream
- add aircrack-ng-0.9.2-include_limits.patch

* Thu Aug 23 2007 Till Maas <opensource till name> - 0.9.1-2
- rebuild because of broken ppc32 package
- update License Tag
- fix some bugs in aireplay-ng.c

* Thu Jun 28 2007 Till Maas <opensource till name> - 0.9.1-1
- update to latest version

* Mon May 14 2007 Till Maas <opensource till name> - 0.9-1
- update to latest version

* Sun May 06 2007 Till Maas <opensource till name> - 0.8-2
- fix disttag

* Sun May 06 2007 Till Maas <opensource till name> - 0.8-1
- update to latest version

* Thu Apr 12 2007 Till Maas <opensource till name> - 0.8-0.2.20070417svn
- some more bugfixes

* Thu Apr 12 2007 Till Maas <opensource till name> - 0.8-0.1.20070413svn
- update to 0.8
- fixes http://archives.neohapsis.com/archives/fulldisclosure/2007-04/0408.html
  (remote code execution)
- fix race condition in %%install

* Wed Feb 21 2007 Till Maas <opensource till name> - 0.7-1
- initial spec for fedora
