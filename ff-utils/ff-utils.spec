Name:		ff-utils
Version:	2.4.21
Release:	4%{?dist}
Summary:	Utilities to test force feedback of input device

Group:		Amusements/Games
License:	GPLv2+
URL:		http://sourceforge.net/apps/mediawiki/libff/
Source0:	http://downloads.sourceforge.net/libff/%{name}.tar.bz2

#Add 64-bit port and kernel 2.6.22 compatibility
#http://sourceforge.net/tracker/download.php?group_id=44724&atid=440671&file_id=292511&aid=2098907
Patch0:		ff-utils-2.6.22-64bitPort.patch.tgz

#Add manpages fromt the Debian joystick package
#http://ftp.de.debian.org/debian/pool/main/j/joystick/joystick_20051019-12.debian.tar.gz
Patch1:		ff-utils-manpages.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	SDL-devel

%description
Set of utilities provides possibility to test force feedback of
input devices like joysticks, game-pads or game-wheels in Linux.


%prep
%setup -q -n %{name}
%patch0 -p 1 -b .64bit
%patch1 -p 1
make clean


%build
make -e CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags} ffcfstress ffmvforce ffset fftest
gzip *.1


%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -m 0755 ffcfstress ffmvforce ffset fftest %{buildroot}%{_bindir}/
install -d %{buildroot}%{_mandir}/man1
install -m 0644 *.1.gz %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
#There are no doc files in the package
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Mon Apr 11 2011 Michal Ambroz <rebus at, seznam.cz> 2.4.21-4
- apply patch as suggested by Didier Moens in package review
- add manpages from Debian joystick package

* Sun Apr 18 2010 Michal Ambroz <rebus at, seznam.cz> 2.4.21-3
- cleanup directory macros

* Sun Jan 24 2010 Michal Ambroz <rebus at, seznam.cz> 2.4.21-2
- added build requirement for the SDL-devel

* Sat Jan 16 2010 Michal Ambroz <rebus at, seznam.cz> 2.4.21-1
- Initial SPEC for Fedora 12
