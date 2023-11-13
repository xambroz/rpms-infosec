Name:           rizin
Summary:        UNIX-like reverse engineering framework and command-line tool-set
Version:        0.6.3
%global         baserelease     1
URL:            https://rizin.re/
VCS:            https://github.com/rizinorg/rizin

%global         gituser         rizinorg
%global         gitname         rizin
%global         shortversion    %(c=%{version}; echo ${c} | cut -d'.' -f-2)

Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/v%{version}/%{name}-src-v%{version}.tar.xz

License:        LGPL-3.0-or-later AND GPL-2.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND MIT AND Apache-2.0 AND MPL-2.0 AND Zlib


BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  python3-pyyaml

%if 0%{?rhel}
# rhel8 file-devel package stil doesn't provide pkgconfig 
BuildRequires:  file-devel
%else
BuildRequires:  pkgconfig(libmagic)
%endif
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(capstone) >= 3.0.4
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(tree-sitter)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libmspack)

Requires:       %{name}-common = %{version}-%{release}

# Package contains several bundled libraries that are used in Fedora builds

# ./shlr/spp/README.md
# SPP stands for Simple Pre-Processor, a templating language.
# https://github.com/rizinorg/spp
Provides:       bundled(spp) = 1.2.0

# ./shlr/sdb/README.md
# sdb is a simple string key/value database based on djb's cdb
# https://github.com/rizinorg/sdb
Provides:       bundled(sdb) = db7edd4a96a89b6749b677a85d7fa4ee2c6fbbb9

# librz/util/regex/README
# Modified OpenBSD regex to be portable
# cvs -qd anoncvs@anoncvs.ca.openbsd.org:/cvs get -P src/lib/libc/regex
# version from 2010/11/21 00:02:30, version of files ranges from v1.11 to v1.20
Provides:       bundled(openbsdregex) = 1.11

# ./librz/asm/arch/tricore/README.md
# Based on code from https://www.hightec-rt.com/en/downloads/sources/14-sources-for-tricore-v3-3-7-9-binutils-1.html
# part of binutils to read machine code for Tricore architecture
# ./librz/asm/arch/ppc/gnu/
# part of binutils to read machine code for ppc architecture
# ./librz/asm/arch/arm/gnu/
Provides:       bundled(binutils) = 2.13

# ./librz/asm/arch/avr/README
# * This code has been ripped from vavrdisasm 1.6
Provides:       bundled(vavrdisasm) = 1.6

# rizin-v0.5.0/subprojects/blake3
# url = https://github.com/BLAKE3-team/BLAKE3.git
# revision = f84636e59ce575e5dd127399e0c7de0c1ea595da
Provides:       bundled(blake3) = 1.3.1



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
%autosetup -n %{gitname}-v%{version}

%build
# Whereever possible use the system-wide libraries instead of bundles
%meson \
    -Duse_sys_magic=enabled \
    -Duse_sys_libzip=enabled \
    -Duse_sys_zlib=enabled \
    -Duse_sys_lz4=enabled \
    -Duse_sys_xxhash=enabled \
    -Duse_sys_openssl=enabled \
    -Duse_sys_capstone=enabled \
    -Duse_sys_tree_sitter=enabled \
    -Duse_sys_lzma=enabled \
    -Duse_sys_libmspack=enabled \
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
%ldconfig_scriptlets


%check
# Do not run the unit testsuite yet - it pulls another big repository
# https://github.com/rizinorg/rizin-testbins from github



%files
%doc CONTRIBUTING.md DEVELOPERS.md README.md SECURITY.md BUILDING.md
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/librz_*.so.%{version}*
%{_libdir}/librz_*.so.%{shortversion}
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
* Mon Nov 13 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.6.3-1
- Rebase to upstream version 0.6.3
- change license string to comply with the SPDX

* Mon Aug 21 2023 Riccardo Schirone <rschirone91@gmail.com> - 0.6.1-1
- Rebase to upstream version 0.6.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.5.2-2
- cosmetics, remove the excessive .2 in the release
- use baserelese (recognized by rpmdev-bumpspec used for massrebuilds)
- prepare to sync for the feature branches
- fix dependencies for rhel

* Wed May 17 2023 Riccardo Schirone <rschirone91@gmail.com> - 0.5.2-1.2
- Rebase to upstream version 0.5.2

* Tue Mar 14 2023 Riccardo Schirone <rschirone91@gmail.com> - 0.5.1-1
- Rebase to upstream version 0.5.1

* Sun Feb 19 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.5.0-1
- Rebase to upstream version 0.5.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Sep 10 2022 Richard Hughes <richard@hughsie.com> - 0.4.1-1
- Rebase to upstream version 0.4.1
- Fixed CVE-2022-36039
- Fixed CVE-2022-36040
- Fixed CVE-2022-36041
- Fixed CVE-2022-36042
- Fixed CVE-2022-36043
- Fixed CVE-2022-36044

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Riccardo Schirone <rschirone91@gmail.com> - 0.4.0-2
- Increase release number to put in the side-tag

* Mon Jun 27 2022 Riccardo Schirone <rschirone91@gmail.com> - 0.4.0-1
- Rebase to upstream version 0.4.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Riccardo Schirone <rschirone91@gmail.com> - 0.3.4-1
- Rebase to upstream version 0.3.4

* Mon Jan 3 2022 Riccardo Schirone <rschirone91@gmail.com> - 0.3.2-1
- Rebase to upstream version 0.3.2

* Mon Nov 29 2021 Riccardo Schirone <rschirone91@gmail.com> - 0.3.1-1
- Rebase to upstream version 0.3.1

* Mon Sep 27 2021 Riccardo Schirone <rschirone91@gmail.com> - 0.3.0-1
- Rebase to upstream version 0.3.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.2.0-2.2
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 20 2021 Riccardo Schirone <rschirone91@gmail.com> - 0.2.0-2
- Apply patch to avoid symbols collision

* Mon Apr 12 2021 Riccardo Schirone <rschirone91@gmail.com> - 0.2.0-1
- Rebase to upstream version 0.2.0

* Tue Mar 30 2021 Riccardo Schirone <rschirone91@gmail.com> - 0.1.2-1
- Initial SPEC file
