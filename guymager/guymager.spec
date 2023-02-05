%define debug_package %{nil}

Summary:	Imager for forensic media acquisition

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		guymager
%if 0%{?centos} == 6
Version:	0.8.8
%else
Version:	0.8.13
%endif
Release:	1%{?dist}
URL:		http://guymager.sourceforge.net/

License:	GPL

Group:		Applications/Forensics Tools

# Get the source with svn co https://svn.code.sf.net/p/guymager/code/tags/guymager-%{vesion} guymager-%{vesion}

Source0:	%{name}-%{version}.tar.gz
Patch1:		%{name}-%{version}-patch-001
%if 0%{?rhel} == 6
Patch2:		%{name}-%{version}-patch-002
%endif
BuildRoot:	%{buildroot}
BuildRequires:  qt5-qtbase-devel
BuildRequires:	libguytools parted-devel
%if 0%{?fedora} > 0
%if 0%{?fedora} < 36
BuildRequires:	openssl-static
%else
BuildRequires:  openssl-devel
%endif
%endif
%if 0%{?rhel} == 6
BuildRequires:	openssl-static
%endif
%if 0%{?rhel} == 5
BuildRequires:	openssl-devel
%endif
BuildRequires:	libewf-devel
Requires:	parted libewf
%if 0%{?rhel} != 5
%if 0%{?rhel} == 7 || 0%{?rhel} == 8 || 0%{?rhel} == 9
Requires:	udisks2
%else
Requires:	udisks
%endif
%endif
BuildRequires:	libudev-devel
BuildRequires:	libbfio-devel
BuildRequires:	zlib-devel
BuildRequires:	afflib-devel
BuildRequires:	gcc-c++

%description
guymager is an imager for forensic media acquisition. Its main features are:

    * Easy user interface in different languages
    * Runs under Linux
    * Multi-threaded design, multi-threaded data compression
    * Makes full usage of multi-processor machines
    * Generates flat (dd) and EWF (E01) images


%prep
%setup -n %{name}-%{version}
%patch1 -p1
%if 0%{?rhel} == 6
%patch2 -p1
%endif

%build
%if 0%{?fedora} > 0
	qmake-qt5  guymager.pro
%endif
%if 0%{?rhel} > 0
        %{_libdir}/qt5/bin/qmake guymager.pro
%endif
%{__make}
cd manuals; sh rebuild.sh

%install
rm -rf %{buildroot}
%__install -d %{buildroot}%{_bindir}
%__install -d %{buildroot}%{_sysconfdir}/%{name}
%__install -d  %{buildroot}%{_mandir}/man1
%__install -m 755 %{name} %{buildroot}%{_bindir}
%__install -m 644 %{name}.cfg %{buildroot}%{_sysconfdir}/%{name}
sed --in-place 's/\\$/ /' %{buildroot}%{_sysconfdir}/%{name}/%{name}.cfg
%if 0%{?rhel} == 5
%endif
%__install -m 644 manuals/%{name}.1 %{buildroot}%{_mandir}/man1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%attr(755, root, root)		%{_bindir}/*
%attr(644, root, root)		%{_sysconfdir}/%{name}/*
%attr(644, root, root)		%{_mandir}/man1/*

%changelog
%if 0%{?centos} != 6
* Thu Aug  5 2021 Lawrence R. Rogers <lrr@cert.org> 0.8.13-1
* Release 0.8.13-1
	guymager-beta (0.8.13-1) unstable; urgency=low
	 * Querying CID data for SD memory cards (DeviceInfoCommands in guymager.cfg)
	 * String of OS version in corresponding EWF field now corresponds to the
	   output of "uname -r" in order to circumvent Encase bugs.

* Mon May  4 2020 Lawrence R. Rogers <lrr@cert.org> 0.8.12-1
* Release 0.8.12-1
	guymager-beta (0.8.12-1) unstable; urgency=low
	 * Avoiding error "flexible array member ... ~not at end of ..." in newer gcc versions.
         * Removed bug where acquisition state never changed from "Launch" to "Acquire" for special devices

* Wed Jun 26 2019 Lawrence R. Rogers <lrr@cert.org> 0.8.11-1
* Release 0.8.11-1
	guymager-beta (0.8.11-1) unstable; urgency=low
	   * Added configuration check for invalid EwfFormat/EwfCompression setting
	 -- Guy Voncken <develop@faert.net>  Wed, 26 Jun 2019 11:00:00 +0200

	guymager-beta (0.8.10-1) unstable; urgency=low
	   * Removed a bug where verification failed if EwfFormat set to something
	     different than Guymager and segmentation beyond .EZZ
	 -- Guy Voncken <develop@faert.net>  Mon, 27 May 2019 16:00:00 +0100

	guymager-beta (0.8.9-1) unstable; urgency=low
	   * New cfg parameter DeleteAbortedImageFiles
	   * Removed a bug where a AEWF file open error would escalate to program exit.
	   * Checking and detecting possible devices changes upon acquisition start.
	   * Total acquisition speed displayed in info field
	   * Cleanup for C++14
	 -- Guy Voncken <develop@faert.net>  Thu, 30 Aug 2018 16:00:00 +0100
%endif

* Thu Nov  1 2018 Lawrence R. Rogers <lrr@cert.org> 0.8.8-2
* Release 0.8.8-2
	Patch for GCC 8

* Wed Jan 24 2018 Lawrence R. Rogers <lrr@cert.org> 0.8.8-1
* Release 0.8.8-1
	guymager-beta (0.8.8-1) unstable; urgency=low
	   * Using pkexec instead of gksudo
	   * New compile option ENABLE_LIBEWF

* Tue Jan  16 2018 Lawrence R. Rogers <lrr@cert.org> 0.8.7-2
* Release 0.8.7-2
	Rebuilt with libguytools-2.0.5.

* Fri Sep 22 2017 Lawrence R. Rogers <lrr@cert.org> 0.8.7-1
* Release 0.8.7-1
	guymager-beta (0.8.7-1) unstable; urgency=low
	   * Typing errors corrected

	guymager-beta (0.8.6-1) unstable; urgency=low
	   * Upon disconnection of device, do not pause verification if it is done
	     on the image only (pausing still for source verifications).
	   * New cfg parameter AdditionalStateInfoName
	   * System signal HUP triggers device rescanning
	   * Special tokens %UserField% and %AddStateInfo% added

	guymager-beta (0.8.5-1) unstable; urgency=low
	   * New cfg parameters BadSectorLogThreshold and BadSectorLogModulo.

* Thu Feb  2 2017 Lawrence R. Rogers <lrr@cert.org> 0.8.4-1
* Release 0.8.4-1
	guymager-beta (0.8.4-1) unstable; urgency=low
	   * Removed bug that occurred if remaining time was longer than 99 hours
	   * Adapted to gcc7

	guymager-beta (0.8.3-1) unstable; urgency=low
	   * Corrected bug where Guymager not always recognised if duplicate image or
	     info file was the same as first one.
	   * In the duplicate acquisition dialog mark the device selected in the first
	     acquisition dialog and make it unselectable.
	   * New features in acquisition dialog: Allow relative paths in filenames,
	     allow direct editing of directory fields. See new configuration parameters
	     DirectoryFieldEditing, AllowPathInFilename and ConfirmDirectoryCreation.
	   * Forbid overwriting image / info files of other acquisitions (up until now,
	     only an warning was shown that could have been ignored by the user).

	guymager-beta (0.8.2-1) unstable; urgency=low
	   * Support for SHA1 checksum in EWF images (for AEWF and LIBEWF)
	   * Corrected bug where directory button in dlgacquire would be drawn
	     half underneath entry field for certain configuration settings.
	   * Corrected bug where %SizeHumanNoSep% behaved the same as %SizeHuman%

* Tue Mar  3 2015 Lawrence R. Rogers <lrr@cert.org> 0.8.1-1
* Release 0.8.1-1
	* New DeviceScanMethod libudev
	* Adapted to Qt 5 API
	* For computers with non standard mouse: Double click open context menu
	* New configuration parameter AvoidCifsProblems
	* Show version number in main window title bar
	* Debug CIFS flcose problem
	* Added EWFX support from libewf

* Tue Mar  3 2015 Lawrence R. Rogers <lrr@cert.org> 0.7.4-2
* Release 0.7.4-2
	Rebuilt with libguytools-2.0.3

* Thu Oct 30 2014 Lawrence R. Rogers <lrr@cert.org> 0.7.4-1
* Release 0.7.4-1
  * Added output for hostname, domainname and system to info file
  * New cfg param InfoFieldsForDd
  * Corrected bug: DisconnectTimeout only must be active if LimitJobs is active
  * libewf version check changed, all versions >= 20130416 are accepted
  * New cfg parameter InfoFieldsForDd

* Mon May 19 2014 Lawrence R. Rogers <lrr@cert.org> 0.7.3-2
* Release 0.7.3-2
	Use latest version of libewf
	Installed workaround where \ at the end of a line in the config file caused errors

* Fri Jan 17 2014 Lawrence R. Rogers <lrr@cert.org> 0.7.3-1
* Release 0.7.3-1

* Fri Mar 15 2013 Lawrence R. Rogers <lrr@cert.org> 0.7.1-1
* Release 0.7.1-1
  * Duplicate image creation
  * New RunStats module
  * New job queue mechanism
  * New userfield
  * New configuration table for main Guymager table
  * New font configuration
  * New cfg table HiddenDevices
  * New configuration parameter CommandAcquisitionEnd
  * Writing hidden area info into info file
  * Gray out rescan button when scan is running
  * In order to avoid the "contagious error", DirectIO is switched on in fallback mode.
  * Removed race condition where write thread would write hash into image before it has been calculated by hash thread.
  * SHA-1 support added

* Thu Dec 27 2012 Lawrence R. Rogers <lrr@cert.org> 0.6.13-1
* Release 0.6.13-1
  * Package dependency to udisks added (for recent Ubuntu)
  * libparted search extended to subdirs
  * Added cfg parameter ForceCommandGetSerialNumber

* Fri Jul 20 2012 Lawrence R. Rogers <lrr@cert.org> 0.6.12-1
* Release 0.6.12-1
  * Avoiding -O3 / inline compiler bug
  * Correct srceen output if no log file is in use
  * DD verification: retry with NOATIME switched off if open fails
  * DD verification: Do not exit if open fails

* Wed Jul 18 2012 Lawrence R. Rogers <lrr@cert.org> 0.6.11-2
* Release 0.6.11-2
	Built with libguytools 2.0.2

* Wed Jul 4 2012 Lawrence R. Rogers <lrr@cert.org> 0.6.11-1
* Release 0.6.11-1
  * Removed bug where section tables might contain only one entry.
  * New cfg parameter EwfNaming supports 2 methods for naming EWF segment files
  * Added warnings for low space on destination path and large number of image
    files before starting acquisition, new configuration parameters 
    WarnAboutImageSize and WarnAboutSegmentFileCount
  * When opening destination image fails, retry with NOATIME switched off (thus
    enabling cloning without root rights)
  * Removed bug where section tables might contain only one entry.

* Fri Jun 29 2012 Lawrence R. Rogers <lrr@cert.org> 0.6.9-1
* Release 0.6.9-1
  * Releasing all changes of 0.6.8 (switch to new version in order to have test
    users update their packages correctly)
  * AEWF: Considering also 1st chunk base offset when checking if chunk can be
    added to current sectors section.
  * New cfg parameter CheckRootRights
  * If source disk can't be opened, give it another try without option NOATIME
  * Corrected text output for image hash calculation in info file; Translations
    updated.
  * Error in UtilIsZero removed (leading to wrong image if FifoBlockSizeEwf is
    set to values above 65536)
  * Package no longer recommends gksu, smartmontools and hdparm but depends on
    them
  * No longer exits on write errors on info file or in AEWF module (should
    already have been done in 0.6.4, but the takeover from trunk wasn't done)
  * New cfg parameter EwfCompressionThreshold
  * Also include symlinks when searching for libparted
  * Changes from Mika (unistd.h)

* Mon Apr 30 2012 Guy Voncken <vogu00@gmail.com> 0.6.7-1
* Release 0.6.7-1
  * Configuration parameter CommandGetAddStateInfo now understands placeholder
    %local for distinguishing between local and non-local devices.
  * New configuration parameter QueryDeviceMediaInfo for devices that do not 
    like HPA/DCO querying
  * MD5 calculation of destination disk corrected for disks whose size is not 
    a multiple of the block size
  * no longer depends on libproc (using libc functions instead)
  * New, fast SHA256 and MD5 routines (from package coreutils)
  * No longer depends on libcrypto or libcrypto for fast hash functions

* Mon Feb 6 2012 Guy Voncken <vogu00@gmail.com> 0.6.5-1
* Release 0.6.5-1
  * Device scan: Assume that a device will not be included more than once
    in a scan
  * New CFG parameter AvoidEncaseProblems for Encase EWF string limitations

* Fri Dec 30 2011 Guy Voncken <vogu00@gmail.com> 0.6.4-1
* Release 0.6.4-1
  * No longer exits on write errors in AEWF module
  * No longer exits on info file write errors
  * Center info dialog relative to application (not screen)

* Wed Dec 7 2011 Guy Voncken <vogu00@gmail.com> 0.6.3-1
* Release 0.6.3-1
  * Compressed chunks must be smaller than uncompressed chunks without the CRC, or else Encase fails

* Tue Dec 6 2011 Guy Voncken <vogu00@gmail.com> 0.6.2-1
* Release 0.6.2-1
  NOTE: the changes listed here are cumulative to 0.5.9.
  * Better HPA/DCO log output
  * Bug removed where acquisition hash codes were not shown in info file if verification was aborted.
  * Additional State Info added
  * zlib zero block compression / decompression optimised
  * New configuration parameter DirectIO
  * Setting sectors per chunk correctly for libewf
  * Removed full path of image file names from .info file, only show the image filename
  * Bug removal: pDevice->ImageFilehashList was not cleared after acquisition
  * New thread debugging messages
  * New EWF module reduces memory footprint significantly.
  * Posibility to compute MD5 hashes of the individual image files and write them to the .info file.
  * Better log output always contains acquired device
  * Bug removed where libewf only did empty block compression (slight API change in libewf20100226)
  * Compression problem with libewf20100226 fixed
  * Wrong file size check in acquisition dialog corrected

* Fri Jul 8 2011 Guy Voncken <vogu00@gmail.com> 0.5.9-1
* Release 0.5.9-1
	- The 2GiB limit for EWF files no longer exists (the max. size now is 8EiB)
	- A new AutoExit function has been added. If activated, guymager ends as soon as all
	  acquisitions terminated successfully. By means of the program's exit code, a script might decide,
	  for instance, to shut down the system. This feature is interesting for acquisitions taking place
	  overnight or during the weekend.
	- A new menu point in Gnome allows for launching Guymager from the menu Application / System tools.
	- The problems with UDisks under KDE / Kubuntu no longer exist.

* Tue Sep 09 2008 Guy Voncken <vogu00@gmail.com> 0.3.1
- New branch, guymager (0.3.0beta3) becomes 0.3.1, no other changes

* Tue Sep 09 2008 Guy Voncken <vogu00@gmail.com> 0.3.0beta3
- Several things concerning Debian packaging
- New, flexible handling for acquisition dialog fields
- Language support

* Tue Sep 02 2008 Guy Voncken <vogu00@gmail.com> 0.3.0beta2
- New cfg param SpecialFilenameChars for allowing special chars in image and info filenames
- Writing version info also to log file
- Auto-detect number of CPUs for optimal multi-threaded compression
- Special sequence %size% in cfg file expands to non fractional value

* Tue Apr 15 2008 Guy Voncken <vogu00@gmail.com> 0.3.0beta1
- Possibility to chose between self-written or Qt file dialog (cfg param UseFileDialogFromQt)
- Correct display of libewf version in use
- Device matching on device rescan corrected (as some memsticks behave like 2 devices with identical serial nr.)
- When starting without root rights: Ask user if he really wants this

* Tue Apr 01 2008 Guy Voncken <vogu00@gmail.com> 0.2.0beta3
- Locale initialisation added
- MemWatch really switched off if UseMemWatch is false
- Simplified compilation
- Man page added
- Debian package corrections (lintian no longer reports errors)

* Tue Apr 01 2008 Guy Voncken <vogu00@gmail.com> 0.2.0beta2
- Current unstable

* Fri Mar 21 2008 Guy Voncken <vogu00@gmail.com> 0.2.0beta1
- Current unstable

* Wed Sep 12 2007 Guy Voncken <vogu00@gmail.com> 0.1.0-1
- First official branch, released for "BKA-Fachtagung forensische IuK", 18-19 Sept. 2007, D-Knuellwald.
