Name:           iaito
Version:        5.2.0
Release:        1%{?dist}
Summary:        GUI for radare2 reverse engineering framework

%global         iaito_translations_commit 9e4b6de0d1cbf8f8bf077240b54532cc32b384b4


# CC-BY-SA: src/img/icons/
# CC0: src/fonts/Anonymous Pro.ttf
License:        GPLv3 and CC-BY-SA and CC0

URL:            https://github.com/radareorg/iaito/
Source0:        https://github.com/radareorg/iaito/archive/%{version}/iaito-%{version}.tar.gz
Source1:        https://github.com/radareorg/iaito-translations/archive/%{iaito_translations_commit}.tar.gz#/iaito-translations-%{iaito_translations_commit}.tar.gz

# FIXED 5.2.0 - Cosmetics - GCC10 compilation warnings - Fix unhandled pipe return code
# reported to upstream https://github.com/radareorg/iaito/issues/10
# Patch0:         https://github.com/radareorg/iaito/commit/3e34672e7e2cb2bdba3541f391121e0cf52d508c.patch#/iaito-00-unhandled-write.patch


# FIXED 5.2.0 - Cosmetics - GCC10 compilation warnings - get rid of unused iod variable
# reported to upstream https://github.com/radareorg/iaito/issues/9
# Patch1:         https://github.com/radareorg/iaito/commit/19435220bfa377a503a32aa4b0bb660cfd8a274a.patch#/iaito-01-unused-iod.patch

# FIXED 5.2.0 - Cosmetics - GCC10 compilation warnings - Two definitions of the ColumnIndex
# reported to upstream https://github.com/radareorg/iaito/issues/8
# Patch2:         https://github.com/radareorg/iaito/commit/7d9729bbffe18a87c6039b583c30ea84887bdff1.patch#/iaito-02-doubled-enum.patch

# FIXED 5.2.0 - Cosmetics - GCC10 compilation warnings - Fix unhandled pipe return code
# reported to upstream https://github.com/radareorg/iaito/pull/11
# Patch3:         https://github.com/radareorg/iaito/commit/955d6278363474a3e91aaff4b2ef846b094422ca.patch#/iaito-03-unhandled-pipe.patch

# FIXED 5.2.0 - Cosmetics - GCC10 compilation warnings - Avoid warning about uninitialized menu
# reported to upstream https://github.com/radareorg/iaito/pull/12
# Patch4:         https://github.com/radareorg/iaito/commit/f9acd9e53ff7bd936a731bfc446461946c6b57a9.patch#/iaito-04-uninitialized-menu.patch


BuildRequires:  radare2-devel >= 5.2.0
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
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
Requires:       python3-jupyter-client
Requires:       python3-notebook
Requires:       hicolor-icon-theme

Obsoletes:      r2cutter < 5.1.1
Obsoletes:      r2cutter-devel < 5.1.1



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

%description devel
Development files for the iaito package. See iaito package for more
information.


%prep
%autosetup -p1 -n iaito-%{version}
tar --strip-component=1 -xvf %{SOURCE1} -C src/translations

mv src/org.radare.r2cutter.desktop src/org.radare.iaito.desktop
mv src/org.radare.r2cutter.appdata.xml src/org.radare.iaito.appdata.xml

# Icon inst
sed -i -e 's/^Icon=iaito$/Icon=iaito-o/' src/org.radare.iaito.desktop

%build
%cmake src
%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_metainfodir}
install -pm644 src/org.radare.iaito.appdata.xml %{buildroot}%{_metainfodir}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%files
%{_bindir}/iaito
%{_datadir}/applications/*.desktop
%{_datadir}/RadareOrg/
%{_metainfodir}/*.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%license COPYING src/img/icons/Iconic-LICENSE
%doc README.md


%files devel
%{_includedir}/iaito
%{_libdir}/iaito/*.cmake
%dir %{_libdir}/iaito


%changelog
* Fri Mar 19 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.0-1
- name change again -> iaito

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
