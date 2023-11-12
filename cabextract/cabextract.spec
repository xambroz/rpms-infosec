Name:           cabextract
Version:        1.11
Release:        1%{?dist}
Summary:        Utility for extracting cabinet (.cab) archives

License:        GPL-2.0-or-later
URL:            https://www.cabextract.org.uk/
Source:         https://www.cabextract.org.uk/%{name}-%{version}.tar.gz

# use external/non-bundled libmspack
%if 0%{?fedora} || 0%{?rhel} > 8
#global mspack 1
%endif


## upstream patches

BuildRequires:  gcc
BuildRequires:  make
%if 0%{?mspack}
BuildRequires:  libmspack-devel >= 0.8
%else
# educated guess at version
Provides: bundled(libmspack) = 1.9
%endif


%description
cabextract is a program which can extract files from cabinet (.cab)
archives.


%prep
%autosetup -p1


%build
%configure \
  %{?mspack:--with-external-libmspack}

%make_build


%install
%make_install


%files
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/cabextract
%{_mandir}/man1/cabextract.1*


%changelog
* Sun Nov 12 2023 Michal Ambroz <rebus _AT seznam.cz> - 1.11-1
- bump to 1.11
- change to SPDX license string

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Robert Scheck <robert@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1 (#1684967)

* Sun Mar 07 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.9-7
- use bundled libmspack on epel

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.9-1
- 1.9

* Tue Oct 30 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.8-1
- 1.8

* Wed Jul 25 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.7-1
- 1.7 (#1186186)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 09 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.5-2
- Use license macro

* Tue Feb 24 2015 Juan Orti Alcaine <jorti@fedoraproject.org> - 1.5-1
- Updated to 1.5

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Dan Horák <dan[at]danny.cz> - 1.4-1
- updated to 1.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.3-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Dan Horák <dan[at]danny.cz> - 1.3-1
- updated to 1.3
- built with system copy of libmspack (CVE-2010-2800 CVE-2010-2801)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Patrice Dumas <pertusus@free.fr> - 1.2-1
- update to 1.2

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1-8
- respin (gcc43)
- cosmetics

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.1-7
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.1-6
- License: GPLv2+

* Tue Aug 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1-5
- Rebuild.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1-4
- Rebuild.

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.1-3
- Fix FC4 build.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 1.1-2
- Update to 1.1.
- Bump release to provide Extras upgrade path.

* Sat Mar 27 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.0-0.fdr.1
- Updated to 1.0.
- Added COPYING and TODO to documentation.
- Converted spec file to UTF-8.

* Sat May 31 2003 Warren Togami <warren@togami.com> 0:0.6-0.fdr.2
- Remove redundant %%doc

* Thu May 29 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.6-0.fdr.1
- Initial Fedora RPM release.
