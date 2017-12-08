%global         gituser         XQF
%global         gitname         xqf
%global         commit          97afad6998a2625789aae5002c748a3d3ae07c33
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           xqf
Version:        1.0.6.2
Release:        1%{?dist}
Summary:        Server browser for many popular games

Group:          Amusements/Games
License:        GPLv2+
#               http://www.linuxgames.com/xqf/
#               https://github.com/XQF/xqf/releases
URL:            http://xqf.github.io/
#Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source:         https://github.com/%{gituser}/%{gitname}/archive/xqf-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Patch0:         %{name}-%{version}-launch.patch
Patch1:		%{name}-libs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       qstat >= 2.11
BuildRequires:  GeoIP-devel
BuildRequires:  qstat
BuildRequires:  gettext
BuildRequires:  zlib-devel
BuildRequires:  glib
BuildRequires:  gtk2-devel
BuildRequires:  intltool
BuildRequires:  perl-XML-Parser
BuildRequires:  desktop-file-utils
BuildRequires:  readline-devel
BuildRequires:  gdk-pixbuf2
BuildRequires:  gdk-pixbuf2-xlib-devel


%description
XQF is a game server browser and launcher for Unix/X11 for many popular games 
such as the Quake series, Unreal Tournament series, Half-Life etc.
XQF is a front-end to QStat, a program by Steve Jankowski 
and uses the GTK+ toolkit.

%prep
%setup -q -n %{name}-%{name}-%{version}
#%patch0 -p0
#%patch1 -p1



%build
./autogen.sh
%configure \
   --with-qstat=%{_bindir}/quakestat \
   --enable-geoip \
   --enable-bzip2 \
   --enable-externalrcon \
   --enable-gtk2

make %{?_smp_mflags} CFLAGS="%{optflags}"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install \
       --dir=%{buildroot}%{_datadir}/applications \
       %{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

install -p -m 0644 pixmaps/%{name}_32x32.png \
        %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

%find_lang %{name}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%{_bindir}/%{name}-rcon
%{_datadir}/pixmaps/%{name}_*.png
%{_datadir}/pixmaps/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
%{_mandir}/man6/%{name}.6.*


%changelog
* Fri Dec 8 2017 Michal Ambrz <rebus _AT seznam.cz> - 1.0.6.2-1
- bump to 1.0.6.2, rebuild for F27

* Sun Jan 03 2010 Vivek Shah <boni.vivek at gmail.com> - 1.0.5-10
- Fix RHBZ #551990
- Fixed dependency issues

* Sun Nov 08 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 1.0.5-9
- Fix RHBZ #533704 #533705
- Cosmetical changes

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 07 2009 Stefan Posdzich <cheekyboinc@foresightlinux.org> - 1.0.5-7
- Added new icon cache scriptlets
- Fixed "Bug 503695 - Xqf freezes with 100% CPU"

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Stefan Posdzich <cheekyboinc@foresightlinux.org> - 1.0.5-5
- Remove BuildRequires: glibc-devel

* Wed Jun 18 2008 Stefan Posdzich <cheekyboinc@foresightlinux.org> - 1.0.5-4
- Add new .desktop file source
- Remove BuildRequires: gtk+-devel, glib2-devel
- Remove desktop-file-install --remove-category=X-SuSE-Core-Game and {name}.desktop

* Mon Jun 16 2008 Stefan Posdzich <cheekyboinc@foresightlinux.org> - 1.0.5-3
- Add --enable-bzip2 for bzip2 data compression
- Add --enable-externalrco (Remote server administration tool)
- Add BuildRequires: readline-devel
- Add correct url for Source:
- Add gtk-update-icon-cache

* Sun Jun 15 2008 Stefan Posdzich <cheekyboinc@foresightlinux.org> - 1.0.5-2
- Add desktop-file-install for the .desktop file
- Add BuildRequires: GeoIP-devel, qstat
- Remove the dummy libGeoIP.so
- Remove Requires: GeoIP

* Fri Jun 13 2008 Stefan Posdzich <cheekyboinc@foresightlinux.org> - 1.0.5-1
- Initial SPEC file
