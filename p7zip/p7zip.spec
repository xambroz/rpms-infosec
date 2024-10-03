%if ( 0%{?rhel} && ! 0%{?epel} ) || 0%{?epel} == 8
%bcond_with gui
%else
%bcond_without gui
%endif

Summary: Very high compression ratio file archiver
Name: p7zip
Version: 16.02
Release: %autorelease
# Files under C/Compress/Lzma/ are dual LGPL or CPL
# Automatically converted from old format: LGPLv2 and (LGPLv2+ or CPL) - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2 AND (LicenseRef-Callaway-LGPLv2+ OR CPL-1.0)
URL: http://p7zip.sourceforge.net/
# RAR sources removed since their license is incompatible with the LGPL
#Source: http://downloads.sf.net/p7zip/p7zip_%%{version}_src_all.tar.bz2
# export VERSION=15.14.1
# wget http://downloads.sf.net/p7zip/p7zip_${VERSION}_src_all.tar.bz2
# tar xjvf p7zip_${VERSION}_src_all.tar.bz2
# rm -rf p7zip_${VERSION}/CPP/7zip/{Archive,Compress,Crypto,QMAKE}/Rar*
# rm p7zip_${VERSION}/DOC/unRarLicense.txt
# tar --numeric-owner -cjvf p7zip_${VERSION}_src_all-norar.tar.bz2 p7zip_${VERSION}
Source: p7zip_%{version}_src_all-norar.tar.bz2
Patch0: p7zip_15.14-norar_cmake.patch
# from Debain
Patch4: p7zip-manpages.patch
Patch5: 02-man.patch
Patch6: CVE-2016-9296.patch
Patch7: 05-hardening-flags.patch
Patch10: CVE-2017-17969.patch
Patch11: 14-Fix-g++-warning.patch
Patch12: gcc10-conversion.patch
Patch13: 0001-fix-data-null-pointer.patch
Patch14: 0001-fix-out-of-mem.patch
Patch15: p7zip-015-hide-passwd.patch

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: cmake
%if %{with gui}
# for 7zG GUI
BuildRequires: wxGTK-devel
BuildRequires: kde-filesystem
%endif
%ifarch %{ix86}
BuildRequires: nasm
%endif
%ifarch x86_64
BuildRequires: yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.


%package plugins
Summary: Additional plugins for p7zip

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.

%if %{with gui}
%package gui
Summary: 7zG - 7-Zip GUI version
Requires: kde-filesystem
Requires: p7zip-plugins

%description gui
7zG is a gui provide by p7zip and it is now in beta stage.
Also add some context menus for KDE4.
This package is *experimental*.
%endif

%package        doc
Summary:        Manual documentation and contrib directory
BuildArch:      noarch

%description    doc
This package contains the p7zip manual documentation and some code
contributions.

%prep
%autosetup -p1 -n %{name}_%{version}

# move license files
mv DOC/License.txt DOC/copying.txt .

%build
pushd CPP/7zip/CMAKE/
sh ./generate.sh
popd
%ifarch %{ix86}
cp -f makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif
%ifarch x86_64
cp -f makefile.linux_amd64_asm makefile.machine
%endif
%ifarch ppc ppc64
cp -f makefile.linux_any_cpu_gcc_4.X makefile.machine
%endif

%make_build all2 \
%if %{with gui}
	7zG \
%endif
    OPTFLAGS="%{optflags}" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%install
make install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}

# remove redundant DOC dir
mv %{buildroot}%{_docdir}/p7zip/DOC/* %{buildroot}%{_docdir}/p7zip
rmdir %{buildroot}%{_docdir}/p7zip/DOC/

%if %{with gui}
mkdir -p %{buildroot}%{_datadir}/kservices5/
# remove a duplicated of p7zip_compress.desktop
rm GUI/kde4/p7zip_compress2.desktop
cp GUI/kde4/*.desktop %{buildroot}%{_datadir}/kservices5/
#fix non-executable-in-bin
chmod +x %{buildroot}%{_bindir}/p7zipForFilemanager
%endif

%check
%if ! 0%{?rhel} || 0%{?rhel} >= 7
make test
%endif
# Next test fails, because we don't have X11 envoirment ...
# Error: Unable to initialize gtk, is DISPLAY set properly?
#make test_7zG || :


%files
%{_docdir}/p7zip
%exclude  %{_docdir}/p7zip/MANUAL
%license copying.txt License.txt
%{_bindir}/7za
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx
%{_mandir}/man1/7za.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%{_bindir}/7z
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/7z.so
#{_libexecdir}/p7zip/Codecs/
#{_libexecdir}/p7zip/Formats/
%{_mandir}/man1/7z.1*

%if %{with gui}
%files gui
%{_bindir}/7zG
%{_bindir}/p7zipForFilemanager
%{_libexecdir}/p7zip/7zG
%{_libexecdir}/p7zip/Lang
%{_datadir}/kservices5/*.desktop
%endif

%files doc
%{_docdir}/p7zip/MANUAL
%doc contrib/


%changelog
%autochangelog
