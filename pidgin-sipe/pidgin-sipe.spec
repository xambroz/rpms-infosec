Name:           pidgin-sipe
Summary:        Pidgin protocol plugin to connect to MS Office Communicator
Version:        1.23.2
Release:        2%{?dist}

Group:          Applications/Communications
License:        GPLv2+
URL:            http://sipe.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/sipe/sipe/pidgin-sipe-%{version}/pidgin-sipe-%{version}.tar.bz2

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(farstream-0.2)
BuildRequires:  pkgconfig(gio-2.0) >= 2.18.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.18.0
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.18.0
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-rtp-1.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(nice) >= 0.1.0
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(purple) >= 2.8.0
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gssntlmssp-devel >= 0.5.0
BuildRequires:  intltool
BuildRequires:  libtool

Requires:       purple-sipe = %{version}-%{release}

# Called from commandline to establish the RDP screen sharing
Requires:       remmina
Requires:       remmina-plugins-rdp


%description
A third-party plugin for the Pidgin multi-protocol instant messenger.
It implements the extended version of SIP/SIMPLE used by various products:

    * Skype for Business
    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)

With this plugin you should be able to replace your Microsoft Office
Communicator client with Pidgin.

This package provides the icon set for Pidgin.


%package -n purple-sipe
Summary:        Libpurple protocol plugin to connect to MS Office Communicator
Group:          Applications/Communications
License:        GPLv2+

Requires:       gssntlmssp >= 0.5.0

%description -n purple-sipe
A third-party plugin for the Pidgin multi-protocol instant messenger.
It implements the extended version of SIP/SIMPLE used by various products:

    * Skype for Business
    * Microsoft Office 365
    * Microsoft Business Productivity Online Suite (BPOS)
    * Microsoft Lync Server
    * Microsoft Office Communications Server (OCS 2007/2007 R2)
    * Microsoft Live Communications Server (LCS 2003/2005)

This package provides the protocol plugin for libpurple clients.


%prep
%setup -q

%build
autoreconf -f -i
%configure \
    --with-krb5 \
    --enable-purple \
    --disable-telepathy
%make_build


%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
# Pidgin doesn't have 24 or 32 pixel icons
rm -f \
   %{buildroot}%{_datadir}/pixmaps/pidgin/protocols/24/sipe.png \
   %{buildroot}%{_datadir}/pixmaps/pidgin/protocols/32/sipe.png
%find_lang %{name}


%check
%make_build check



%files -n purple-sipe -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_libdir}/purple-2/libsipe.so


%files
%defattr(-,root,root,-)
%{_datadir}/appdata/%{name}.metainfo.xml
%{_datadir}/pixmaps/pidgin/protocols/*/sipe.*


%changelog
* Fri Apr 27 2018 Michal Ambroz <rebus AT_ seznam.cz> - 1.23.2-2
- add missing runtime dependency to remmina, remmina-plugins-rdp

* Sat Mar 10 2018 Stefan Becker <chemobejk@gmail.com> - 1.23.2-1
- update to 1.23.2:
    - fix some HTTP requests that were not sent

* Sun Feb 25 2018 Stefan Becker <chemobejk@gmail.com> - 1.23.1-1
- update to 1.23.1:
    - add support for user redirect in Lync autodiscover
    - enable audio/video calls for Office365 cloud-based accounts
- drop obsolete patch for GCC 8.0 compilation error

* Sun Feb 18 2018 Stefan Becker <chemobejk@gmail.com> - 1.23.0-5
- add BR gcc

* Sun Feb 18 2018 Stefan Becker <chemobejk@gmail.com> - 1.23.0-4
- change source URL to https://

* Tue Feb 13 2018 Stefan Becker <chemobejk@gmail.com> - 1.23.0-3
- add upstream patch to fix build failure on rawhide

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 28 2017 Stefan Becker <chemobejk@gmail.com> - 1.23.0-1
- update to 1.23.0:
    - add support for IPv6 addresses in SIP & SDP messages
    - extend libpurple D-Bus interface
    - don't load buddy photos from unknown sites by default
- add BR dbus-1, gstreamer-rtp-1.0 & krb5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 11 2017 Stefan Becker <chemobejk@gmail.com> - 1.22.1-1
- update to 1.22.1:
    - fix multiple client detection
    - speed up Lync Autodiscover
    - avoid rare SSL read deadlock
    - various bug fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Stefan Becker <chemobejk@gmail.com> - 1.22.0-1
- update to 1.22.0:
    - add support for Application Sharing Viewer
    - add support for Lync Autodiscover
    - separate logging and debugging output
- add BR farstream-0.2 & gio-2.0

* Sat May 28 2016 Stefan Becker <chemobejk@gmail.com> - 1.21.1-1
- update to 1.21.1:
    - various bug fixes in media support

* Thu May 05 2016 Stefan Becker <chemobejk@gmail.com> - 1.21.0-2
- add patch to fix configure failure on F23+ x86_64 (bz #1333438)

* Sat Apr 23 2016 Stefan Becker <chemobejk@gmail.com> - 1.21.0-1
- update to 1.21.0:
    - add support for Lync File Transfer
    - support embedded XML as buddy photo URL
    - improve "Join scheduled conference" dialog
    - add AppStream metadata file

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 24 2015 Stefan Becker <chemobejk@gmail.com> - 1.20.1-1
- update to 1.20.1:
    - add support for another type of ADFS response
    - improve configure check for back-ported features

* Sat Aug 29 2015 Stefan Becker <chemobejk@gmail.com> - 1.20.0-2
- add build fix for heavily patched libpurple-2.10.11 on F22+

* Sat Aug 29 2015 Stefan Becker <chemobejk@gmail.com> - 1.20.0-1
- update to 1.20.0:
    - add support for SRTP (requires libpurple >= 3.0.0)
    - parse HTML from Lync conference URL
    - fixes Office365 authentication failure (bz #1257485)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 04 2015 Stefan Becker <chemobejk@gmail.com> - 1.19.1-1
- update to 1.19.1:
    - add workaround for farstream 0.1.x with libnice >= 0.1.10
    - fix SIP re-authentication timeout to be max. 8 hours
- drop obsolete patches

* Wed Mar 18 2015 David Woodhouse <dwmw2@infradead.org> - 1.19.0-3
- add upstream patch to ignore TCP candidates with newer libnice
- add upstream patch to build against same GStreamer as Pidgin

* Sun Feb 08 2015 Stefan Becker <chemobejk@gmail.com> - 1.19.0-2
- add upstream patch to fix GCC 5.0 compilation errors on F22+

* Sat Feb 07 2015 Stefan Becker <chemobejk@gmail.com> - 1.19.0-1
- update to 1.19.0:
    - added support for automatic authentication scheme selection
    - added support for Multi-Factor Authentication (MFA)
    - added support for buddy photos from contact card
    - added support for SIP ID in contact search
    - added support for EWS based contact search when UCS is used
    - improves user experience for [MS-DLX] based contact search
    - fixes calendar state machine when EWS URL is set
- Fedora Packaging Guidelines: use license tag instead of doc

* Mon Dec 29 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.5-1
- update to 1.18.5:
    - fixes Pidgin user status being stuck in "Away"
    - fixes RealmInfo request when user and login name differ

* Sat Oct 18 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.4-1
- update to 1.18.4:
    - fixes ADFS failure when user and login name differ
    - fixes a longstanding issue that the Pidgin user status sometimes
      didn't switch back to "Available" after the end of a meeting
    - fixes some memory leaks

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 16 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.3-1
- update to 1.18.3:
    - fixes audio/video call if host has IPv6 address (bz #1124510)
    - fixes assert triggered by EWS autodiscover in older libxml2 versions
    - fixes crash triggered by EWS autodiscover when glib2 < 2.30.0
- add dependency on gssntlmssp(-devel) >= 0.5.0 for F21+

* Sat Jun 07 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.2-1
- update to 1.18.2:
    - fixes crash when PersistentChat sends BYE
    - fixes joining of conference for some users
    - fixes conference call ending in error message
    - fixes EWS autodiscover for some Office 365 users
    - UCS now honors email URL set by user

* Sat Apr 12 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.1-1
- update to 1.18.1:
    - fixes crash when gstreamer nice plugin is missing (bz #1071710)
    - fixes false "not delivered" errors in conference
    - fixes incorrect HTML escaping for URLs
    - fixes conference call ending in error message
    - fixes endless loop with failed HTTP Basic authentication
    - fixes EWS autodiscover for some Office 365 users
    - fixes missing "Copy to" in buddy menu

* Sun Mar 09 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.0-4
- drop gmime-2.6 from BRs

* Sun Mar 09 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.0-3
- Fedora Packaging Guidelines: use pkgconfig() for BRs

* Tue Mar 04 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.0-2
- add dependency on libnice-gstreamer for F20+ (bz #1071710)

* Sat Jan 11 2014 Stefan Becker <chemobejk@gmail.com> - 1.18.0-1
- update to 1.18.0:
    - added support for EWS Autodiscover redirection

* Wed Dec 11 2013 Stefan Becker <chemobejk@gmail.com> - 1.17.3-1
- update to 1.17.3:
    - fixes crash when groupchat session expired (again)
    - fixes HTTP re-authentication with NTLM
    - fixes UCS Persona key extraction

* Sat Nov 30 2013 Stefan Becker <chemobejk@gmail.com> - 1.17.2-1
- update to 1.17.2:
    - fixes problems with typing notifications fix (bz #1031554)
    - fixes crash when groupchat session expired

* Sat Nov 16 2013 Stefan Becker <chemobejk@gmail.com> - 1.17.1-1
- update to 1.17.1:
    - fixes typing notifications
    - fixes that passwords were not entity encoded
    - accept alternatives for webticket timestamp/keydata

* Sat Sep 21 2013 Stefan Becker <chemobejk@gmail.com> - 1.17.0-1
- update to 1.17.0:
    - added Lync 2013 support: buddy list modification, buddy photo, group chat
    - added support for group chat history
    - fixes group chat: duplicate messages & users, HTML tags in text
    - fixes EWS autodiscover for Office 365

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Stefan Becker <chemobejk@gmail.com> - 1.16.1-1
- update to 1.16.1: bug fix release
    - fixes call failure when host has multiple IP addresses
    - fixes buddy list handling after moving to Lync 2013
    - fixes crashes in new HTTP stack

* Sat Jun 15 2013 Stefan Becker <chemobejk@gmail.com> - 1.16.0-1
- update to 1.16.0:
    - new HTTP stack: reduced network traffic, no more crashes
    - added support to call to a phone number
    - fixes subscription timeout handling, e.g. for buddy status updates

* Sun Apr 07 2013 Stefan Becker <chemobejk@gmail.com> - 1.15.1-1
- update to 1.15.1: bug fix release
    - fixes crash experienced by some users (bz #928323)
    - fixes broken NTLM fallback in Negotiate

* Sat Mar 09 2013 Stefan Becker <chemobejk@gmail.com> - 1.15.0-1
- update to 1.15.0:
    - added support for Kerberos & Negotiate authentication in HTTP connections
    - added support for DNS A record search in server auto-discovery
    - added setting to suppress calendar information publishing
    - unified Single Sign-On (SSO) handling in all places

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 26 2012 Stefan Becker <chemobejk@gmail.com> - 1.14.1-1
- update to 1.14.1: bug fix release

* Sun Dec 16 2012 Stefan Becker <chemobejk@gmail.com> - 1.14.0-1
- update to 1.14.0:
    - added support for Web Ticket authentication using ADFS
    - added support for buddy photos
    - added support for call to Audio Test Service
    - reduced network traffic for acquiring Web Tickets

* Sun Aug 19 2012 Stefan Becker <chemobejk@gmail.com> - 1.13.3-1
- update to 1.13.3: bug fix release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Stefan Becker <chemobejk@gmail.com> - 1.13.2-1
- update to 1.13.2: bug fix release

* Mon Apr 09 2012 Stefan Becker <chemobejk@gmail.com> - 1.13.1-1
- update to 1.13.1: bug fix release
- drop obsolete patch for GCC 4.7.0 compilation errors

* Wed Mar 14 2012 Stefan Becker <chemobejk@gmail.com> - 1.13.0-2
- add patch to fix maybe-uninitialized errors for F17+

* Wed Mar 14 2012 Stefan Becker <chemobejk@gmail.com> - 1.13.0-1
- update to 1.13.0:
    - support for Lync & Office365
    - added [MS-SIPAE] TLS-DSK authentication scheme
    - added [MS-DLX] based Get Info/Contact Search
    - added experimental media TCP transport
- add BR nss-devel
- drop obsolete patch to replace deprecated glib2 functions

* Mon Jan 09 2012 Stefan Becker <chemobejk@gmail.com> - 1.12.0-3
- add patch to replace deprecated glib2 functions for F17+

* Sun Jan 08 2012 Stefan Becker <chemobejk@gmail.com> - 1.12.0-2
- enable audio/video call support for F15+ (bz #761528)

* Mon Sep 12 2011 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.12.0-1
- Update to 1.12.0:
    - Add support for OCS2007R2 Group Chat
    - Miscellaneous features and bugfixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.11.2-1
- Update to 1.11.2

* Wed Oct 06 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0

* Fri Sep 24 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-2
- Fix group for purple-sipe (#624246)

* Fri Jul 16 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-1
- Upstream 1.10.1:
        - Fixes to build against pidgin-2.7
        - Initial support for Office 2007+ "Access Levels"
        - SVG icon artwork
        - Miscellaneous bugfixes

* Tue Mar 16 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.9.1-1
- Upstream 1.9.1:
        - Fix Kerberos authentication for unix platforms (broken in 1.9.0)
        - Bugfixes

* Thu Mar 11 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.9.0-1
- Upstream 1.9.0:
        - Contributed File transfer functionality. File encryption is supported.
        - NTLMv2 and NTLMv2 Session Security support
        - Implemented SIP Authentication Extensions protocol version 4 and 3
        - another shot at presence update problems
        - fix crash caused by uninitialized security contexts
        - Updated translations: ru, de, es, pt_BR
        - Bugfixes and crash fixes
- BR libpurple >= 2.4.0
- Split into purple-sipe and pidgin-sipe
- Other spec fixes to match upstream's spec file

* Tue Feb 16 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.8.1-1
- Upstream 1.8.1 (crash fixes)

* Mon Feb 08 2010 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.8.0-1
- Upstream 1.8.0 (new features)
- Exchange Calendar integration
- New and updated translations
- Bugfixes

* Mon Nov 23 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.7.1-1
- Upstream 1.7.1 (bugfixes)

* Tue Nov 03 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.7.0-1
- Upstream 1.7.0

* Mon Sep 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6.3-1
- Upstream 1.6.3

* Tue Sep 08 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6.2-1
- Upstream 1.6.2
- Drop obsoleted ppc fix patch

* Fri Jul 31 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6.0-2
- Add BR: gettext to build on EPEL

* Thu Jul 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6.0-2
- Another attempt at ppc build fix (patch from Stefan Becker)

* Tue Jul 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6.0-1
- Upstream 1.6.0
- Build on ppc, but pass --enable-quality-check=no to configure

* Thu Jul 16 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.5.0-2
- Build --with-krb5

* Tue Jun 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.5.0-1
- Initial packaging.

