%define debug_package %{nil}

Name:		scrounge-ntfs
Version:	0.9
Release:	1%{?dist}

Summary:	Data recovery program for NTFS file systems
License:	BSD
Group:		File tools
URL:		http://thewalter.net/stef/software/scrounge/
Source0:	http://thewalter.net/stef/software/scrounge/scrounge-ntfs-0.9.tar.gz
BuildRoot: 	%{_tmppath}/rpm-root-%{name}-v%{version}

# Automatically added by buildreq on Tue May 16 2006
BuildRequires:	gcc-c++
%if 0%{?centos} >= 8 || 0%{?amzn}
BuildRequires:	gtk2-devel
%else
BuildRequires:	gtk+-devel
%endif

%description
scrounge-ntfs is a utility that can rescue data from corrupted NTFS partitions. It 
writes the files retrieved to another working file system. Certain 
information about the partition needs to be known in advance. 

%prep
%setup -q

%build
# Rename conflicting variable, fixes gcc4 FTBFS.

%configure --prefix=/usr --mandir=/usr/share/man --bindir=/usr/bin
%{__make}

%install
# by default 'make install' try to install unneeded thingies...
%makeinstall 

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%attr(555,bin,bin)	%{_sbindir}/%name
%attr(444,bin,bin)	%{_mandir}/man8/%name.8.gz

%changelog
* Mon Aug 16 2010 Stef Walter <stef@memberwebs.com> 0.9
 - Use my real name 'Stef Walter'
   See: http://memberwebs.com/nielsen/

* Mon Aug 16 2010 Stef Walter <stef@memberwebs.com> 0.8.7
 - Fix crasher on corrupted drives. A problem with update 
   sequence offset being filled with garbage [Albert Kwok]

* Mon Aug 16 2010 Stef Walter <stef@memberwebs.com> 0.8.6
 - Don't exit on error reading source drive [Marius Hillenbrand]
 - Fixed core dump when attribute list, but no MFT loaded [Marius Hillenbrand]

* Mon Aug 16 2010 Stef Walter <stef@memberwebs.com> 0.8.5
 - Ported to Linux/FreeBSD
 - Support for very fragmented MFTs
 - Fixed memory leaks
 - Fixed many bugs

* Mon Aug 16 2010 Stef Walter <stef@memberwebs.com> 0.8
 - Support for non-contiguous MFT
 - Better support for WinXP NTFS
 - Other bug fixes

* Mon Aug 16 2010 Stef Walter <stef@memberwebs.com> 0.7
 - Initial public release

