%define debug_package %{nil}

Summary:	Plugins for regripper

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		regripper-plugins
Version:	20200528
Release:	1%{?dist}

License: GPL

Group:		Applications/Forensics Tools

Source1:	%{name}-%{version}.zip
Requires:	perl perl-Parse-Win32Registry
BuildArch:	noarch
URL:		https://github.com/keydet89/RegRipper3.0/tree/master/plugins
BuildRoot:      %{_tmppath}/rpm-root-%{name}-%{version}
BuildRequires:	dos2unix

%description
RegRipper is a Windows Registry data extraction and correlation
tool. RegRipper uses plugins (similar to Nessus) to access specific
Registry hive files in order to access and extract specific keys, values,
and data, and does so by bypassing the Win32API.

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}/plugins
cd %{name}-%{version}/plugins
unzip -o %{SOURCE1}
for p in *; do dos2unix < $p > X; mv X $p; done

%build

%install
cd %{name}-%{version}
%__install -d %{buildroot}%{perl_vendorlib}/regripper
%__cp -r plugins %{buildroot}%{perl_vendorlib}/regripper

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%attr(555,bin,bin)	%{perl_vendorlib}/regripper/*

%changelog
* Thu May 28 2020 Lawrence R. Rogers <lrr@cert.org> 20200528-1
* Release 20200528-1
	Plugins from 20200528

* Wed Oct 17 2018 Lawrence R. Rogers <lrr@cert.org> 20181017-1
* Release 20181017-1
	Plugins from 20181017

* Wed Aug  9 2017 Lawrence R. Rogers <lrr@cert.org> 20170809-1
* Release 20170809-1
	Plugins from 20170809

* Thu Dec 17 2015 Lawrence R. Rogers <lrr@cert.org> 20151216-2
* Release 20151216-2
	Added missing files: all ntuser sam security software system usrclass

* Wed Dec 16 2015 Lawrence R. Rogers <lrr@cert.org> 20151216-1
* Release 20151216-1
	Plugins from 20151216

* Mon Apr 29 2013 Lawrence R. Rogers <lrr@cert.org> 20130429-1
* Release 20130429-1
	Includes the following changes
		20130429
			created winlogon_tln.pl, applets_tln.pl
			added alertMsg() func. to:
				brisv.pl, inprocserver.pl, inprocserver_u.pl, iejava.pl, spp_clients.pl
			retired scanwithav.pl (func. included in attachmgr.pl)
			retired taskman.pl (func. included in winlogon.pl)
			retired vista_wireless.pl (func. in networklist.pl)
		20130425
			RegRipper and rip updated to v2.8; added alertMsg() capability
			retired userinit.pl (functionality included in winlogon.pl)
			created new plugins
				srun_tln.pl, urun_tln.pl,cmdproc_tln.pl
				-cmd_shell_tln.pl,muicache_tln.pl
			added alertMsg() functionality to rip.pl, rr.pl, and plugins
				appcompatcache.pl, appcompatcache_tln.pl
				appinitdlls.pl
				soft_run.pl, user_run.pl
				imagefile.pl
				winlogon.pl, winlogon_u.pl
				muicache.pl (look for values with "Ttemp" paths)
				attachmgr.pl (look for values per KB 883260)
				virut.pl
				cmdproc.pl, cmd_shell.pl
		20130411
			retired specaccts.pl & notify.pl; incorporated functionality into winlogon.pl
		20130410
			retired taskman.pl; merged into winlogon.pl
			updated winlogon.pl (Wow6432Node support, etc.)
			updated winlogon_u.pl (Wow6432Node support)
			updated shellexec.pl, imagefile.pl, installedcomp.pl (Wow6432Node support)
		20130409
			added drivers32.pl (C. Harrell) to the archive
		20130408
			updated bho.pl to support Wow6432Node
		20130405
			updated cmd_shell.pl to include Clients subkey in the Software hive
			created cmd_shell_u.pl
			fixed issue with rip.exe syntax info containing 'rr'
			fixed banner in findexes.pl
	+ NOTE RegRipperPluginsPackage (RRPP) counts 285 plugins

* Thu Apr 04 2013 Lawrence R. Rogers <lrr@cert.org> 20130404-1
* Release 20130404
	+ NOTE: these are the packager's comments on what is new in this release, not the authors.

	+ NEW PLUGIN	attachmgr.pl		The Windows Attachment Manager manages how attachments are handled,
						and settings are on a per-user basis.  Malware has been shown to access
						these settings and make modifications.
	+ NEW PLUGIN	javasoft.pl		Gets contents of JavaSoft/UseJava2IExplorer value
	+ NEW PLUGIN	lsa_packages.pl		Lists various *Packages key contents beneath LSA key
	+ NEW PLUGIN	olsearch.pl		Gets contents of user's OutLook Searches
	+ NEW PLUGIN	outlook2.pl		Gets MAPI (Outlook) settings *BETA*
	+ NEW PLUGIN	photos.pl		Read data on images opened via Win8 Photos app
	+ NEW PLUGIN	scanwithav.pl		Checks ScanWithAV value in Software hive, per KB 883260
	+ NEW PLUGIN	uac.pl			Get User Account Control (UAC) Values from HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System

	+ UPDATE	appinitdlls.pl		updated to address 64-bit systems
	+ UPDATE	ares.pl			updated based on data provided by J. Weg
	+ UPDATE	ie_settings.pl		added "AutoConfigURL" value info
	+ UPDATE	inprocserver.pl		fixed retrieving LW time from correct key
	+ UPDATE	landesk.pl		added Wow6432Node path
	+ UPDATE	sevenzip.pl		minor updates added
	+ UPDATE	soft_run.pl		updated to include Policies keys; added additional keys
	+ UPDATE	ssh_host_keys.pl	Added rptMsg for key not found errors by Corey Harrell
	+ UPDATE	termserv.pl		updated with autostart locations
	+ UPDATE	user_run.pl		added additional keys; updated to include Policies keys;
						updated to include additional keys; updated to include 64-bit, additional keys/values
	+ UPDATE	winlogon_u		updated with ThreatExpert info
	+ UPDATE	winscp_sessions.pl	Added rptMsg for key not found errors by Corey Harrell

	+ NOTE RegRipperPluginsPackage (RRPP) now counts 236 plugins

* Mon Feb 18 2013 Lawrence R. Rogers <lrr@cert.org> 20130218-1
* Release 20130218
	+ NEW PLUGIN by Corey Harrell: "uac.pl" that gets UAC configuration values (SOFTWARE)
	+ UPDATE by Harlan Carvey to "comdlg32.pl", many updates (NTUSER)
	+ NOTE profile software-all was updated
	+ NOTE profiles '-all' DO NOT contain plugins TLN versions: you must create your own profiles or use them directly
	+ NOTE RegRipperPluginsPackage (RRPP) counts 236 plugins

* Mon Oct 1 2012 Lawrence R. Rogers <lrr@cert.org> 20120926-1
* Release 20120926
	Installed 20120926 version of the plugins. Here are the changes:
	+ NEW PLUGIN by Harlan Carvey: "appcertdlls.pl" that gets entries from AppCertDlls key (SYSTEM)
	+ NEW PLUGIN by Harlan Carvey: "appcompatcache.pl" that parses files from the Shim Cache (SYSTEM)
	+ NEW PLUGIN by Harlan Carvey: "appcompatcache_tln.pl" that parses files from the Shim Cache, TLN output (SYSTEM)
	+ NEW PLUGIN by Harlan Carvey: "applets_tln.pl" that gets the content of Applets key, TLN output (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "appspecific.pl" that gets contents of user's Intellipoint\AppSpecific subkeys (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "ares.pl" that gets contents of user's Software\Ares key (NTUSER)
	+ NEW PLUGIN by Corey Harrell: "backuprestore.pl" that gets FilesNotToSnapshot, KeysNotToRestore, FilesNotToBackup (SYSTEM)
	+ NEW PLUGIN by Harlan Carvey: "compatassist.pl" that checks user's Compatibility Assistant\Persisted values (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "direct.pl" that searches Direct keys for MostRecentApplication subkeys (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "direct_tln.pl" that searches Direct keys for MostRecentApplication subkeys, TLN output (SOFTWARE)
	+ NEW PLUGIN by Corey Harrell: "disablesr.pl" that gets the on/off value for System Restore (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "installer.pl" that determines products install information (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "javafx.pl" that gets contents of user's JavaFX key (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "legacy_tln.pl" that lists LEGACY entries in Enum\Root key, TLN output (SYSTEM)
	+ NEW PLUGIN by Harlan Carvey: "networklist_tln.pl" that collects network info from NetworkList key, TLN output (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "osversion.pl" that checks for OSVersion value, malware related (NTUSER)
	+ NEW PLUGIN by Corey Harrell: "prefetch.pl" that gets the Prefetch Parameters (SYSTEM)
	+ NEW PLUGIN by Harlan Carvey: "runmru_tln.pl" that gets contents of user's RunMRU key, TLN output (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "shellbags.pl" that gets contents of users's Shell/BagMRU keys, Windows7 (USRCLASS)
	+ NEW PLUGIN by Harlan Carvey: "sysinternals.pl" that checks for SysInternals apps keys (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "sysinternals_tln.pl" that checks for SysInternals apps keys, TLN output (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "tracing.pl" that gets list of apps that can be traced (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "tracing_tln.pl" that gets list of apps that can be traced, TLN output (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "trustrecords.pl" that gets user's Office 2010 TrustRecords values (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "trustrecords_tln.pl" that gets user's Office 2010 TrustRecords values, TLN output (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "tsclient_tln.pl" that gets contents of user's Terminal Server Client key, TLN output (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "typedpaths_tln.pl" that gets contents of user's typedpaths key, TLN output (NTUSER)
	+ NEW PLUGIN by Harlan Carvey: "userassist_tln.pl" that displays contents of UserAssist subkeys, TLN output (NTUSER)
	+ NEW PLUGIN by Mari DeGrazia: "winbackup.pl" that gets Windows Backup settings (SOFTWARE)
	+ NEW PLUGIN by Harlan Carvey: "wpdbusenum.pl" that gets WpdBusEnumRoot subkey info (SYSTEM)

	+ UPDATE by Harlan Carvey to "legacy.pl", added analysis tip (SYSTEM)
	+ UPDATE by Harlan Carvey to "muicache.pl", the plugin works both on NTUSER and/or USRCLASS hives (NTUSER,USRCLASS)
	+ UPDATE by Harlan Carvey to "networklist.pl", added NameType value reporting (SOFTWARE)
	+ UPDATE by Harlan Carvey to "soft_run.pl", added support to newer OS and 64 bits (SOFTWARE)
	+ UPDATE by Harlan Carvey to "tsclient.pl", added parsing of Servers key (NTUSER)
	+ UPDATE by Harlan Carvey to "userassist.pl" (NTUSER)

	+ REMOVED TEMPORARILY plugin "typedurlstime.pl", postponed on next packages
	+ REMOVED TEMPORARILY plugin "typedurlstime_tln.pl", postponed on next packages

	+ REMOVED plugin "bagtest.pl", deprecated
	+ REMOVED plugin "bagtest2.pl", deprecated
	+ REMOVED plugin "crashcontrol.pl", too similar to "crashdump.pl"
	+ REMOVED plugin "filesnottosnapshot.pl", superseded by "backuprestore.pl"
	+ REMOVED plugin "pstools.pl", superseded by the more general "sysinternals.pl" plugin
	+ REMOVED plugin "userassist2.pl", deprecated since "userassist.pl" was updated
	+ REMOVED plugin "vista_comdlg32.pl", deprecated since "comdlg32.pl" was updated
	+ REMOVED plugin "win7_ua.pl", Windows7-RC and Vigenerè encryption are obsolete

	+ NOTE added profile "usrclass-all" for USRCLASS.DAT hive
q	+ NOTE profiles all-all, ntuser-all, sam-all, security-all, software-all, system-all, usrclass-all were updated
	+ NOTE profiles '-all' DO NOT contain plugins TLN versions: you must create your own profiles or use them directly
	+ NOTE source code repository was switched to GIT and it was aligned to the current release
	+ NOTE RegRipperPluginsPackage (RRPP) now counts 236 plugins

* Mon Oct 1 2012 Lawrence R. Rogers <lrr@cert.org> 20120812-2
* Release 20120812-2
	Moved the plugin directory from plugins/regripperplugins_%{version} to plugins.

* Sun Aug 12 2012 Lawrence R. Rogers <lrr@cert.org> 20120812-1
* Release 20120812-1
    Now uses regripper plugins 20120812.
    RegRipperPlugins now counts 215 plugins

    Changes from the previous version:
	+ NEW PLUGIN by Hal Pomeranz: "ssh_host_keys.pl" that extracts stored Putty and WinSCP host keys from NTUSER hive
	+ NEW PLUGIN by Hal Pomeranz: "winscp_sessions.pl" that extracts WinSCP saved session data from NTUSER hive (with password decoding)
	+ NOTE profiles all-all, ntuser-all, sam-all, security-all, software-all and system-all were updated
	+ NOTE source code repository was aligned to current release
	+ NEW PLUGIN by John Lukach: "pstools.pl" that displays the content for PsTools EULA Agreements
	+ NEW PLUGIN by K. Johnson (with Harlan Carvey updates): "filehistory.pl" that parses NTUSER FileHistory Registry keys from Windows 8
	+ NEW PLUGIN by Elizabeth Schweinsberg: "user_runplus.pl" that gets contents of the Run, RunOnce, and RunServices keys from NTUSER hive
	+ NEW PLUGIN by Elizabeth Schweinsberg: "soft_runplus.pl" that gets contents of the Run, RunOnce, and RunServices keys from SOFTWARE hive
	+ NEW PLUGIN by Elizabeth Schweinsberg: "svc_plus.pl" that gets services, displaied in short format, from SYSTEM hive

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

* Sat Jan 7 2012 Lawrence R. Rogers <lrr@cert.org> 20120206-1
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

* Tue Aug 30 2011 Lawrence R. Rogers <lrr@cert.org> 20110830-1
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
