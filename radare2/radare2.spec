Name:           radare2
Summary:        The reverse engineering framework
Version:        5.1.1
URL:            https://radare.org/
VCS:            https://github.com/radare/radare2

# by default it builds from the released version of radare2
%bcond_without  build_release

%global         gituser         radareorg
%global         gitname         radare2

%global         gitdate         20210211
%global         commit          a86f8077fc148abd6443384362a3717cd4310e64
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         rel              2

%if %{with build_release}
Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{rel}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{commit}.zip
%endif

License:        LGPLv3+ and GPLv2+ and BSD and MIT and ASL 2.0 and MPLv2.0 and zlib
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
# https://github.com/radare/spp
Provides:       bundled(spp) = 1.2.0

# ./shlr/sdb/README.md
# sdb is a simple string key/value database based on djb's cdb
# https://github.com/radare/sdb
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
Provides:	bundled(tree-sitter) = 0.17.2

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
%if %{with build_release}
# Build from git release version
%setup -n %{gitname}-%{version}
%else
# Build from git commit
%setup -q -n %{gitname}-%{commit}
# Rename internal "version-git" to "version"
sed -i -e "s|%{version}-git|%{version}|g;" configure configure.acr
%endif
# Removing zip/lzip and lz4 files because we use system dependencies
rm -rf shlr/zip shlr/lz4

# Webui contains pre-build and/or minimized versions of JS libraries without source code
# Consider installing the web-interface from https://github.com/radare/radare2-webui
rm -rf ./shlr/www/*
echo "The radare2 source usually comes with a pre-built version of the web-interface, but without the source code." > ./shlr/www/README.Fedora
echo "This has been removed in the Fedora package to follow the Fedora Packaging Guidelines." >> ./shlr/www/README.Fedora
echo "Available under https://github.com/radare/radare2-webui" >> ./shlr/www/README.Fedora

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
# Do not run the testsuite yet - it pulls another package
# https://github.com/radare/radare2-regressions from github make tests



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
* Sun Feb 28 2021 Michal Ambroz <rebus at, seznam.cz> 5.1.1-2
- stop removing the r2pm binary from the package

* Mon Feb 15 2021 Henrik Nordstrom <henrik@henriknordstrom.net> - 5.1.1-1
- Rebase to upstream version 5.1.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 2 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.5.0-2.1
- Rebuilt to make sure version is no lower than F32

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.5.0-1
- Rebase to upstream version 4.5.0
* Fri May 8 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.4.0-2
- Just re-build
* Mon May 4 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.4.0-1
- Rebase to upstream version 4.4.0
* Mon Feb 3 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.2.1-1
- Rebase to upstream version 4.2.1
- Fix CVE-2019-19647
- Fix CVE-2019-19590

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Riccardo Schirone <rschirone91@gmail.com> - 3.9.0-3.1
- Fix epel7 build

* Fri Oct 04 2019 Ivan Mironov <mironov.ivan@gmail.com> - 3.9.0-2.1
- Add missing BuildRequires: xxhash-devel, openssl-devel
- Add missing Requires for -devel package: file-devel, openssl-devel

* Mon Sep 30 2019 Riccardo Schirone <rschirone91@gmail.com> - 3.9.0-1.1
- rebase to upstream version 3.9.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Riccardo Schirone <rschirone91@gmail.com> - 3.6.0
- rebase to upstream version 3.6.0
* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.4.1-2
- Rebuild with Meson fix for #1699099
- Fix versioning

* Mon Apr 8 2019 Riccardo Schirone <rschirone91@gmail.com> - 3.4.1-1
- rebase to upstream version 3.4.1
* Tue Feb 19 2019 Riccardo Schirone <rschirone91@gmail.com> - 3.3.0-2
- rebase to upstream version 3.3.0
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Riccardo Schirone <rschirone91@gmail.com> 3.2.0-2
- fix version reported by radare2 -V
* Tue Jan 8 2019 Riccardo Schirone <rschirone91@gmail.com> 3.2.0-1
- rebase to upstream version 3.2.0
- remove patch to disable debugger on s390x and use build option
- move doc files to common package
- fix CVE-2018-20455 CVE-2018-20456 CVE-2018-20457 CVE-2018-20458 CVE-2018-20459 CVE-2018-20460 CVE-2018-20461
* Fri Nov 23 2018 Riccardo Schirone <rschirone91@gmail.com> 3.1.0-1
- rebase to upstream version 3.1.0
- remove duplicated /usr/share/radare2 dir in %files
* Tue Oct 23 2018 Riccardo Schirone <rschirone91@gmail.com> 3.0.1-1
- rebase to upstream version 3.0.1 which includes some minor fixes and fixes
  for ppc64 and s390x architectures
* Tue Oct 16 2018 Riccardo Schirone <rschirone91@gmail.com> 3.0.0-2
- fix datadir dir ownership
* Tue Oct 16 2018 Riccardo Schirone <rschirone91@gmail.com> 3.0.0-1
- rebase to upstream version 3.0.0
- fixes for r_sys_breakpoint on ppc64 and s390x architectures
* Tue Sep 4 2018 Riccardo Schirone <rschirone91@gmail.com> 2.9.0-1
- use system xxhash and openssl
- bump to 2.9.0 release
- use bcond_without to choose between release build or git one
- add gcc as BuildRequires
- do not directly call ldconfig but use RPM macros
- add patch to compile on s390x architecture (disable debugger because there is no support)
- add patch to make tags.r2 file generation reproducible
- make common subpackage do not depend on arch of main package

* Fri Aug 3 2018 Riccardo Schirone <rschirone91@gmail.com> 2.8.0-0.2.20180718git51e2936
- add grub2 and xxhash Provides
- add some license comments
- move SDB files in -common subpackage

* Mon Jul 16 2018 Riccardo Schirone <rschirone91@gmail.com> 2.8.0-0.1.20180718git51e2936
- bump to 2.8.0 version and switch to meson

* Fri Apr 13 2018 Michal Ambroz <rebus at, seznam.cz> 2.5.0-1
- bump to 2.5.0 release

* Sun Feb 11 2018 Michal Ambroz <rebus at, seznam.cz> 2.4.0-1
- bump to 2.4.0 release

* Mon Feb 05 2018 Michal Ambroz <rebus at, seznam.cz> 2.3.0-1
- bump to 2.3.0 release
- drop the web-interface for now

* Tue Nov 14 2017 Michal Ambroz <rebus at, seznam.cz> 2.0.1-1
- bump to 2.0.1 release

* Fri Aug 04 2017 Michal Ambroz <rebus at, seznam.cz> 1.6.0-1
- bump to 1.6.0 release

* Thu Jun 08 2017 Michal Ambroz <rebus at, seznam.cz> 1.5.0-1
- bump to 1.5.0 release

* Sun Apr 23 2017 Michal Ambroz <rebus at, seznam.cz> 1.4.0-1
- bump to 1.4.0 release

* Sat Mar 18 2017 Michal Ambroz <rebus at, seznam.cz> 1.3.0-1
- bump to 1.3.0 release

* Sat Feb 18 2017 Michal Ambroz <rebus at, seznam.cz> 1.3.0-0.1.gita37af19
- switch to git version fixing sigseg in radiff2

* Wed Feb 08 2017 Michal Ambroz <rebus at, seznam.cz> 1.2.1-1
- bump to 1.2.1
- removed deprecated post postun calling of /sbin/ldconfig

* Sat Oct 22 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.6-1
- bump to 0.10.6

* Sun Aug 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.5-1
- bump to 0.10.5

* Mon Aug 01 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.4-1
- bump to 0.10.4

* Sun Jun 05 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.3-1
- build for Fedora for release of 0.10.3

* Mon Apr 25 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.2-1
- build for Fedora for release of 0.10.2

* Thu Jan 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.0-2
- build for Fedora for release of 0.10.0

* Sat Oct 10 2015 Michal Ambroz <rebus at, seznam.cz> 0.10.0-1
- build for Fedora for alpha of 0.10.0

* Sun Nov 09 2014 Pavel Odvody <podvody@redhat.com> 0.9.8rc3-0
- initial radare2 package
