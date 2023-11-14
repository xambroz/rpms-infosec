Name:           cutter-re
Version:        2.3.2
Release:        1%{?dist}
Summary:        GUI for Rizin reverse engineering framework

# CC-BY-SA: src/img/icons/
# CC0: src/fonts/Anonymous Pro.ttf
License:        GPL-3.0-only AND CC-BY-SA-3.0 AND CC0-1.0

URL:            https://cutter.re/
VCS:            https://github.com/rizinorg/cutter
Source0:        https://github.com/rizinorg/cutter/releases/download/v%{version}/Cutter-v%{version}-src.tar.gz
Source1:        cutter-re.desktop
Source2:        cutter-re.appdata.xml

BuildRequires:  rizin-devel >= 0.6.1
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
Cutter is a Qt and C++ GUI for Rizin. Its goal is making an advanced,
customizable and FOSS reverse-engineering platform while keeping the user
experience at mind. Cutter is created by reverse engineers for reverse
engineers.


%package devel
Summary:        Development files for the cutter-re package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the cutter-re package. See cutter-re package for more
information.


%prep
%autosetup -p1 -n Cutter-v%{version}


%build
%cmake -DCUTTER_USE_BUNDLED_RIZIN=OFF
%cmake_build


%install
%cmake_install
mv %{buildroot}%{_bindir}/cutter %{buildroot}%{_bindir}/cutter-re

# replace default .desktop file with our own, to use cutter-re name
mkdir -p %{buildroot}%{_datadir}/applications
rm %{buildroot}%{_datadir}/applications/re.rizin.cutter.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
        %{SOURCE1}

mkdir -p %{buildroot}%{_metainfodir}
install -pm644 %{SOURCE2} \
        %{buildroot}%{_metainfodir}

# rename cutter svg icon to cutter-re
mv %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/{cutter,cutter-re}.svg
sed -i 's/bin\/cutter/bin\/cutter-re/g' %{buildroot}%{_libdir}/cmake/Cutter/CutterTargets-*.cmake

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml


%files
%{_bindir}/cutter-re
%{_datadir}/applications/*.desktop
%{_datadir}/rizin/cutter/translations/*.qm
%{_metainfodir}/*.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%license COPYING src/img/icons/Iconic-LICENSE
%doc README.md


%files devel
%{_includedir}/cutter
%{_libdir}/cmake/Cutter/*.cmake
%dir %{_libdir}/cmake/Cutter


%changelog
* Mon Nov 13 2023 Michal Ambroz <rebus _AT seznam.cz> - 2.3.2-1
- Rebase to version 2.3.2

* Mon Aug 21 2023 Riccardo Schirone <rschirone91@gmail.com> - 2.3.1-1
- Rebase to version 2.3.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 17 2023 Riccardo Schirone <rschirone91@gmail.com> - 2.2.1-1
- Rebase to version 2.2.1

* Tue Mar 14 2023 Riccardo Schirone <rschirone91@gmail.com> - 2.2.0-1
- Rebase to version 2.2.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 13 2022 Riccardo Schirone <rschirone91@gmail.com> - 2.1.2-1
- Rebase to version 2.1.2

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 16 2022 Riccardo Schirone <rschirone91@gmail.com> - 2.1.0-2
- Fix cutter path in .cmake file for -devel package

* Tue Jun 28 2022 Riccardo Schirone <rschirone91@gmail.com> - 2.1.0-1
- Rebase to version 2.1.0 which uses Rizin 0.4.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Riccardo Schirone <rschirone91@gmail.com> - 2.0.4-2
- Rebuild for Rizin 0.3.4

* Mon Nov 29 2021 Riccardo Schirone <rschirone91@gmail.com> - 2.0.4-1
- Rebase to version 2.0.4 which uses Rizin 0.3.1

* Mon Sep 27 2021 Riccardo Schirone <rschirone91@gmail.com> - 2.0.3-1
- Rebase to version 2.0.3 which uses Rizin 0.3.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 12 2021 Riccardo Schirone <rschirone91@gmail.com> - 2.0.1-1
- Rebase to version 2.0.1 which uses Rizin 0.2.0

* Fri Apr 2 2021 Riccardo Schirone <rschirone91@gmail.com> - 2.0.0-1
- Rebase to version 2.0.0 which uses Rizin

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.11.0-1
- Bump to upstream version 1.11.0-1 (Thanks to Michal Ambroz, changes mostly
  taken from https://src.fedoraproject.org/rpms/cutter-re/pull-request/2#request_diff)
- Add cutter translations
- Provide -devel sub package to allow compilation of cutter plugins

* Fri May 8 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.2-2
- Just re-build

* Tue May 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.2-1
- Rebase to upstream version 1.10.2

* Tue May 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.1-5
- Re-build for new radare2 release

* Wed Feb 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.1-4
- Just use the right desktop file name and app metadata instead of messing with cutter source code

* Wed Feb 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.1-3
- Rebuild with new radare2

* Wed Feb 5 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.1-2
- Fix the main window icon

* Mon Feb 3 2020 Riccardo Schirone <rschirone91@gmail.com> - 1.10.1-1
- Rebase to cutter 1.10.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Riccardo Schirone <rschirone91@gmail.com> - 1.9.0-2
- Rebuilt for radare2-3.9.0-3

* Mon Sep 30 2019 Riccardo Schirone <rschirone91@gmail.com> - 1.9.0-1
- rebase to cutter 1.9.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Riccardo Schirone <rschirone91@gmail.com> - 1.8.3-1
- rebase to cutter 1.8.3

* Wed Jun 26 2019 Riccardo Schirone <rschirone91@gmail.com> - 1.8.0-4
- recompile for radare2 3.6.0

* Mon Apr 15 2019 Riccardo Schirone <rschirone91@gmail.com> - 1.8.0-3
- recompile for radare2 3.4.1

* Tue Apr 09 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.0-2
- Update to radare2 3.4.1

* Thu Mar 21 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.0-1
- Update to 1.8.0
- Require hicolor-icon-theme
- Move appdata to a correct location
- Fix license field (Robert-André Mauchin, #1690050)

* Thu Mar 14 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.7.4-1
- Initial packaging
