Name:           rizin
Summary:        The reverse engineering framework
Version:        0.1.2
%global         rel              1
URL:            https://rizin.re/
VCS:            https://github.com/rizinorg/rizin

# by default it builds from the released version of rizin
%bcond_without  build_release

%global         gituser         rizinorg
%global         gitname         rizin

%global         gitdate         20210329
%global         commit          810bb14e0baa584699def7beb841a37fc9987cfb
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         sdb_commit      29ce97365dead99bf6892d07bd2692aa169ff2ac

%global         ts_version      0.19.4


%if %{with build_release}
Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{rel}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{commit}.zip
%endif

# Bundled libraries
Source1:        https://github.com/%{gituser}/sdb/archive/%{sdbcommit}/%{name}-sdb-%{sdb_commit}.tar.gz
Source2:	https://github.com/tree-sitter/tree-sitter/archive/refs/tags/v%{ts_version}.tar.gz#/%{name}-tree-sitter-%{ts_version}.tar.gz

Patch0:         rizin-meson-sdb.patch


License:        LGPLv3+ and GPLv2+ and BSD and MIT and ASL 2.0 and MPLv2.0 and zlib
# rizin as a package is targeting to be licensed/compiled as LGPLv3+
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
# shlr/spp - MIT
# shlr/squashfs/src - GPLv2+
# shlr/tcc - LGPLv2+
# shlr/udis86 - 2 clause BSD
# shlr/wind - LGPL v3+
# shlr/spp - MIT
# shlr/zip/zlib - zlib/libpng License (system installed shared libzip is used instead)
# shlr/zip/zip - 3 clause BSD (system installed shared zlib is used instead)
# shlr/ptrace-wrap - LGPL v3+
# shlr/tree-sitter - MIT

# Removed from the final package because of the presence of minified JS and
# absence of the source JS - this should be packaged with rizin-webui
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

%if %{!with build_release}
BuildRequires:  sed
%endif

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  file-devel
BuildRequires:  xxhash-devel
BuildRequires:  pkgconfig

%if 0%{?epel}
BuildRequires:  bzip2-devel
BuildRequires:  python3
%else
BuildRequires:  pkgconfig(bzip2)
%endif
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(capstone) >= 3.0.4
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(openssl)

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
# compiled with -D use_sys_openssl=true instead

# ./shlr/spp/README.md
# SPP stands for Simple Pre-Processor, a templating language.
# https://github.com/rizinorg/spp
Provides:       bundled(spp) = 1.2.0

# ./shlr/sdb/README.md
# sdb is a simple string key/value database based on djb's cdb
# https://github.com/rizinorg/sdb
Provides:       bundled(sdb) = 1.7.0

# ./shlr/sdb/src/json/README
# Based on js0n with a lot of modifications
# https://github.com/quartzjer/js0n
# JSON support for sdb.
Provides:       bundled(js0n)

# libr/util/regex/README
# Modified OpenBSD regex to be portable
# cvs -qd anoncvs@anoncvs.ca.openbsd.org:/cvs get -P src/lib/libc/regex
# version from 2010/11/21 00:02:30, version of files ranges from v1.11 to v1.20
Provides:       bundled(openbsdregex) = 1.11

# ./shlr/tcc/README.md
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
Provides:       bundled(grub2)

# ./shlr/ptrace-wrap
# https://github.com/thestr4ng3r/ptrace-wrap
Provides:       bundled(ptrace-wrap)

# ./shlr/tree-sitter
# https://github.com/tree-sitter/tree-sitter
Provides:	bundled(tree-sitter) = 0.19.4

%description
The rizin is a reverse-engineering framework that is multi-architecture,
multi-platform, and highly scriptable.  rizin provides a hexadecimal
editor, wrapped I/O, file system support, debugger support, diffing
between two functions or binaries, and code analysis at opcode,
basic block, and function levels.


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
%if %{with build_release}
# Build from git release version
%autosetup -n %{gitname}-%{version}
%else
# Build from git commit
%autosetup -n %{gitname}-%{commit}
# Rename internal "version-git" to "version"
sed -i -e "s|%{version}-git|%{version}|g;" configure configure.acr
%endif
# Removing zip/lzip and lz4 files because we use system dependencies
rm -rf shlr/zip shlr/lz4

# Bundled libraries
tar --strip-components=1 -C shlr/sdb -xzvf %SOURCE1
tar --strip-components=1 -C shlr/tree-sitter -xzvf %SOURCE2



%build
# Whereever possible use the system-wide libraries instead of bundles
%meson \
    -Duse_sys_magic=true \
    -Duse_sys_zip=true \
    -Duse_sys_zlib=true \
    -Duse_sys_lz4=true \
    -Duse_sys_xxhash=true \
    -Duse_sys_openssl=true \
    -Duse_libuv=true \
%ifarch s390x
    -Ddebugger=false \
%endif
    -Duse_sys_capstone=true \
    -Denable_tests=false \
    -Denable_r2r=false
%meson_build


%install
%meson_install
# install README.Fedora for the www part
mkdir -p %{buildroot}/%{_datadir}/%{name}/%{version}/www
cp ./shlr/www/README.Fedora %{buildroot}/%{_datadir}/%{name}/%{version}/www/README.Fedora
# remove unneeded fortunes
rm %{buildroot}/%{_datadir}/doc/%{name}/fortunes.fun

%ldconfig_scriptlets


%check



%files
%doc CONTRIBUTING.md DEVELOPERS.md README.md
%doc doc/3D/ doc/node.js/ doc/pdb/ doc/sandbox/
%doc doc/avr.md doc/brainfuck.md doc/calling-conventions.md doc/debug.md
%doc doc/esil.md doc/gdb.md doc/gprobe.md doc/intro.md doc/io.md doc/rap.md
%doc doc/siol.md doc/strings.md doc/windbg.md doc/yara.md
%doc %{_datadir}/doc/%{name}/fortunes.tips
%dir %{_datadir}/%{name}/%{version}/www
# Webui removed cuz of having minified js code and missing source code
%doc %{_datadir}/%{name}/%{version}/www/README.Fedora
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/libr_*.so.%{version}*
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
%dir %{_datadir}/%{name}
%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/%{name}/%{version}


%changelog
* Sun Mar 21 2021 Michal Ambroz <rebus at, seznam.cz> 0.1.2-1
- initial rizin package
