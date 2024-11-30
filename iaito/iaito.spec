Name:           iaito
Summary:        GUI for radare2 reverse engineering framework
Version:        5.9.9
# %%global      upversion       %%{version}-beta
URL:            https://radare.org/n/iaito.html
%global         urlvcs          https://github.com/radareorg/iaito
VCS:            git:%{urlvcs}
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
%global         gitdate         20241121
%global         commit          465cf40df7642fe708ab41f66a5aeff127098cc6
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         iaito_translations_gitdate      20221114
%global         iaito_translations_commit       e66b3a962a7fc7dfd730764180011ecffbb206bf
%global         iaito_translations__shortcommit %(c=%{iaito_translations_commit}; echo ${c:0:7})


%if %{with releasetag}
Release:        %autorelease
Source0:        %{urlvcs}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        %{urlvcs}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
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
# BuildRequires:  python3-devel
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

# BuildRequires:  python3-breathe
# BuildRequires:  python3-recommonmark

# Requires:       python3-jupyter-client
# Requires:       python3-notebook
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

# RHEL up to 9 doesn't know url type of vcs-browser
%if ( 0%{?rhel} && 0%{?rhel} <= 9 )
    sed -i -e '/type="vcs-browser"/d;' src/org.radare.iaito.appdata.xml
%endif

# RHEL up to 8 doesn't know url type of bugtracker, contact
%if ( 0%{?rhel} && 0%{?rhel} <= 8 )
    sed -i -e '/<url type="bugtracker"/d; /<url type="contact"/d;' src/org.radare.iaito.appdata.xml
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
%autochangelog