Name:           r2cutter
Version:        0.1.1
Release:        2%{?dist}
Summary:        GUI for radare2 reverse engineering framework

%global         cutter_translations_commit 8e1d24b4040474c681d8db39cb75c0ed66bb5bda


# CC-BY-SA: src/img/icons/
# CC0: src/fonts/Anonymous Pro.ttf
License:        GPLv3 and CC-BY-SA and CC0

URL:            https://github.com/radareorg/r2cutter/
Source0:        https://github.com/radareorg/r2cutter/archive/%{version}/r2cutter-%{version}.tar.gz
Source1:        https://github.com/radareorg/cutter-translations/archive/%{cutter_translations_commit}.tar.gz#/cutter-translations-%{cutter_translations_commit}.tar.gz

Patch0:         https://github.com/radareorg/r2cutter/commit/3e34672e7e2cb2bdba3541f391121e0cf52d508c.patch#/r2cutter-00-unhandled-write.patch
Patch1:         https://github.com/radareorg/r2cutter/commit/19435220bfa377a503a32aa4b0bb660cfd8a274a.patch#/r2cutter-01-unused-iod.patch
Patch2:         https://github.com/radareorg/r2cutter/commit/7d9729bbffe18a87c6039b583c30ea84887bdff1.patch#/r2cutter-02-doubled-enum.patch
Patch3:         https://github.com/radareorg/r2cutter/commit/955d6278363474a3e91aaff4b2ef846b094422ca.patch#/r2cutter-03-unhandled-pipe.patch
Patch4:         https://github.com/radareorg/r2cutter/commit/f9acd9e53ff7bd936a731bfc446461946c6b57a9.patch#/r2cutter-04-uninitialized-menu.patch


BuildRequires:  radare2-devel >= 4.5.0
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

%description
R2Cutter is a Qt and C++ GUI for radare2.
It is the continuation of Cutter before the fork to keep radare2 as backend.
Its goal is making an advanced, customizable and FOSS reverse-engineering
platform while keeping the user experience at mind.
The r2cutter is created by reverse engineers for reverse engineers.
Focus on supporting latest version of radare2.
Recommend the use of system installed libraries/radare2.
Closer integration between r2 and the UI.

%package devel
Summary:        Development files for the r2cutter package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the r2cutter package. See r2cutter package for more
information.


%prep
%autosetup -p1 -n r2cutter-%{version}
tar --strip-component=1 -xvf %{SOURCE1} -C src/translations


%build
%cmake src
%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_metainfodir}
install -pm644 src/org.radare.r2cutter.appdata.xml %{buildroot}%{_metainfodir}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%files
%{_bindir}/r2cutter
%{_datadir}/applications/*.desktop
%{_datadir}/RadareOrg/
%{_metainfodir}/*.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%license COPYING src/img/icons/Iconic-LICENSE
%doc README.md


%files devel
%{_includedir}/r2cutter
%{_libdir}/r2cutter/*.cmake
%dir %{_libdir}/r2cutter


%changelog
* Fri Mar 19 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.1.1-1
- switch from cutter to r2cutter

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
