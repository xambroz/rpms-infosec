%define debug_package %{nil}

Name:		stegdetect
Version:	0.6
Release:	2%{?dist}

Summary:	Detect and extract steganography messages inside JPEG
License:	BSD
Group:		File tools
URL:		https://github.com/abeluck/stegdetect
Source0:	http://www.outguess.org/stegdetect-%version.tar.gz
Patch1:		%{name}-%{version}-patch-001
Patch3:		%{name}-%{version}-patch-003
BuildRoot: 	%{_tmppath}/rpm-root-%{name}-v%{version}

# Automatically added by buildreq on Tue May 16 2006
BuildRequires:	gcc-c++
%if 0%{?centos} >= 8 || 0%{?amzn}
BuildRequires:	gtk2-devel
%else
BuildRequires:	gtk+-devel
%endif

%description
Stegdetect is an automated tool for detecting steganographic content in
images. It is capable of detecting several different steganographic
methods to embed hidden information in JPEG images. Currently, the
detectable schemes are jsteg, jphide, invisible secrets, outguess 01.3b,
F5, appendX, and camouflage. Using linear discriminant analysis, it also
supports detection of new stego systems. Stegbreak is used to launch
dictionary attacks against JSteg-Shell, JPHide, and OutGuess 0.13b.

%prep
%setup -q
%patch1 -p1
%patch3 -p1

%build
# Rename conflicting variable, fixes gcc4 FTBFS.
sed --in-place 's/debug/stegdebug/g' stegdetect.c

%if 0%{?fedora} >= 23 || 0%{?centos} >= 8
%ifarch x86_64
export CC="gcc -fPIC"
%endif
%endif

%ifarch %{ix86}
%configure CFLAGS="-O1 -Wall -g" CXXFLAGS="-O1 -g -march=i686"
%else
%configure CFLAGS="-O1 -Wall -g" CXXFLAGS="-O1 -g"
%endif

%{__make}

%install
# by default 'make install' try to install unneeded thingies...
%makeinstall SUBDIRS=""

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%attr(555,bin,bin)	%{_bindir}/stegbreak
%attr(555,bin,bin)	%{_bindir}/stegcompare
%attr(555,bin,bin)	%{_bindir}/stegdeimage
%attr(555,bin,bin)	%{_bindir}/stegdetect
%attr(444,bin,bin)	%{_mandir}/man1/stegbreak.1.gz
%attr(444,bin,bin)	%{_mandir}/man1/stegdetect.1.gz


%changelog
* Fri Jul 12 2013 Lawrence R. Rogers <lrr@cert.org> 0.6-2
- Release 0.6-2

* Tue May 16 2006 Victor Forsyuk <force@altlinux.ru> 0.6-alt2
- Fix FTBFS with gcc4.

* Tue Jun 21 2005 Victor Forsyuk <force@altlinux.ru> 0.6-alt1
- Initial build.
