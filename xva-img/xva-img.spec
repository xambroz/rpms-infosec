%define debug_package %{nil}

Summary:	xva-img - Assemble Citrix XEN disk image

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		xva-img
Version:	1.4.2
Release:	2%{?dist}
URL:		https://github.com/eriklax/xva-img

License:	GPL

Group:		Applications/Forensics Tools
#               https://github.com/eriklax/xva-img/archive/refs/tags/1.4.2.tar.gz
Source:		%{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}
%if  0%{?centos} == 7
BuildRequires:	cmake3
%else
BuildRequires:	cmake
%endif
BuildRequires:	openssl-devel
%if 0%{?centos}0%{?amzn} == 70
BuildRequires:  devtoolset-7-gcc-c++
%endif
%if 0%{?centos} >= 8 || 0%{?amzn}
BuildRequires:	gcc-c++
%endif
%if 0%{?fedora}
BuildRequires:	g++
%endif

%description
Citrix Xen uses a custom virtual appliance format for import/export called "XVA". it's basically
a strangely crafted tar-file. You don't need this program to unpack this tar-file, just use
your favourite tar unpacker (tar, gtar, bsdtar). Once unpacked you will end up with a lot of
different files, ova.xml (which contains the settings for the virtual appliance, think VMware
vmx) and a number of folders called Ref:/, this is your disks. Each of these folders contain
hundreds of files named 00000000, 00000001 with a accompanying .CHECKSUM file (SHA1). Each file
is a 1MB slice of the disk, but some of the files in the sequence will probably be missing this is
because XVA do not use compression; instead it will exclude slices of the disk that only contains
zeros (are empty). This tool can assemble the disk for you (you will end up with a RAW disk)
that can easily be mounted and modified. It can then also split the file again and generate
checksum. Once ready, you will probably want to use the "package" command to rebuild the XVA file.

%prep
%setup

%build
mkdir build
cd build
%if 0%{?centos}0%{?amzn} == 70
echo cmake3 .. | scl enable devtoolset-7 -
echo %{__make} | scl enable devtoolset-7 -
%else
%if 0%{?amzn}
cmake3 ..
%else
cmake ..
%endif
%endif
%{__make}

%install
cd build
%{__install} -Dp -m 755 %{name} %{buildroot}%{_bindir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644, root, root, 0755)
%doc CHANGELOG INSTALL LICENSE README.md 
%attr(0755, root, root) %{_bindir}/%{name}

%changelog
* Sat Jul  3 2021 Lawrence R. Rogers <lrr@cert.org> 1.4.2-2
* Release 1.4.2-2
	Version 1.4.202 - changed modes for xva-img to 755.

* Fri Mar  5 2021 Lawrence R. Rogers <lrr@cert.org> 1.4.2-1
* Release 1.4.2-1
	Version 1.4.2

* Wed Jun 12 2019 Lawrence R. Rogers <lrr@cert.org> 1.3-1
* Release 1.3-1
	Initial release
