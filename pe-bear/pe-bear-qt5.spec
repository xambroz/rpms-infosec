Name:           pe-bear
Version:        0.5.3.2
Release:        1%{?dist}
Summary:        reversing tool for PE files

# pe-bear package licensed as "freeware" but closed source
# https://hshrzd.wordpress.com/pe-bear/
# https://web.archive.org/web/20170711210758/https://hshrzd.wordpress.com/pe-bear/
#
# it contains embedded udis86 library - licensed with 2-clause BSD license
License:        freeware
URL:            https://hshrzd.wordpress.com/pe-bear/
VCS:            https://github.com/hasherezade/pe-bear-releases

%global         gituser         hasherezade
%global         gitname         pe-bear-releases
%global         debug_package   %{nil}

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
NoSource:       0
Source1:        https://github.com/%{gituser}/%{gitname}/releases/download/%{version}/PE-bear_%{version}_x64_linux.tar.xz
NoSource:       1
Source2:        pe-bear.desktop
BuildArch:      x86_64

Requires:       bzip2-libs
Requires:       compat-openssl10
Requires:       expat
Requires:       fontconfig
Requires:       freetype
Requires:       glib2
Requires:       glibc
Requires:       libffi
Requires:       libgcc
Requires:       libICE
Requires:       libpng
Requires:       libSM
Requires:       libstdc++
Requires:       libuuid
Requires:       libX11
Requires:       libXau
Requires:       libxcb
Requires:       libXcursor
Requires:       libXext
Requires:       libXfixes
Requires:       libXi
Requires:       libXinerama
Requires:       libXrandr
Requires:       libXrender
Requires:       pcre
Requires:       qt
Requires:       qt-x11
Requires:       zlib

Provides:       bundled(capstone)

%description
PE-bear is a freeware reversing tool for PE files.
Its objective was to deliver fast and flexible “first view” tool for malware
analysts, stable and capable to handle malformed PE files.


%prep
# ======================= prep =======================================
%autosetup -n "%{gitname}-%{version}"
tar xJvf  %{SOURCE1} --strip-components=1


%build
# ======================= build ======================================
echo Do nothing for the build

%install
# ======================= install ====================================

# Install binary
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 PE-bear %{buildroot}/%{_bindir}/PE-bear
ln -s %{_bindir}/PE-bear %{buildroot}/%{_bindir}/%{name}

# Install application launcher with icon
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps
install -m 0644 logo/main_ico.png %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop



%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :



%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
        touch --no-create %{_datadir}/icons/hicolor &>/dev/null
        gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi



%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :




%files
# ======================= files ======================================
#%doc
%{_bindir}/PE-bear
%{_bindir}/pe-bear
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%changelog
* Thu Sep 19 2019 Michal Ambroz <rebus at, seznam.cz> - 0.3.9.5-1
- update to 0.3.9.5

* Tue Apr 03 2018 Michal Ambroz <rebus at, seznam.cz> - 0.3.8-1
- initial fedora package

