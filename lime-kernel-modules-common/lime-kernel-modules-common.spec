Name:		lime-kernel-modules-common
Version:	1.7.8
License:	GPL
Vendor:		cert.org
Packager:	Lawrence R. Rogers (lrr@cert.org)
Group:		Applications/Forensics Tools
Summary:	This package contains the source code for making LiME Modules


%global         debug_package   %{nil}

%global         gituser         504ensicsLabs
%global         gitname         LiME
# Current version
%global         gitdate         20130410
%global         commit          ab48695b7113db692982a1839e3d6eb9e73e90a9
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:	1

URL:		https://github.com/504ensicsLabs/LiME
#Source0:	lime-forensics-%{version}.tar.gz
Source0:	https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{gitname}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}

Obsoletes:	lime-kernel-objects

BuildArch:	noarch

%description
This package provides a script to install and use the kernel objects.
These modules are now packaged separately.
This package is intended to be shared across all OSes and architectures

%prep
%autosetup -n %{gitname}-%{version}

%build

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 755 CaptureMemoryWithLime %{buildroot}/%{_bindir}
%__install -d %{buildroot}%{_mandir}/man1
%__install CaptureMemoryWithLime.1 %{buildroot}%{_mandir}/man1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc disk.c lime.h main.c tcp.c Makefile Makefile.sample LiME_Documentation_1.1.pdf 
%attr(755, root, root)	%{_bindir}/CaptureMemoryWithLime
%attr(0644, root, root)	%{_mandir}/man1/*.1.gz

%changelog
* Fri Jun  2 2017 Lawrence R. Rogers <lrr@cert.org> 1.1.r17-4
* Release 1.1.r17-4
	Updated tcp.c due to changes in the 4.11 kernel.
	
* Fri Sep  9 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.r17-3
* Release 1.1.r17-3
	Updated these files:
		main.c
	to be in sync with the LiME Forensics Source code repository.

	Also updated CaptureMemoryWithLime and CaptureMemoryWithLime.1 to change the default location
		of the modules directory.

* Tue Jul 12 2016 Lawrence R. Rogers <lrr@cert.org> 1.1.r17-2
* Release 1.1.r17-2
	Updated these files:
		disk.c
		lime.h
		main.c
		Makefile
		tcp.c
	to be in sync with the LiME Forensics Source code repository.

* Mon Jun 2 2014 Lawrence R. Rogers <lrr@cert.org> 1.1.r17-1
* Release 1.1.r17-1
	This is the initial release of this package.
	It contains all of the OS and architecture-independent parts of LiME.
