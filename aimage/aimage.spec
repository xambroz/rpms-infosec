Name:           aimage
Version:        3.2.5
Release:        3%{?dist}
Summary:        Advanced Disk Imager

Group:          Applications/System
License:        BSD with advertising
URL:            http://www.afflib.org
Source0:        http://www.afflib.org/downloads/aimage-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  afflib-devel >= 3.3.7
BuildRequires:  expat-devel
BuildRequires:  openssl-devel

%description
Advanced Disk Imager.


%prep
%setup -q
automake --add-missing
autoreconf

%build
%configure --enable-opt
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog
%{_bindir}/aimage


%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2.5-1
- Update to 3.2.5

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 27 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 3.2.4-1
- Update to 3.2.4

* Sun Nov 22 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 3.2.3-1
- Update to 3.2.3
- Remove upstreamed patch

* Wed Sep  2 2009 kwizart < kwizart at gmail.com > - 3.2.1-1
- Update to 3.2.1
- Update gcc44 patch

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.2.0-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  2 2009 kwizart < kwizart at gmail.com > - 3.2.0-4
- Fix for gcc44

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 3.2.0-2
- rebuild with new openssl

* Tue Sep 23 2008 kwizart < kwizart at gmail.com > - 3.2.0-1
- Update to 3.2.0

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 3.1.2-1
- Update to 3.1.2

* Wed Mar 12 2008 kwizart < kwizart at gmail.com > - 3.1.0-1
- Initial spec file
