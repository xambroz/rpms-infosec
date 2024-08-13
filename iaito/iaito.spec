Name:           iaito
Summary:        GUI for radare2 reverse engineering framework
Version:        5.9.4
%global         baserelease     1
# %%global      upversion       %%{version}-beta
URL:            https://radare.org/n/iaito.html
VCS:            https://github.com/radareorg/iaito/
#               https://github.com/radareorg/iaito/releases
#               https://github.com/radareorg/iaito-translations/


%if 0%{?fedora} && 0%{?fedora} == 36
# there is issue on F36 with the missing note file
# https://bugzilla.redhat.com/show_bug.cgi?id=2043178
%undefine _package_note_file
%endif


# by default it builds from the released version of radare2
# to build from git use rpmbuild --without=releasetag
%bcond_without     releasetag

%global         gituser         radareorg
%global         gitname         iaito
%global         gitdate         20240808
%global         commit          dc51d5fe1604596d0278bd7cc7d2c589a4ec1671
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         iaito_translations_gitdate      20221114
%global         iaito_translations_commit       e66b3a962a7fc7dfd730764180011ecffbb206bf
%global         iaito_translations__shortcommit %(c=%{iaito_translations_commit}; echo ${c:0:7})


%if %{with releasetag}
Release:        %{baserelease}%{?dist}
Source0:        %{vcs}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        %{vcs}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif


# CC-BY-SA: src/img/icons/
# CC0: src/fonts/Anonymous Pro.ttf
License:        GPL-3.0-only AND CC-BY-SA-3.0 AND CC0-1.0

Source1:        https://github.com/radareorg/iaito-translations/archive/%{iaito_translations_commit}.tar.gz#/iaito-translations-git%{iaito_translations_gitdate}.tar.gz
Patch0:         iaito-5.8.8-norpath.patch

BuildRequires:  radare2-devel >= 5.6.8
# BuildRequires:  git
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
# BuildRequires:  doxygen
# BuildRequires:  /usr/bin/sphinx-build

BuildRequires:  python3-breathe
BuildRequires:  python3-recommonmark

Requires:       python3-jupyter-client
Requires:       python3-notebook
Requires:       hicolor-icon-theme

# Package iaito was renamed from r2cutter in version 5.2.0
Obsoletes:      r2cutter < 5.2.0
Provides:       r2cutter%{?_isa} = %{version}-%{release}

# There used to be iaito-doc package
Obsoletes:      iaito-doc < 5.6.0-0.3.20220303gitafaa7df
# Provides:       iaito-doc = %%{version}-%%{release}

# cmake files removed with 5.7.2
Obsoletes:      iaito-devel < 5.6.0-0.6

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

# %%package doc
# Summary:        Documentation for the iaito package
# BuildArch:      noarch
# Requires:       %%{name} = %%{version}-%%{release}

# %%description doc
# Documentation for the iaito package. See iaito package for more
# information.


%prep
%if %{with releasetag}
# Build from git release version
%autosetup -p1 -n %{gitname}-%{version}
%else
%autosetup -p1 -n %{gitname}-%{commit}
# Rename internal "version-git" to "version"
sed -i -e "s|%{version}-git|%{version}|g;" configure configure.acr
%endif

# RHEL up to 9 do not know uel type of vcs-browser
%if ( 0%{?rhel} && 0%{?rhel} <= 9 )
    sed -i -e '/type="vcs-browser"/d;' src/org.radare.iaito.appdata.xml
%endif

[ -d src/translations ] || mkdir -p src/translations
tar --strip-component=1 -xvf %{SOURCE1} -C src/translations

# Honor parallel jobs number
sed -i Makefile -e '\@MAKE@s|-j4|%_smp_mflags|'

# Honor Fedora compiler flags
sed -i src/Iaito.pro \
    -e 's|^QMAKE_CXXFLAGS +=.*$|QMAKE_CXXFLAGS += %build_cxxflags\nQMAKE_LFLAGS += %build_ldflags|' \
    %{nil}

# Change prefix
sed -i src/Iaito.pro -e 's|/usr/local|%_prefix|'

# Tweak path to find qmake, lrelease with -qt5 suffix
mkdir TMPBINDIR
cd TMPBINDIR
ln -sf %_bindir/qmake-qt5 qmake
ln -sf %_bindir/lrelease-qt5 lrelease
cd ..

%build
export PATH=$(pwd)/TMPBINDIR:$PATH

%configure
%make_build

# In 2e5cb221f55d9e4127d576ae4033f6d448e0f812 the current documentation was removed
# cd docs
# make html
# rm -rf build/html/.buildinfo
# mv build/html ../


%install
export PATH=$(pwd)/TMPBINDIR:$PATH
# don't strip binary
%make_install STRIP=true
make install-translations DESTDIR=%{?buildroot}

# Move files manually
# mkdir -p %%{buildroot}%%{_mandir}/man1
# cp -p ./src/iaito.1 %%{buildroot}%%{_mandir}/man1/

%find_lang %name --with-qt

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%{_bindir}/iaito
%dir %{_datadir}/iaito/
%dir %{_datadir}/iaito/translations
%{_datadir}/applications/*.desktop
%{_metainfodir}/*.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_mandir}/man1/iaito.1*
%license COPYING src/img/icons/Iconic-LICENSE
%doc README.md


%changelog
* Mon Aug 12 2024 Michal Ambroz <rebus _AT seznam.cz> - 5.9.4-1
- bump to 5.9.4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 24 2024 Michal Ambroz <rebus _AT seznam.cz> - 5.9.2-1
- bump to 5.9.2

* Thu May 23 2024 Michal Ambroz <rebus _AT seznam.cz> - 5.9.0-2
- rebuild with radare2 5.9.2

* Sun May 05 2024 Michal Ambroz <rebus _AT seznam.cz> - 5.9.0-1
- rebuild with radare2 5.9.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.8-4
- rebuild with capstone 5.0.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 09 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.8-2
- rebuild with radare2 5.8.8

* Wed Jul 05 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.8-1
- bump to 5.8.8

* Mon Apr 10 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.4-2
- rebuild with fixed radare2 5.8.5

* Wed Mar 29 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.4-1
- bump to 5.8.4

* Fri Feb 03 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.2-1
- bump to 5.8.2

* Thu Jan 26 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.0-1
- bump to 5.8.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.8-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 27 2022 Michal Ambroz <rebus _AT seznam.cz> - 5.7.8-1
- bump to 5.7.8

* Tue Oct 04 2022 Michal Ambroz <rebus _AT seznam.cz> - 5.7.6-1
- bump to 5.7.6

* Mon Sep 19 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.7.2-1
- 5.7.2
- build system switched from cmake to configure / make

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.5.20220303gitb8a42d8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Henrik Nordstrom <henrik@henriknordstrom.net> - 5.6.0-0.5.20220303gitb8a42d8
- rebuilt with radare2 5.6.8

* Thu Mar 03 2022 Michal Ambroz <rebus _AT seznam.cz> - 5.6.0-0.3.20220303gitafaa7df
- fixes issue in disassembly with not visible arguments
- remove the obsolete docs

* Tue Mar 01 2022 Michal Ambroz <rebus _AT seznam.cz> - 5.6.0-0.2.20220206git28a1099
- rebuild with radare2 5.6.4
- add missing include #2059619 to compile with the new version of highlighting

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
