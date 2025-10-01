Name:           rizin
Summary:        UNIX-like reverse engineering framework and command-line tool-set
Version:        0.8.1

%global forgeurl https://github.com/rizinorg/rizin
%forgemeta

Release:        %autorelease
URL:            https://rizin.re/

Source0:        %{forgeurl}/releases/download/v%{version}/%{name}-src-v%{version}.tar.xz

# https://github.com/rizinorg/rizin/pull/5414
Patch:          rizin-0001-Add-option-to-use-system-BLAKE3.patch

# https://github.com/rizinorg/rizin/pull/5417
Patch:          rizin-0002-Fix-using-system-libpcre2.patch

# see .reuse/dep5 for license breakdown
License:        LGPL-3.0-only AND LGPL-2.1-or-later AND LGPL-2.1-only AND LGPL-2.0-or-later AND GPL-3.0-or-later AND GPL-2.0-or-later AND GPL-2.0-only AND GPL-1.0-or-later AND MIT AND Apache-2.0 AND NCSA AND BSD-3-Clause AND BSD-2-Clause AND CC-BY-SA-4.0 AND CC0-1.0 AND CC-PDDC


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  python3-pyyaml

BuildRequires:  pkgconfig(capstone) >= 3.0.4
%if 0%{?rhel}
# rhel8 file-devel package stil doesn't provide pkgconfig 
BuildRequires:  file-devel
%else
BuildRequires:  pkgconfig(libmagic)
%endif
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libmspack)
BuildRequires:  pkgconfig(tree-sitter)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libblake3)

Requires:       %{name}-common = %{version}-%{release}

# Package contains several bundled libraries that are used in Fedora builds

# subprojects/spp
# SPP stands for Simple Pre-Processor, a templating language.
# https://github.com/rizinorg/spp
Provides:       bundled(spp) = 1.2.0

# all binutils code resides in librz/arch/p_gnu/ and librz/arch/isa_gnu/
# last update's upstream commit: 4ed07377e47addf4dd0594ac5b16d7e4cdb19436
# BFD_VERSION_DATE = 20221025
Provides:       bundled(binutils) = 2.39.50~20221025

# subprojects/softfloat
# url = https://github.com/rizinorg/softfloat
# version: 3e
Provides:       bundled(softfloat3) = 3e~git537d18e

%description
Rizin is a free and open-source Reverse Engineering framework, providing a
complete binary analysis experience with features like Disassembler,
Hexadecimal editor, Emulation, Binary inspection, Debugger, and more.

Rizin is a fork of radare2 with a focus on usability, working features and code
cleanliness.


%package devel
Summary:        Development files for the rizin package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       file-devel
Requires:       openssl-devel

%description devel
Development files for the rizin package. See rizin package for more
information.


%package common
Summary:        Arch-independent SDB files for the rizin package
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description common
Arch-independent SDB files used by rizin package. See rizin package for more
information


%prep
# Build from git release version
%autosetup -p1 -n %{name}-v%{version}

%build
# Whereever possible use the system-wide libraries instead of bundles
%meson \
    -Duse_sys_capstone=enabled \
    -Duse_sys_magic=enabled \
    -Duse_sys_libzip=enabled \
    -Duse_sys_zlib=enabled \
    -Duse_sys_lz4=enabled \
    -Duse_sys_libzstd=enabled \
    -Duse_sys_lzma=enabled \
    -Duse_sys_xxhash=enabled \
    -Duse_sys_openssl=enabled \
    -Duse_sys_libmspack=enabled \
    -Duse_sys_tree_sitter=enabled \
    -Duse_sys_pcre2=enabled \
    -Duse_sys_blake3=enabled \
%ifarch s390x
    -Ddebugger=false \
%endif
    -Denable_tests=false \
    -Denable_rz_test=false \
    -Dlocal=disabled \
    -Dpackager="Fedora" \
    -Dpackager_version="%{version}-%{release}"
%meson_build

%install
%meson_install


%check
# Do not run the unit testsuite yet - it pulls another big repository
# https://github.com/rizinorg/rizin-testbins from github



%files
%doc CONTRIBUTING.md DEVELOPERS.md README.md SECURITY.md BUILDING.md
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/librz_*.so.%{version}*
%{_libdir}/librz_*.so.0.8
%{_mandir}/man1/rizin.1.*
%{_mandir}/man1/rz*.1.*
%{_mandir}/man7/rz-esil.7.*


%files devel
%{_includedir}/librz
%{_libdir}/librz*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/**/*.cmake
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/**


%files common
%{_datadir}/%{name}/arch
%{_datadir}/%{name}/asm
%{_datadir}/%{name}/cons
%{_datadir}/%{name}/flag
%{_datadir}/%{name}/format
%{_datadir}/%{name}/fortunes
%{_datadir}/%{name}/hud
%{_datadir}/%{name}/magic
%{_datadir}/%{name}/opcodes
%{_datadir}/%{name}/reg
%{_datadir}/%{name}/syscall
%{_datadir}/%{name}/types
%dir %{_datadir}/%{name}


%changelog
%autochangelog
