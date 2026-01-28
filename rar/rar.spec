#
# Specfile for rar
#

# norootforbuild

%define debug_package %{nil}

Summary:        Compression and decompression program rar
Summary(de):    Kompressions- und Dekompressionsprogramm rar
Name:           rar
Version:        7.12
%global         rarversion 712
Release:        1%{?dist}
License:        see license.txt
Group:          Productivity/Archiving/Compression
URL:            http://www.rarsoft.com

Source0:        https://www.rarlab.com/rar/rarlinux-x64-%{rarversion}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  x86_64

%description
Compression and decompression program.
includes version 2.7.1 and %{version}

%description -l de
Kompressions- und Dekompressionsprogramm.
Enthält Version 2.7.1 und %{version}

%prep

%setup -q -c -T
tar xfz %{SOURCE0}

%build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
cd rar
mkdir %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 755 rar %{buildroot}%{_bindir}/
%{__mkdir_p} %{buildroot}%{_libdir}
%{__mkdir_p} %{buildroot}/etc
chmod 644 *
# cd ../oldrar/rar
# %{__install} -m 755 rar %{buildroot}%{_bindir}/rar2
#%{__install} -m 755 unrar %{buildroot}%{_bindir}/unrar2

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc rar/*.txt rar/*.htm
%{_bindir}/*

%changelog
* Tue Aug  8 2017 Larence R. Rogers <lrr@cert,org> - 5.4.0-1
* Release 5.4.0-1
	See the list of chages here: http://www.rarlab.com/rarnew.htm

* Wed Nov 18 2015 Larence R. Rogers <lrr@cert,org> - 5.3.0-1
* Release 5.3.0-1
  1. Directory wildcards are allowed in RAR command line in file names to
      archive. For example:

      rar a backup c:\backup\2015*\*

      Recursion is enabled automatically for such directory wildcards
      even if -r switch is not specified.

   2. New 'R' object for -sc switch defines encoding of console
      RAR messages sent to redirected files and pipes. For example:

      rar lb -scur data > list.txt

      will produce Unicode list.txt with archived file names.

   3. Console RAR "l" and "v" commands display file time in YYYY-MM-DD
      format.

   4. "Test" command also verifies contents of NTFS alternate data streams
      in RAR 3.x - 5.x archives. Previously their contents was checked
      only during extraction command.

   5. Bugs fixed:

      a) console RAR crashed instead of displaying an overwrite prompt
         when attempting to add files to already existing volumes;

      b) console RAR "lt" command did not display seconds in file timestamp.

* Fri Mar 19 2010 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.9.3-0.pm.1
- update to 3.9.3
* Fri Feb 19 2010 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.9.2-0.pm.1
- update to 3.9.2
* Tue Dec 15 2009 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.9.1-0.pm.1
- update to 3.9.1
* Fri Aug 21 2009 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.9.0-0.pm.0
- update to 3.9.0
* Thu Oct 02 2007 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.8.0-0.pm.1
- update to 3.8.0 now also with x86_64 version
* Fri Sep 21 2007 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.7.1-0.pm.0
- update to 3.7.1
* Thu May 29 2007 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.7.0-0.pm.0
- update to 3.7.0
* Thu Aug 17 2006 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.6.0-0.pm.0
- update to 3.6.0
* Sun Nov 06 2005 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.5.1-0.pm.1
- added a lot of usefull changes from Andreas Hanke
- some cleanups in the spec-file
* Tue Oct 11 2005 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.5.1-0.pm.0
- update to 3.5.1
* Thu Aug 09 2005 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.5.0-0.pm.0
- update to 3.5.0
* Thu Sep 16 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.4.0-0.pm.0
- update to 3.4.0
* Mon Jan 26 2004 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.3.0-0.pm.0
- update to 3.3.0
* Sun Sep 07 2003 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.2.0-0.pm.1
- now included 3.2.0 and 2.7.1
* Sat Feb 22 2003 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 2.7.1-0.pm.0
- downgrade to 2.7.1
* Wed Feb 19 2003 Manfred Tremmel <Manfred.Tremmel@iiv.de> - 3.2.0-0.pm.0
- first release
