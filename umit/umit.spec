Name:           umit
Version:        1.0
Release:        16%{?dist}
Summary:        Nmap front-end
License:        GPLv2+ and LGPLv2+
URL:            http://umit.sourceforge.net/
Source0:        http://downloads.sourceforge.net/umit/umit-%{version}.tar.gz
# http://trac.umitproject.org/ticket/378
Source1:        umit_48x48.png
# http://trac.umitproject.org/ticket/378
Source2:        umit.desktop
# Fedora-specific: Fix check-buildroot issues
Patch0:         umit-1.0-setup.py.patch
Patch1:         umit-1.0-usrmove.patch
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  python2-devel

Requires:       nmap
Requires:       pygtk2


%description
With Umit, you have all the power provided by Nmap through its regular 
command line interface, and a lot more in a highly usable and portable 
Graphical Interface. Some of its main features include:
    * Easily create powerful Nmap commands and save them as profiles to use 
      whenever you need it
    * Edit your Profiles using the Interface Editor
    * Create Profiles with the assistance of a Wizard
    * Group and order you scan results
    * Filter hosts list by services
    * Filter services list by hosts
    * Compare two scan results in one of our three compare modes: text diff, 
      graphical comparison and HTML diff
    * Search scan results
    * Use Umit interface through the Web


%prep
%autosetup -p1


%build
%py2_build


%install
%py2_install

# Fix permissions
find %{buildroot} -type f -exec chmod 644 {} \;
chmod 755 %{buildroot}%{_bindir}/*

# Remove a interpreter from the site-packages
find %{buildroot}%{python2_sitelib} -type f -iname "*py" -exec \
    sed -i 's/#!\/usr\/bin\/env python2//' {} \;

# Install the icons
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/umit
install -d %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
ln -s ../../../../pixmaps/umit/umit_48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/umit.png

# Install the desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    %{SOURCE2}

%find_lang %{name}


%files -f %{name}.lang
%doc README
%license COPYING COPYING_HIGWIDGETS
%{_bindir}/umit
%{_bindir}/umit_scheduler.py
%{_datadir}/applications/umit.desktop
%{_datadir}/icons/hicolor/*/*/umit*
%{_datadir}/icons/umit
%{_datadir}/pixmaps/umit
%{_datadir}/umit
%{python2_sitelib}/higwidgets
%{python2_sitelib}/umit
%{python2_sitelib}/umit-*.egg-info


%changelog
* Mon Jul 29 2019 Filipe Rosset <rosset.filipe@gmail.com> - 1.0-16
- Fix FTBFS, drop sphinx doc support, spec cleanup and modernization

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Feb 10 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.0-11
- rebuilt to fix FTBFS on rawhide, silent rpmlint + spec cleanup

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0-9
- Remove obsolete scriptlets

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Nikolay Ulyanitsky <lystor AT gmail.com> - 1.0-1
- Update to 1.0

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.RC
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.RC
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.RC
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.5.RC
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0-0.4.RC
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 15 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.0-0.3.RC
- Fix the Summary
- Remove doc macro from %%{_docdir}/umit

* Sat Mar 13 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.0-0.2.RC
- Add the pygtk2 to the Requires
- Fix the license
- Fix the Source0
- Remove the unused macro python_sitearch
- Remove the -doc subpackage
- Replace generally useful macros by regular commands

* Fri Feb 05 2010 Nikolay Ulyanitsky <lystor AT lystor.org.ua> - 1.0-0.1.RC
- Initial package build

