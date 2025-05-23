%define debug_package %{nil}

Summary:	A Windows Registry data extraction and correlation tool

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		regripper
Version:	30000000
Release:	2%{?dist}

License: GPL

Group: Applications/Forensics Tools

Source1:	rrv3.0.zip
Patch1:		%{name}-%{version}-patch-001
Source2:	regripper-3.0.pdf
Requires:	perl perl-Parse-Win32Registry
%if 0%{?rhel} > 0
Requires:	perl-DateTime-Format-WindowsFileTime
%endif
BuildArch:	noarch
URL:		https://github.com/keydet89/RegRipper3.0
BuildRoot:      %{_tmppath}/rpm-root-%{name}-%{version}
BuildRequires:	dos2unix
Requires:	regripper-plugins >= 20200528
Provides:	perl(shellitems.pl)

%description
RegRipper is a Windows Registry data extraction and correlation
tool. RegRipper uses plugins (similar to Nessus) to access specific
Registry hive files in order to access and extract specific keys, values,
and data, and does so by bypassing the Win32API.

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
unzip -o %{SOURCE1}
dos2unix < rip.pl > X; mv X rip.pl
%patch1 -p1
cp %{SOURCE2} %{name}.pdf

%build

%install
cd %{name}-%{version}
%__install -d %{buildroot}%{_bindir}
%__install rip.pl %{buildroot}%{_bindir}
ln -s rip.pl %{buildroot}%{_bindir}/regripper
%__install -d %{buildroot}%{_docdir}/%{name}
%__install -m 0644 %{name}.pdf %{buildroot}%{_docdir}/%{name}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%attr(555,root,root)	%{_bindir}/*
%attr(444,root,root)	%{_docdir}/%{name}/*

%changelog
* Wed Jul 15 2020 Lawrence R. Rogers <lrr@cert.org> 30000000-2
* Release 30000000-2
	Fix the plugin path patch.

* Thu May 28 2020 Lawrence R. Rogers <lrr@cert.org> 30000000-1
* Release 30000000-1
	This is RegRipper 3.0.

* Mon Aug 26 2013 Lawrence R. Rogers <lrr@cert.org> 28000000-4
* Release 28000000-4
	New auto_rip.pl (2012-08-26 version)
		Fixes some issues running on Linux
		There is a new switch (-r) to save the output reports to a folder of your choice

* Thu May 23 2013 Lawrence R. Rogers <lrr@cert.org> 28000000-3
* Release 28000000-3
	Fixed help comments and path for rip.pl.

* Wed May 22 2013 Lawrence R. Rogers <lrr@cert.org> 28000000-2
* Release 28000000-2
	Added auto_rip.pl/auto_rip

* Thu Apr 25 2013 Lawrence R. Rogers <lrr@cert.org> 28000000-1
* Release 28000000-1
	Regripper version 2.8
		Includes an additional function/subroutine that is available to the plugins: alertMsg().

* Mon Oct 1 2012 Lawrence R. Rogers <lrr@cert.org> 25000000-2
* Release 25000000-2
	Now correctly finds the plugins directory using perl's @INC array.

* Tue Jun 26 2012 Lawrence R. Rogers <lrr@cert.org> 25000000-1
* Release 25000000-1
	Regripper plugins are now a separate package.

* Tue Jun 12 2012 Lawrence R. Rogers <lrr@cert.org> 20120612-1
* Release 20120612-1
    Now uses regripper plugins 20120528
	+ NEW PLUGIN by Jason Hale: "typedurlstime.pl" that parses and correlates the TypedURLs and TypedURLsTime subkeys
	+ NEW PLUGIN by Jason Hale: "typedurlstime_tln.pl" that parses and correlates the TypedURLs and TypedURLsTime subkeys (output in TLN format)

* Mon May 28 2012 Lawrence R. Rogers <lrr@cert.org> 20120528-2
* Release 20120528-2
	Removes old plugins before installing the lastest ones.

* Mon May 28 2012 Lawrence R. Rogers <lrr@cert.org> 20120528-1
* Release 20120528-1
    Now uses regripper plugins 20120528
	+ NEW PLUGIN by Francesco Picasso: “internet_explorer_cu.pl” that parses the Internet Explorer info from NTUSER.DAT registry
	+ NEW PLUGIN by Francesco Picasso: “internet_settings_cu.pl” that parses the Internet Settings info from NTUSER.DAT registry
	+ REMOVED plugin “ie_main.pl“, since superseded by “internet_explorer_cu.pl”
	+ REMOVED plugin “iexplore.pl“, since superseded by “internet_explorer_cu.pl”
	+ FIXED plugin “timezone.pl“, see  Issue14  and see source code comments
	+ FIXED plugin “userassist2.pl“, now it parses Windows7 entries, see source code comments
	+ ADDED profiles with every plugin listed in alphabetical order: all-all (3), ntuser-all (98), sam-all (1), security-all (3), software-all (56), system-all (46)
	+ NOTE RegRipperPlugins now counts 207 plugins
	+ KNOWN ISSUES: comdlg32 does not parse Vista/7 subkeys (Issue 15)

* Fri Feb 24 2012 Lawrence R. Rogers <lrr@cert.org> 20120224-1
* Release 20120224-1
    Now uses regripper plugins 20120224
	+ NEW PLUGIN by Adrian Leong: "ccleaner.pl" (gets CCleaner User's Settings from NTUSER.DAT)

* Fri Feb 10 2012 Lawrence R. Rogers <lrr@cert.org> 20120210-1
* Release 20120210-1
    Now uses regripper plugins 20120210
	+ NEW PLUGIN by Brad Reninger: "EMDMgt.pl" (Parses the EMDMgt registry key located in the SOFTWARE Hive.
	  This registry key identifies the volume serial number of USB devices.)

* Tue Jan 7 2012 Lawrence R. Rogers <lrr@cert.org> 20120206-1
* Release 20120206-1
    Now uses regripper plugins 201200206
	+ NEW PLUGIN by Corey Harrell: spp_clients.pl that lists volumes currently monitored by
	  the Volume Shadow Copy Service
	+ NEW PLUGIN by Corey Harrell: filesnottosnapshot.pl that extracts from SYSTEM registry files
	  and folders not backed up in Volume Shadow Copies
	
* Tue Dec 6 2011 Lawrence R. Rogers <lrr@cert.org> 20111118-1
* Release 20111118-1
    Now uses regripper plugins 20111118
	* CHANGED winlivemsn.pl, now it's able to parse 'SoundEvents' keys too
	* BUGFIX winlivemail.pl (wrong cut&paste file in previous archive)
	------------------------------------------------------
	From 17 november 2011 release:
	+ NEW PLUGIN winlivemail.pl (Windows Live Mail parser)
	+ NEW PLUGIN winlivemsn.pl (Windows Live Messenger parser)
	* CHANGED networkcards.pl to include printout of 'ServiceName' to correlate info coming from otherplugins
	- REMOVED wlm_cu.pl plugin, since it's substituted by winlinemsn.pl
	- REMOVED TODO.txt, unuseful (let's use the RegRipperPlugins Google Code site)

* Thu Oct 20 2011 Lawrence R. Rogers <lrr@cert.org> 20111014-1
* Release 20111014-1
    Now uses regripper plugins 20111014
	+ Added (NEW PLUGIN) Corey Harrell "userinfo.pl" (Microsoft Office)
	+ Added references to officedocs2010.pl (provided by Cameron Howell).
	- Removed the use of "DateTime::Format::WindowsFileTime" from officedocs2010.pl (ref: Issue 1).
	* PURGED OLD/REDUNDANT PLUGINS (ref: Issue 12): the process of plugins eliminating and renaming was based to the fact
	  that the new plugins generated the same output of the old one (eventually with enhancement). *PLEASE UPDATE YOUR PLUGIN LIST
	  FILES* (otherwise you will get error when trying to use the renamed/delete plugins). As following:
	- Eliminated old "comdlg32.pl" and renamed the plugin "comdlg32a.pl" to "comdlg32.pl". Updated version number to be
	   able to compare and track down changes.
	- Eliminated old "mountdev.pl" and renamed the plugin "mountdev2.pl" to "mountdev.pl". Updated version number to be able
	  to compare and track down changes: current version is 20110901.
	- Eliminated "port_dev.pl": the current plugin is "removedev.pl", as renamed by its author H.Carvey.
	- Eliminated old "timezone.pl" and renamed the plugin "timezone2.pl" to "timezone.pl". Updated version number to be able
	  to compare and track down changes: current version is 20110901.
	- Eliminated old "samparse.pl" and renamed this plugin "sameparse2.pl" to "samparse.pl". Updated version number to
	  be able to compare and track down changes: current version is 20110901

* Wed Aug 30 2011 Lawrence R. Rogers <lrr@cert.org> 20110830-1
* Release 20110830-1
	Added banner (rptMsg) to all plugins
	Restored identation of some "flat" plugins
	Restored a common template for the plugins' descriptions
	Purged "yahoo.pl" plugin

* Tue Aug 2 2011 Lawrence R. Rogers <lrr@cert.org> 20110518-2
* Release 20110518-2
	Now correctly finds the plugin directory.

* Tue Aug 2 2011 Lawrence R. Rogers <lrr@cert.org> 20110518-1
* Release 20110518-1
	This version uses the plugins as of 20110518
