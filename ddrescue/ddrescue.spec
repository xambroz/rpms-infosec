Name:           ddrescue
Version:        1.26
Release:        2%{?dist}
Summary:        Data recovery tool trying hard to rescue data in case of read errors
License:        GPLv3+
URL:            http://www.gnu.org/software/ddrescue/ddrescue.html
Source0:        http://ftpmirror.gnu.org/ddrescue/ddrescue-%{version}.tar.lz
Source1:        http://ftpmirror.gnu.org/ddrescue/ddrescue-%{version}.tar.lz.sig

BuildRequires:   gcc-c++
BuildRequires:   make
BuildRequires:   lzip


%description
GNU ddrescue is a data recovery tool. It copies data from one file or block
device (hard disc, cd-rom, etc) to another, trying hard to rescue data in 
case of read errors. GNU ddrescue does not truncate the output file if not
asked to. So, every time you run it on the same output file, it tries to 
fill in the gaps.

%prep
# rpmbuild doesn't support lzip format
#setup -q
%setup -q -T -c
cd ..
lzip -d -c %{SOURCE0} > ddrescue-%{version}.tar
tar xf ddrescue-%{version}.tar
rm ddrescue-%{version}.tar

%build
# not a real autotools configure script, flags need to be passed specially
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir

%check
make check

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/ddrescue
%{_bindir}/ddrescuelog
%{_mandir}/man1/ddrescue.1*
%{_mandir}/man1/ddrescuelog.1*
%{_infodir}/%{name}.info*

%changelog
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 14 2022 Michal Ambroz <rebus AT_ seznam.cz> - 1.26-1
- Update to 1.26

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 03 2020 Michal Ambroz <rebus AT_ seznam.cz> - 1.25-1
- Update to 1.25.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Michal Ambroz <rebus AT_ seznam.cz> - 1.24-1
- Update to 1.24.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
- fix build dependency on gcc-c++

* Sun Mar 11 2018 Michal Ambroz <rebus AT_ seznam.cz> - 1.23-1
- Update to 1.23.

* Wed Feb 28 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.22-5
- Added gcc buildrequires.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 06 2017 Michal Ambroz <rebus AT_ seznam.cz> - 1.22-1
- Update to 1.22.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 29 2016 Michal Ambroz <rebus AT_ seznam.cz> - 1.21-1
- Update to 1.21.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Sep 12 2015 Michal Ambroz <rebus AT_ seznam.cz> - 1.20-1
- Update to 1.20.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Michal Ambroz <rebus AT_ seznam.cz> - 1.19-1
- Update to 1.19.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.18.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Sep 01 2014 Michal Ambroz <rebus AT_ seznam.cz> - 1.18-1
- Update to 1.18.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 05 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.17-1
- Update to 1.17.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 02 2012 Michal Ambroz <rebus AT_ seznam.cz> - 1.16-1
- Update to 1.16.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.13-1
- Update to 1.13.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.8-5
- Build with $RPM_OPT_FLAGS (#497152).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.8-3
- fix license tag

* Mon Feb 25 2008 Andreas Thienemann <athienem@redhat.com> - 1.8-2
- Fix info-page installation

* Mon Feb 25 2008 Andreas Thienemann <athienem@redhat.com> - 1.8-1
- Initial fedora release of GNU ddrescue
