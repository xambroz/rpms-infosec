Name:           iaito
Version:        5.2.2
Release:        2%{?dist}
Summary:        GUI for radare2 reverse engineering framework

%global         iaito_translations_commit       93c0bb887c1a0de66d55fb84f3aa75e662a1dfd5


# CC-BY-SA: src/img/icons/
# CC0: src/fonts/Anonymous Pro.ttf
License:        GPLv3 and CC-BY-SA and CC0

URL:            https://github.com/radareorg/iaito/
Source0:        https://github.com/radareorg/iaito/archive/%{version}/iaito-%{version}.tar.gz
Source1:        https://github.com/radareorg/iaito-translations/archive/%{iaito_translations_commit}.tar.gz#/iaito-translations-%{iaito_translations_commit}.tar.gz


BuildRequires:  radare2-devel >= 5.2.0
BuildRequires:  git
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

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  cmake
BuildRequires:  cmake-rpm-macros
%else
BuildRequires:  cmake3
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
%autosetup -p1 -n iaito-%{version} -S git_am
tar --strip-component=1 -xvf %{SOURCE1} -C src/translations


%build
%cmake3 -DAIATO_EXTRA_PLUGIN_DIRS=%{_libdir}/iaito src
%cmake3_build



cd docs
make html
rm -rf build/html/.buildinfo
mv build/html ../


%install
%cmake3_install


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
* Sat May 22 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.2.2-2
- trying build for EPEL

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
