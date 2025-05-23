%define debug_package %{nil}
%define Major		1.25
%define Minor		9
%define	LCName		veracrypt

Summary:	Disk encryption software 
Name:		VeraCrypt
Version:	%{Major}.%{Minor}
Release:	2%{?dist}
License:	Microsoft Public License
Group:		File tools
URL:		https://www.veracrypt.fr/
Source0:	https://github.com/veracrypt/VeraCrypt/archive/%{name}_%{version}.tar.gz
BuildRequires:	wxGTK3-devel
BuildRequires:	nasm
%if 0%{?centos} == 8
BuildRequires:	yasm
%else
BuildRequires:	yasm-devel
%endif
BuildRequires:	fuse-devel
%if 0%{?centos}
BuildRequires:	ghostscript
%else
BuildRequires:	ghostscript-core
%endif
BuildRequires:	ImageMagick
BuildRequires:	gcc-c++
Provides:	veracrypt = %{version}

%description
Free disk encryption software based on TrueCrypt.

%prep
%setup -qn %{name}_%{version}
#sed -i 's|dumpversion|dumpfullversion|' src/Makefile

%build
pushd src
make WX_CONFIG=wx-config-3.0 || echo 0
popd

pushd src/Resources/Icons
for r in 16 48 256
do
	convert %{name}-${r}x${r}.xpm %{name}-${r}x${r}.png
done
popd

rm -f src/Setup/Linux/usr/bin/veracrypt-uninstall.sh

%install
cd src
%make_install
for r in 16 48 256
do
	install -Dm 0644 Resources/Icons/%{name}-${r}x${r}.png %{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps/%{name}.png
done

%if 0%{?fedora} >= 33
%post
/usr/bin/gtk-update-icon-cache -t -f %{_datadir}/icons/hicolor/
%endif

%files
%{_bindir}/*
%{_sbindir}/*
%{_docdir}/%{LCName}
%{_datadir}/mime
%{_datadir}/%{LCName}
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Sun Mar 10 2022 Lawrence R. Rogers <lrr@cert.org> - 1.25.9-2
- Release 1.25.9-2
	Now calls gtk-update-icon-cache with -t and -f arguments.

* Sun Feb 20 2022 Lawrence R. Rogers <lrr@cert.org> - 1.25.9-1
- Release 1.25.9-1
	Version 1.25.9

* Fri Dec  3 2021 Lawrence R. Rogers <lrr@cert.org> - 1.25.4-1
- Release 1.25.4-1
	Version 1.25.4

* Fri Nov 26 2021 Lawrence R. Rogers <lrr@cert.org> - 1.24.7-3
- Release 1.24.7-3
	Version 1.24.7 release 3 that makes 256x256 icons

* Sat Sep  5 2020 Lawrence R. Rogers <lrr@cert.org> - 1.24.7-2
- Release 1.24.7-2
	Version 1.24 Update 7, patched as of 2021-09-05

* Sun Aug  9 2020 Lawrence R. Rogers <lrr@cert.org> - 1.24.7
- Release 1.24.7
	Version 1.24 Update 7

* Tue Mar 10 2020 Lawrence R. Rogers <lrr@cert.org> - 1.24.6
- Release 1.24.6
	Version 1.24 Update 6

* Tue Oct 08 2019 Wei-Lun Chao <bluebat@member.fsf.org> - 1.24
- Rebuild for Fedora
* Tue Oct 18 2016 Denis Silakov <denis.silakov@rosalab.ru> 1.19-1
- (9623fad) Merge pull request #4 from tremod/veracrypt:rosa2016.1
- (9623fad) Update to 1.19
* Sun Oct 18 2015 Denis Silakov <dsilakov@gmail.com> 1.16-1
- (eac346d) Updated to 1.16
