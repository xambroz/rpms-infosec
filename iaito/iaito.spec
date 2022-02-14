Name:           iaito
Summary:        GUI for radare2 reverse engineering framework
Version:        5.6.0
%global         rel             1
%global         upversion       %{version}-beta
URL:            https://radare.org/n/iaito.html
VCS:            https://github.com/radareorg/iaito/
#               https://github.com/radareorg/iaito/releases


# by default it builds from the released version of radare2
# to build from git use rpmbuild --without=releasetag
%bcond_with     releasetag

%global         gituser         radareorg
%global         gitname         iaito

%global         gitdate         20220206
%global         commit          28a1099603b3fa671bfbb226025d1a8c45558471
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         iaito_translations_commit       93c0bb887c1a0de66d55fb84f3aa75e662a1dfd5

%if %{with releasetag}
Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{rel}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{commit}.tar.gz
%endif


# CC-BY-SA: src/img/icons/
# CC0: src/fonts/Anonymous Pro.ttf
License:        GPLv3 and CC-BY-SA and CC0

Source1:        https://github.com/radareorg/iaito-translations/archive/%{iaito_translations_commit}.tar.gz#/iaito-translations-%{iaito_translations_commit}.tar.gz
Patch0:         iaito-5.6.0-norpath.patch


BuildRequires:  radare2-devel >= 5.5.0
# BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  kf5-syntax-highlighting-devel
BuildRequires:  python3-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  file-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  graphviz-devel
BuildRequires:  qt5-linguist
%ifarch %{qt5_qtwebengine_arches}
BuildRequires:  qt5-qtwebengine-devel
%endif

# Generate documentation
BuildRequires:  doxygen
BuildRequires:  /usr/bin/sphinx-build
BuildRequires:  python3-breathe
BuildRequires:  python3-recommonmark

Requires:       python3-jupyter-client
Requires:       python3-notebook
Requires:       hicolor-icon-theme

# Package iaito was renamed from r2cutter in version 5.2.0
Obsoletes:      r2cutter < 5.2.0
Provides:       r2cutter%{?_isa} = %{version}-%{release}


%description
iaito is a Qt and C++ GUI for radare2.
It is the continuation of Cutter before the fork to keep radare2 as backend.
Its goal is making an advanced, customizable and FOSS reverse-engineering
platform while keeping the user experience at mind.
The iaito is created by reverse engineers for reverse engineers.
Focus on supporting latest version of radare2.
Recommend the use of system installed libraries/radare2.
Closer integration between r2 and the UI.

%package devel
Summary:        Development files for the iaito package
Requires:       %{name}%{?_isa} = %{version}-%{release}

# Package iaito was renamed from r2cutter in version 5.2.0
Obsoletes:      r2cutter-devel < 5.2.0
Provides:       r2cutter-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the iaito package. See iaito package for more
information.

%package doc
Summary:        Documentation for the iaito package
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for the iaito package. See iaito package for more
information.


%prep
%if %{with releasetag}
# Build from git release version
%autosetup -p1 -n %{gitname}-%{version} 
%else
%autosetup -p1 -n %{gitname}-%{commit}
# Rename internal "version-git" to "version"
sed -i -e "s|%{version}-git|%{version}|g;" configure configure.acr
%endif

tar --strip-component=1 -xvf %{SOURCE1} -C src/translations


%build
%cmake -DIAITO_EXTRA_PLUGIN_DIRS=%{_libdir}/iaito src
%cmake_build



cd docs
make html
rm -rf build/html/.buildinfo
mv build/html ../


%install
%cmake_install


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%files
%{_bindir}/iaito
%{_libdir}/iaito
%{_datadir}/RadareOrg/
%{_datadir}/applications/*.desktop
%{_metainfodir}/*.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_mandir}/man1/iaito.1*
%license COPYING src/img/icons/Iconic-LICENSE
%doc README.md


%files devel
%{_includedir}/iaito
%{_libdir}/iaito/*.cmake
%dir %{_libdir}/iaito

%files doc
%doc html

%changelog
* Sun Feb 13 2022 Michal Ambroz <rebus _AT seznam.cz> - 5.6.0-0.1.20220206git28a1099
- bump to git version 20220206git28a1099 to be able to upgrade radare2 to 5.6.0

* Sun Feb 13 2022 Michal Ambroz <rebus _AT seznam.cz> - 5.5.0-0.beta.1
- bump to 5.5.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 15 2021 Ivan Mironov <mironov.ivan@gmail.com> - 5.3.1-5
- Fix plugin search paths

* Mon Oct 04 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 5.3.1-4
- rebuilt with radare2 5.4.2

* Sat Sep 18 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 5.3.1-3
- rebuilt with radare2 5.4.0

* Sat Sep 18 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 5.3.1-2
- rebuilt with radare2 5.4.0

* Wed Jul 21 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 5.3.1-1
- Update to release 5.3.1

* Fri Jun 11 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.2-3
- rebuild with radare2 5.3.1

* Wed Jun 09 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.2-2
- rebuild with radare2 5.3.0

* Thu Apr 29 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.2-1
- bump to 5.2.2

* Sat Apr 24 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.1-1
- bump to 5.2.1

* Wed Apr 21 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.0-3
- fix RIO list

* Fri Apr 16 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.0-2
- name change again -> iaito
- adding doc package
- Add '/usr/lib*/iaito/' to plugin search paths

* Mon Mar 22 2021 Ivan Mironov <mironov.ivan@gmail.com> - 0.1.1-4
- Add '/usr/lib*/r2cutter/' to plugin search paths

* Fri Mar 19 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.1.1-3
- switch from cutter to r2cutter
- cosmetic patches to fix gcc10+ warnings (reported upstream)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.11.0-1
- Bump to upstream version 1.11.0-1 (Thanks to Michal Ambroz, changes mostly
  taken from https://src.fedoraproject.org/rpms/cutter-re/pull-request/2#request_diff)
- Add cutter translations
- Provide -devel sub package to allow compilation of cutter plugins

* Fri May 8 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.2-2
- Just re-build

* Tue May 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.2-1
- Rebase to upstream version 1.10.2

* Tue May 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.1-5
- Re-build for new radare2 release

* Wed Feb 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.1-4
- Just use the right desktop file name and app metadata instead of messing with cutter source code

* Wed Feb 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.1-3
- Rebuild with new radare2

* Wed Feb 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.1-2
- Fix the main window icon

* Mon Feb 3 2020 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.10.1-1
- Rebase to cutter 1.10.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.9.0-2
- Rebuilt for radare2-3.9.0-3

* Mon Sep 30 2019 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.9.0-1
- rebase to cutter 1.9.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.8.3-1
- rebase to cutter 1.8.3

* Wed Jun 26 2019 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.8.0-4
- recompile for radare2 3.6.0

* Mon Apr 15 2019 Riccardo Schirone <rschirone91@gmail.com> - 0.0.1.8.0-3
- recompile for radare2 3.4.1

* Tue Apr 09 2019 Lubomir Rintel <lkundrak@v3.sk> - 0.0.1.8.0-2
- Update to radare2 3.4.1

* Thu Mar 21 2019 Lubomir Rintel <lkundrak@v3.sk> - 0.0.1.8.0-1
- Update to 1.8.0
- Require hicolor-icon-theme
- Move appdata to a correct location
- Fix license field (Robert-André Mauchin, #1690050)

* Thu Mar 14 2019 Lubomir Rintel <lkundrak@v3.sk> - 0.0.1.7.4-1
- Cutter - Initial packaging
