Name: aircrack-ng
Version: 1.7
Release: 8%{?dist}

Summary: Tools for auditing 802.11 (wireless) networks
License: GPL-2.0-or-later
URL: https://github.com/%{name}/%{name}
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: ethtool
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: hwloc-devel
BuildRequires: libcmocka-devel
BuildRequires: libnl3-devel
BuildRequires: libpcap-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: sqlite-devel
BuildRequires: util-linux
BuildRequires: zlib-devel

Requires: util-linux%{?_isa}
Recommends: %{name}-doc

%description
aircrack-ng is a set of tools for auditing wireless networks. It's an
enhanced/reborn version of aircrack. It consists of airodump-ng (an 802.11
packet capture program), aireplay-ng (an 802.11 packet injection program),
aircrack (static WEP and WPA-PSK cracking), airdecap-ng (decrypts WEP/WPA
capture files), and some tools to handle capture files (merge, convert, etc.).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch

%description doc
%{summary}.

%prep
%autosetup -p1
find . -type f -name "*.py" -exec sed -e 's@/usr/bin/env python@%{__python3}@g' -e 's@python2@python3@g' -i "{}" \;

%build
autoreconf -fiv
%configure \
    --with-experimental \
    --with-lto \
    --with-avx512 \
    --without-opt \
    --disable-static
%make_build

%install
%make_install
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
find %{buildroot} -type f -name '*.la' -delete

%files
%doc AUTHORS ChangeLog README README.md
%license LICENSE
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/lib*.so
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%dir %{_datadir}/%{name}

# Special files created in runtime.
%ghost %{_datadir}/%{name}/airodump-ng-oui.txt
%ghost %{_datadir}/%{name}/oui.txt

%files devel
%{_includedir}/%{name}/

%files doc
%doc test/*.cap test/*.pcap test/password.lst test/*.py

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7-3
- Converted to SPDX.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 11 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7-1
- Updated to version 1.7.
- Enabled LTO.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.6-10
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Jeff Law <law@redhat.com> - 1.6-5
- Move LTO disablement so that it impacts the optflags override too

* Wed Jul 08 2020 Jeff Law <law@redhat.com> - 1.6-4
- Disable LTO

* Wed Jul 01 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6-3
- Removed useless patches from doc subpackage.

* Thu Apr 09 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6-2
- Moved libraries to main package.
- Moved OUI database to data directory.

* Mon Apr 06 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6-1
- Resurrected package.
- Updated to version 1.6.
- Performed SPEC cleanup.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Aug 25 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.2-8
- Rebuilt for hwloc-2.0

* Sun Aug 11 2019 Filipe Rosset <rosset.filipe@gmail.com> - 1.5.2-7
- Fix FTBFS on rawhide fixes rhbz#1734928 and rhbz#1735447

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Ivan Chavero <ichavero@redhat.com> - 1.5.2-4
- Fix debuginfo
- Fix date

* Tue Jan 22 2019 Ivan Chavero <ichavero@redhat.com> - 1.5.2-3
- Fix directory problem
- Skip failing tests

* Tue Dec 18 2018 Ivan Chavero <ichavero@redhat.com> - 1.5.2-2
- Fix package release

* Tue Dec 18 2018 Ivan Chavero <ichavero@redhat.com> - 1.5.2
- Fix spec file for new versioning from upstream
- Fix spec file for new autotools build system from upstream
- Fix spec file for new build requirements
- Spec file cleanup
- Added new files installation
- Removed patch: altarches.patch
- Removed patch: 0001-Fixed-compilation-with-OpenSSL-1.1.0-Closes-1711.patch

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.17rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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
