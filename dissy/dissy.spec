Name:           dissy
Version:        10
Release:        7%{?dist}
Summary:        Graphical frontend to the objdump disassembler
License:        GPL-2.0-only
URL:            http://code.google.com/p/dissy
Source0:        http://dissy.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:        dissy.desktop
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       binutils
Requires:       pygobject2
Requires:       pywebkitgtk

%description
Dissy is a graphical frontend to the objdump disassembler, it can be used
for debugging and browsing compiler-generated code. 

%prep
%setup -q

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --prefix %{_prefix} --skip-build --root %{buildroot}
rm -r %{buildroot}%{_docdir}

# Icon file. Upstream doesn't use any
install -pd %{buildroot}%{_datadir}/pixmaps
install -pm644 \
        %{buildroot}%{_datadir}/dissy/gfx/red_arrow_left.png \
        %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Desktop menu entry
install -pd %{buildroot}%{_datadir}/applications
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{S:1}

%files
%doc ChangeLog COPYING README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.1*
%{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}-%{version}-py%{python2_version}.egg-info

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 17 2015 Adrien Vergé <adrienverge@gmail.com> - 10-3
- Fix broken dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Christopher Meng <rpm@cicku.me> - 10-1
- SPEC Cleanup.
- Update to latest version and drop the old patch.
- Remove desktop vendor.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 8-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 09 2010 Lubomir Rintel <lkundrak@v3.sk> - 8-5
- Package egg info in RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 06 2008 Lubomir Rintel <lkundrak@v3.sk> - 8-2
- Fix about dialog close

* Sat Feb 02 2008 Lubomir Rintel <lkundrak@v3.sk> - 8-1
- Initial packaging
