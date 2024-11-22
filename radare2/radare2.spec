Name:           radare2
Summary:        The reverse engineering framework
Version:        5.9.8
URL:            https://radare.org/
%global         vcsurl          https://github.com/radareorg/radare2
VCS:            git:%{vcsurl}
#               https://github.com/radareorg/radare2/releases


# %%if 0%%{?rhel} && 0%%{?rhel} == 8
# Radare2 fails to build on EPEL8+s390x
# https://bugzilla.redhat.com/show_bug.cgi?id=1960046
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_architecture_build_failures
# ExcludeArch:    s390x
# %%endif


# by default it builds from the released version of radare2
# to build from git use rpmbuild --without=releasetag
%bcond_without     releasetag

%global         gituser         radareorg
%global         gitname         radare2
%global         gitdate         20241119
%global         commit          4eb49d5ad8c99eaecc8850a2f10bad407067c898
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# autorelease not available on epel7
%if ! ( 0%{?rhel} && 0%{?rhel} <= 7 )
%global         autorelease    1
%endif


%if %{with releasetag}
Release:        %autorelease
Source0:        %{vcsurl}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        %{vcsurl}/archive/%{commit}/%{name}-%{commit}.tar.gz#/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif

# Specific to Fedora - build with system libraries
Patch1:         radare2-5.6.6-use_openssl.patch
Patch3:         radare2-5.9.0-use_magic.patch

# using system-wide LZ4 should be done using conditionals
# Patch4:         radare2-5.6.6-use_lz4.patch

# CVE-2023-4322 - radare2: Heap-based Buffer Overflow in the bf dissassembler
# fix should be part of 5.9.0
# https://github.com/radareorg/radare2/commit/ba919adb74ac368bf76b150a00347ded78b572dd
# Patch5:         radare2-5.8.8-CVE-2023-4322.patch

# CVE-2023-5686 - radare2: heap-buffer-overflow in /radare2/shlr/java/code.c:211:21 in java_print_opcode
# fix should be part of 5.9.0
# https://github.com/radareorg/radare2/commit/1bdda93e348c160c84e30da3637acef26d0348de
# Patch6:         radare2-5.8.8-CVE-2023-5686.patch

# Build reports need for C99 compatibility mode for the index type declaration in the for cycle.
# As rest of the radare2 is strictly defining all index variables prior to for cycle, it is recommended
# to change this one as well
Patch7:           radare2-5.9.8-dec99.patch


License:        LGPL-3.0-or-later AND GPL-2.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND MIT AND Apache-2.0 AND MPL-2.0 AND Zlib
# Radare2 as a package is targeting to be licensed/compiled as LGPLv3+
# during build for Fedora the GPL code is not omitted so effectively it is GPLv2+
# some code has originally different license:
# libr/asm/arch/ - GPLv2+, MIT, GPLv3
# libr/bin/format/pe/dotnet - Apache License Version 2.0
# libr/hash/xxhash.c - 2 clause BSD
# libr/util/qrcode.c - MIT
# shlr/grub/grubfs.c - LGPL
# shlr/java - Apache 2.0
# shlr/sdb/src - MIT
# shlr/lz4 - 3 clause BSD (system installed shared lz4 is used instead)
# shlr/squashfs/src - GPLv2+
# libr/parse/c - LGPLv2+
# shlr/udis86 - 2 clause BSD
# shlr/winkd - LGPL v3+
# shlr/spp - MIT
# shlr/zip/zlib - zlib/libpng License (system installed shared libzip is used instead)
# shlr/zip/zip - 3 clause BSD (system installed shared zlib is used instead)
# shlr/ptrace-wrap - LGPL v3+
# shlr/tree-sitter - MIT
# shlr/mpc - 2 clause BSD
# shlr/yxml - MIT

# Removed from the final package because of the presence of minified JS and
# absence of the source JS - this should be packaged with radare2-webui
# shlr/www/m - Apache-2.0
# shlr/www/enyo/vendors/jquery-ui.min.js - GPL + MIT
# shlr/www/enyo/vendors/jquery.layout-latest.min.js - GPL + MIT
# shlr/www/enyo/vendors/jquery.scrollTo.min.js - MIT
# shlr/www/enyo/vendors/lodash.min.js - lodash license
# shlr/www/enyo/vendors/joint.* - Mozilla MPL 2.0
# shlr/www/enyo/vendors/jquery.min.js - Apache License version 2.0
# shlr/www/p/vendors/jquery* - GPL + MIT
# shlr/www/p/vendors/dagre*|graphlib* - 3 clause BSD
# shlr/www/p/vendors/jquery.onoff.min.js - MIT

BuildRequires:  sed
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
# xxhash-devel
BuildRequires:  pkgconfig(libxxhash)

# version of libzip on rhel7 is too old
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  pkgconfig(libzip)
%endif

BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(capstone) >= 3.0.4
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(openssl)

%if 0%{?rhel}
BuildRequires:  file-devel
BuildRequires:  bzip2-devel
BuildRequires:  python3
# %%meson macro using the %%set_build_flags from Fedora/EPEL, but not bringing the dependency
# https://src.fedoraproject.org/rpms/meson/pull-request/9
BuildRequires:  epel-rpm-macros
# On RHEL xxhash-devel is not bringing the xxhash as dependency
BuildRequires:  xxhash

%else
# file-devel
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(bzip2)
%endif

Requires:       %{name}-common = %{version}-%{release}

# Package contains several bundled libraries

# ./shlr/zip/zlib/README
# compiled with -D use_sys_zip=true and -D use_sys_zlib=true instead

# ./shlr/lz4/README.md
# compiled with -D use_sys_lz4=true instead

# ./libr/magic/README
# compiled with -D use_sys_magic=true instead

# ./shlr/capstone.sh
# compiled with -D use_sys_capstone=true instead

# ./libr/hash/xxhash.*
# compiled with -D use_sys_xxhash=true instead

# ./libr/hash/{md4,md5,sha1,sha2}.{c,h}
# ./libr/util/big.c
# could be compiled with -D use_sys_openssl=true instead,
# but is currently not maintained so using embedded R2 implementations
# for hashing

# ./shlr/spp/README.md
# SPP stands for Simple Pre-Processor, a templating language.
# https://github.com/radare/spp
Provides:       bundled(spp) = 1.2.0

# ./shlr/sdb/README.md
# sdb is a simple string key/value database based on djb's cdb
# https://github.com/radare/sdb
Provides:       bundled(sdb) = 1.8.6

# ./shlr/sdb/src/json/README
# Based on js0n with a lot of modifications
# https://github.com/quartzjer/js0n
# JSON support for sdb.
Provides:       bundled(js0n) = 2018

# libr/util/regex/README
# Modified OpenBSD regex to be portable
# cvs -qd anoncvs@anoncvs.ca.openbsd.org:/cvs get -P src/lib/libc/regex
# version from 2010/11/21 00:02:30, version of files ranges from v1.11 to v1.20
Provides:       bundled(openbsdregex) = 1.11

# ./libr/parse/c/README.md
# This is a stripped down version of tcc without the code generators and heavily modified.
Provides:       bundled(tcc) = 0.9.26

# ./libr/asm/arch/tricore/README.md
# Based on code from https://www.hightec-rt.com/en/downloads/sources/14-sources-for-tricore-v3-3-7-9-binutils-1.html
# part of binutils to read machine code for Tricore architecture
# ./libr/asm/arch/ppc/gnu/
# part of binutils to read machine code for ppc architecture
# ./libr/asm/arch/arm/gnu/
Provides:       bundled(binutils) = 2.13

# ./libr/asm/arch/avr/README
# * This code has been ripped from vavrdisasm 1.6
Provides:       bundled(vavrdisasm) = 1.6

# ./shlr/grub/*
# It is not clear which version has been copied
Provides:       bundled(grub2) = 1.99~beta0

# ./libr/io/ptrace_wrap.c
# https://github.com/thestr4ng3r/ptrace-wrap
Provides:       bundled(ptrace-wrap) = 20181018

# ./shlr/tree-sitter
# https://github.com/tree-sitter/tree-sitter
Provides:       bundled(tree-sitter) = 0.17.2

# ./shlr/mpc
# https://github.com/orangeduck/mpc
Provides:       bundled(mpc) = 0.8.7

# ./shlr/yxml
# https://dev.yorhel.nl/yxml
Provides:       bundled(yxml) = 20201108

# and likely some more in libr/... borrowed from other projects

%description
The radare2 is a reverse-engineering framework that is multi-architecture,
multi-platform, and highly scriptable.  Radare2 provides a hexadecimal
editor, wrapped I/O, file system support, debugger support, diffing
between two functions or binaries, and code analysis at opcode,
basic block, and function levels.


%package devel
Summary:        Development files for the radare2 package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       file-devel
Requires:       openssl-devel

%description devel
Development files for the radare2 package. See radare2 package for more
information.


%package common
Summary:        Arch-independent SDB files for the radare2 package
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description common
Arch-independent SDB files used by radare2 package. See radare2 package for more
information


%prep
%if %{with releasetag}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}
%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
# Rename internal "version-git" to "version"
sed -i -e "s|%{version}-git|%{version}|g;" configure configure.acr
%endif
# Removing zip/lzip files because we use system dependencies
# version of libzip on rhel7 is too old, use the embedded one instead
%if 0%{?fedora} || 0%{?rhel} >= 8
rm -rf shlr/zip/{zip,zlib,include}
%endif

# Remove lx4 files because we use system dependencies
rm -rf shlr/lz4/{deps.mk,LICENSE,lz4.*,Makefile,README.md}
# Remove xxhash files because we use system dependencies
rm -f libr/hash/xxhash.c libr/hash/xxhash.h
# Remove magic files because we use system dependencies
awk 'BEGIN {p=1} /#if USE_LIB_MAGIC/ {p=2; next} p==2 && /#else/ {p=0} p>0 {print}' libr/magic/magic.c > libr/magic/magic.c.stripped
awk 'BEGIN {p=1} /#if !USE_LIB_MAGIC/ {p=0; next} p==2 && /#else/ {p=0} p>0 {print}' libr/magic/ascmagic.c > libr/magic/ascmagic.c.stripped
rm -rf libr/magic/*.c
mv libr/magic/magic.c.stripped libr/magic/magic-libmagic.c
mv libr/magic/ascmagic.c.stripped libr/magic/ascmagic-libmagic.c
# Remove openssl files because we use system dependencies
# rm -f libr/hash/{md4,md5,sha1,sha2}.[ch]

# Webui contains pre-build and/or minimized versions of JS libraries without source code
# Consider installing the web-interface from https://github.com/radare/radare2-webui
rm -rf ./shlr/www/*
echo "The radare2 source usually comes with a pre-built version of the web-interface, but without the source code." > ./shlr/www/README.Fedora
echo "This has been removed in the Fedora package to follow the Fedora Packaging Guidelines." >> ./shlr/www/README.Fedora
echo "Available under https://github.com/radare/radare2-webui" >> ./shlr/www/README.Fedora

%if 0%{?rhel} && 0%{?rhel} == 8
# Meson on EPEL8 is older than meson on EPEL7 and older than recommended one
# on EPEL8 downgrade the recommendation in meson.build and pray
# meson_version : '>=0.50.1' => meson_version : '>=0.49.1'
sed -i -e "s|meson_version : '>=......'|meson_version : '>=0.49.1'|;" meson.build
%endif


%build
# Whereever possible use the system-wide libraries instead of bundles
#     --sanitize=address,undefined,signed-integer-overflow \

%meson \
    -Duse_sys_magic=true \
%if 0%{?fedora} || 0%{?rhel} >= 8
    -Duse_sys_zip=true \
%else
    -Duse_sys_zip=false \
%endif
    -Duse_sys_zlib=true \
    -Duse_sys_lz4=true \
    -Duse_sys_xxhash=true \
    -Duse_ssl=true \
    -Duse_libuv=true \
%ifarch s390x
    -Ddebugger=false \
%endif
    -Duse_sys_capstone=true \
    -Denable_tests=false \
    -Denable_r2r=false \
    -Dwant_threads=false     # multithreading doesn't work well with Iaito package
%meson_build


%install
%meson_install
# install README.Fedora for the www part
mkdir -p %{buildroot}/%{_datadir}/%{name}/%{version}/www
cp ./shlr/www/README.Fedora %{buildroot}/%{_datadir}/%{name}/%{version}/www/README.Fedora
# remove unneeded fortunes
rm %{buildroot}/%{_datadir}/doc/%{name}/fortunes.fun

# Make directory for the plugins
# Users can learn the dirname by "r2 -H"
mkdir -p %{buildroot}%{_libdir}/%{name}/%{version}


%if 0%{?rhel} && 0%{?rhel} <= 8
%ldconfig_scriptlets
%endif


%check
# Do not run the testsuite yet - it pulls another package
# https://github.com/radare/radare2-regressions from github make tests


%files
%license COPYING COPYING.LESSER
%doc CONTRIBUTING.md DEVELOPERS.md README.md
%doc doc/3D/ doc/pdb/ doc/sandbox/
%doc doc/avr.md doc/brainfuck.md doc/calling-conventions.md doc/debug.md
%doc doc/esil.md doc/gdb.md doc/gprobe.md doc/intro.md doc/io.md doc/rap.md
%doc doc/siol.md doc/strings.md doc/windbg.md doc/yara.md
%doc %{_datadir}/doc/%{name}/fortunes.tips
%dir %{_datadir}/%{name}/%{version}/www
# Webui removed cuz of having minified js code and missing source code
%doc %{_datadir}/%{name}/%{version}/www/README.Fedora
%{_bindir}/r*
%{_libdir}/libr_*.so.%{version}*
# Empty directory for plugins
%{_libdir}/%{name}
%{_mandir}/man1/r*.1.*
%{_mandir}/man7/esil.7.*
%{_datadir}/zsh/site-functions/_r*


%files devel
%{_includedir}/libr
%{_libdir}/libr*.so
%{_libdir}/pkgconfig/*.pc


%files common
%{_datadir}/%{name}/%{version}/cons
%{_datadir}/%{name}/%{version}/fcnsign
%{_datadir}/%{name}/%{version}/flag
%{_datadir}/%{name}/%{version}/format
%{_datadir}/%{name}/%{version}/hud
%{_datadir}/%{name}/%{version}/magic
%{_datadir}/%{name}/%{version}/opcodes
%{_datadir}/%{name}/%{version}/syscall
%{_datadir}/%{name}/%{version}/charsets
%{_datadir}/%{name}/%{version}/platform
%{_datadir}/%{name}/%{version}/scripts

%dir %{_datadir}/%{name}
%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/%{name}/%{version}


%changelog
%if ! ( 0%{?rhel} && 0%{?rhel} <= 7 )
%autochangelog
%endif
