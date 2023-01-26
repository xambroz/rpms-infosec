%global _hardened_build 1
%global alphatag rc4

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?fedora} <= 21
 %{!?py2_build:         %global py2_build       %{__python2} setup.py build --executable="%{__python2} -s"}
 %{!?py2_install:       %global py2_install     %{__python2} setup.py install -O1 --skip-build --root %{buildroot}}
 %{!?py3_build:         %global py3_build       %{__python3} setup.py build --executable="%{__python3} -s"}
 %{!?py3_install:       %global py3_install     %{__python3} setup.py install -O1 --skip-build --root %{buildroot}}
%endif


Name:           aircrack-ng
Version:        1.2
#Release:        4%{?dist}
Release:        0.12.%{alphatag}%{?dist}
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
Patch0:         %{name}-destdir.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  sqlite-devel openssl-devel libnl3-devel
# for besside-ng-crawler
BuildRequires:  libpcap-devel

# for ext_scripts=true
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python-tools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

# Used by airmon-ng
Requires: rfkill


%description
aircrack-ng is a set of tools for auditing wireless networks. It's an
enhanced/reborn version of aircrack. It consists of airodump-ng (an 802.11
packet capture program), aireplay-ng (an 802.11 packet injection program),
aircrack (static WEP and WPA-PSK cracking), airdecap-ng (decrypts WEP/WPA
capture files), and some tools to handle capture files (merge, convert, etc.).


%package python2
Summary:        Aircrack-ng python scripts
%{?python_provide:%python_provide python2-%{name}}

Requires:       aircrack-ng == %{version}

%description python2
Aircrack-ng python scripts


%if 0%{?with_python3}
%package python3
Summary:        Aircrack-ng python scripts
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

Requires:       aircrack-ng == %{version}


%description python3
Aircrack-ng python scripts
%endif # with_python3



%prep
%setup -q -n aircrack-ng-%{version}-%{alphatag}
%patch0 -p 1 -b .destdir

#Prepare for the python3
2to3 -w scripts/airdrop-ng
2to3 -w scripts/airgraph-ng
2to3 -w scripts/versuck-ng

%build
#grep '(hex') %{SOURCE4} > airodump-ng-oui.txt
# License unclear
touch airodump-ng-oui.txt
#touch --reference %{SOURCE4} airodump-ng-oui.txt

#-Wp,-D_FORTIFY_SOURCE=2 is causing race condition failures in aircrack-ng
CFLAGS="%{optflags}"
CFLAGS=`echo "$CFLAGS" | sed -e 's|FORTIFY_SOURCE=2|FORTIFY_SOURCE=0|g;'`
export CFLAGS

# experimental=true needed for wesside-ng, easside-ng, buddy-ng and tkiptun-ng
# (also needed in make install)
%make_build sqlite=true experimental=true pcre=true ext_scripts=true

for I in scripts/airgraph-ng scripts/airdrop-ng; do
	pushd $I
	%py2_build
	popd
done

%if 0%{?with_python3}
for I in scripts/airgraph-ng scripts/airdrop-ng; do
	pushd $I
	%py3_build
	popd
done
%endif # with_python3


%install
rm -rf %{buildroot}
mkdir %{buildroot}
export DESTDIR=%{buildroot}
#FIXME: enable scripts, requires python
#make install DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir}/man1 sqlite=true unstable=true ext_scripts=true
make install DESTDIR=%{buildroot} prefix=%{_prefix} etcdir=%{_sysconfdir}/aircrack-ng mandir=%{_mandir}/man1 sqlite=true experimental=true pcre=true ext_scripts=true
install -p -m 644 -D airodump-ng-oui.txt  %{buildroot}%{_sysconfdir}/aircrack-ng/airodump-ng-oui.txt

#Install python2 files
for I in scripts/airgraph-ng scripts/airdrop-ng; do
	pushd $I
	%py2_install
	popd
done

mv %{buildroot}%{_bindir}/airgraph-ng %{buildroot}%{_bindir}/airgraph-ng-2.7
mv %{buildroot}%{_bindir}/airdrop-ng  %{buildroot}%{_bindir}/airdrop-ng-2.7
mv %{buildroot}%{_bindir}/dump-join   %{buildroot}%{_bindir}/dump-join-2.7
cp %{buildroot}%{_bindir}/versuck-ng  %{buildroot}%{_bindir}/versuck-ng-2.7


#Install python3 files
%if 0%{?with_python3}
for I in scripts/airgraph-ng scripts/airdrop-ng; do
	pushd $I
	%py3_install
	popd
done

mv %{buildroot}%{_bindir}/airgraph-ng %{buildroot}%{_bindir}/airgraph-ng-3.4
mv %{buildroot}%{_bindir}/airdrop-ng  %{buildroot}%{_bindir}/airdrop-ng-3.4
mv %{buildroot}%{_bindir}/dump-join   %{buildroot}%{_bindir}/dump-join-3.4
mv %{buildroot}%{_bindir}/versuck-ng  %{buildroot}%{_bindir}/versuck-ng-3.4
%endif # with_python3

#for now link to the python2 as it is the package default
ln -f -s airgraph-ng-2.7 %{buildroot}%{_bindir}/airgraph-ng
ln -f -s airdrop-ng-2.7  %{buildroot}%{_bindir}/airdrop-ng
ln -f -s dump-join-2.7   %{buildroot}%{_bindir}/dump-join
ln -f -s versuck-ng-2.7  %{buildroot}%{_bindir}/versuck-ng


%check
make check

# WEP checks, that are not wanted by upstream:
# http://trac.aircrack-ng.org/ticket/533
#cp %{SOURCE2} test/ptw.cap
#cp %{SOURCE3} test/test.ivs
#src/aircrack-ng -K -b 00:11:95:91:78:8C -q test/test.ivs | grep 'KEY FOUND! \[ AE:5B:7F:3A:03:D0:AF:9B:F6:8D:A5:E2:C7 \]'
#src/aircrack-ng -q -e Appart -z test/ptw.cap | grep 'KEY FOUND! \[ 1F:1F:1F:1F:1F \]'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
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
%{_sbindir}/airoscript-ng
%{_sbindir}/airserv-ng
%{_sbindir}/airtun-ng
%{_sbindir}/besside-ng
%{_sbindir}/easside-ng
%{_sbindir}/tkiptun-ng
%{_sbindir}/wesside-ng
%{_mandir}/man1/aircrack-ng.1*
%{_mandir}/man1/airdecap-ng.1*
%{_mandir}/man1/airdecloak-ng.1*
%{_mandir}/man1/airgraph-ng.1*
%{_mandir}/man1/airolib-ng.1*
%{_mandir}/man1/dump-join.1*
%{_mandir}/man1/besside-ng-crawler.1*
%{_mandir}/man1/buddy-ng.1*
%{_mandir}/man1/ivstools.1*
%{_mandir}/man1/kstats.1*
%{_mandir}/man1/makeivs-ng.1*
%{_mandir}/man1/packetforge-ng.1*
%{_mandir}/man1/versuck-ng.1*
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
%{_datadir}/airoscript-ng/*
%{_docdir}/airoscript-ng/*

%dir %{_sysconfdir}/aircrack-ng
%config(noreplace) %{_sysconfdir}/aircrack-ng/airodump-ng-oui.txt
%config(noreplace) %{_sysconfdir}/aircrack-ng/airoscript-ng.conf
%config(noreplace) %{_sysconfdir}/aircrack-ng/airoscript-ng_advanced.conf
%config(noreplace) %{_sysconfdir}/aircrack-ng/airoscript-ng_debug.conf

%files python2
%{_bindir}/airgraph-ng
%{_bindir}/airdrop-ng
%{_bindir}/dump-join
%{_bindir}/versuck-ng
%{_bindir}/airgraph-ng-2.7
%{_bindir}/airdrop-ng-2.7
%{_bindir}/dump-join-2.7
%{_bindir}/versuck-ng-2.7
%{python2_sitelib}/airdrop*
%{python2_sitelib}/graphviz*
%{python2_sitelib}/airgraph_ng*

%if 0%{?with_python3}
%files python3
%{_bindir}/airgraph-ng-3.4
%{_bindir}/airdrop-ng-3.4
%{_bindir}/dump-join-3.4
%{_bindir}/versuck-ng-3.4
%{python3_sitelib}/airdrop*
%{python3_sitelib}/graphviz*
%{python3_sitelib}/airgraph_ng*
%endif # with_python3




%changelog
* Thu Oct 06 2016 Michal Ambroz <rebus AT seznam.cz> - 1.2-0.12.rc4
- package contrib scripts such as airoscript-ng airdrop-ng airgraph-ng

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
