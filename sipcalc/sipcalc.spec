Name: sipcalc
Version: 1.1.6
Release: 27%{?dist}
Summary: An "advanced" console based ip subnet calculator

License: BSD-3-Clause
URL: http://www.routemeister.net/projects/sipcalc
#URL2 : http://freecode.com/projects/sipcalc
Source0: http://www.routemeister.net/projects/%{name}/files/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc

%description
Sipcalc is an "advanced" console based ip subnet calculator.

%prep
%autosetup -p 1
autoreconf --verbose --force --install


# convert ChangeLog to UTF-8
iconv -f ISO-8859-1 -t UTF-8 ChangeLog > ChangeLog.utf8 && \
touch -r ChangeLog ChangeLog.utf8 && \
mv -f ChangeLog{.utf8,}

%build
%configure
%make_build

%install
%make_install DESTDIR=%{buildroot} INSTALL="install -p"

%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%doc doc/sipcalc.txt
%{_bindir}/sipcalc
%{_mandir}/man1/sipcalc.1.*

%changelog
* Wed Jul 31 2024 Michal Ambroz <rebus _AT seznam.cz> - 1.1.6-27
- use current macros, spdx license

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 18 2018 Michael Hampton <error@ioerror.us> - 1.1.6-13
- Add BuildRequires: gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Jaromir Capik <jcapik@redhat.com> - 1.1.6-2
- ChangeLog typo fixed in the upstream tarball
- Reuploading the sources

* Tue Jan 15 2013 Jaromir Capik <jcapik@redhat.com> - 1.1.6-1
- Update to 1.1.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Jaromir Capik <jcapik@redhat.com> - 1.1.5-1
- Updated to 1.1.5 + heavily patched
- #782324 - sipcalc buffer overflow

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Gary T. Giesen <giesen@snickers.org> 1.1.4-3
  Convert ChangeLog to UTF-8

* Tue Jul 07 2009 Gary T. Giesen <giesen@snickers.org> 1.1.4-2
- Spec file cleanup.

* Mon Jul 06 2009 Gary T. Giesen <giesen@snickers.org> 1.1.4-1
- Initial spec file creation for Fedora
