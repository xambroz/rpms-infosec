Name:           radare2
Summary:        The reverse engineering framework
Group:          Development/Tools
Version:        2.7.0
URL:            http://radare.org/
#               https://github.com/radare/radare2

%global         rel              2


%global         gituser         radare
%global         gitname         radare2
%global         gitdate         20180611
%global         commit          c52c7bace3a8a4e53baa008d05df8aee75733eee
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Build source is github release=1 or git commit=0
%global         build_release    0

%if 0%{?build_release}  > 0
Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{rel}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

License:        LGPLv3+ and GPLv2+ and BSD and MIT and ASLv2.0 and MPLv2.0
# Radare2 as a package is targeting to be licensed/compiled as LGPLv3+
# during build for Fedora the GPL code is not omitted so effectively it is GPLv2+
# some code has originally different license:
# shlr/grub/grubfs.c - LGPL
# shlr/java - Apache 2.0
# shlr/sdb/src - MIT
# shlr/spp - MIT
# shlr/squashfs/src - GPLv2+
# shlr/tcc - LGPLv2+
# shlr/udis86 - 2 clause BSD
# shlr/wind - LGPL v3+
# shlr/spp - MIT
# shlr/zip/zlib - 3 clause BSD (system installed sared zlib is used instead)

# Removed from the final package because of the presence of minified JS and
# absence of the source JS - this should be packaged with radare2-webui
# shlr/www/m - Apache-2.0
# shlr/www/enyo/vendors/jquery-ui.min.js - GPL + MIT
# shlr/www/enyo/vendors/jquery.layout-latest.min.js - GPL + MIT
# shlr/www/enyo/vendors/jquery.scrollTo.min.js - MIT
# shlr/www/enyo/vendors/lodash.min.js - lodash license
# shlr/www/enyo/vendors/joint.* - Mozilla MPL 2.0
# shlr/www/enyo/vendors/jquery.min.js - Aplache License version 2.0
# shlr/www/p/vendors/jquery* - GPL + MIT
# shlr/www/p/vendors/dagre*|graphlib* - 3 clause BSD
# shlr/www/p/vendors/jquery.onoff.min.js - MIT



BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  pkgconfig
BuildRequires:  file-devel
BuildRequires:  libzip-devel
BuildRequires:  capstone-devel >= 3.0.4

# Package contains several bundled libraries
# TODO - find versions

# ./shlr/zip/zlib/README
# compiled with --with-syszip instead

# ./libr/magic/README
# compiled with --with-sysmagic instead

# ./shlr/capstone.sh
# compiled with --with-syscapstone instead

# ./shlr/sdb/README.md
# sdb is a simple string key/value database based on djb's cdb
# https://github.com/radare/sdb
Provides:       bundled(sdb)

# ./shlr/sdb/src/json/README
# https://github.com/quartzjer/js0n
# JSON support for sdb
Provides:       bundled(js0n)

# libr/util/regex/README
# Modified OpenBSD regex to be portable
# cvs -qd anoncvs@anoncvs.ca.openbsd.org:/cvs get -P src/lib/libc/regex
# version from 2010/11/21 00:02:30
Provides:       bundled(openbsdregex)

# ./shlr/tcc/README.md
# This is a stripped down version of tcc without the code generators.
Provides:       bundled(tcc)

# ./shlr/lz4/README.md
Provides:       bundled(lz4)

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




%description
The radare2 is a reverse-engineering framework that is multi-architecture,
multi-platform, and highly scriptable.  Radare2 provides a hexadecimal
editor, wrapped I/O, file system support, debugger support, diffing
between two functions or binaries, and code analysis at opcode,
basic block, and function levels.


%package devel
Summary:        Development files for the %{name} package
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the %{name} package. See %{name} package for more
information.


%prep
%if 0%{?build_release} > 0
# Build from git release version
%setup -q -n %{gitname}-%{version}

%else
# Build from git commit
%setup -q -n %{gitname}-%{commit}
# Rename internatl "version-git" to "version"
sed -i -e "s|%{version}-git|%{version}|g;" configure configure.acr
%endif

# Webui contains pre-build and/or minimized versions of JS libraries without source code
# Consider installing the web-interface from https://github.com/radare/radare2-webui
rm -rf ./shlr/www/*
echo "The radare2 source usually comes with a pre-built version of the web-interface, but without the source code" >    ./shlr/www/README.Fedora
echo "This has been removed in the Fedora package to follow the Fedora Packaging Guidelines." >> ./shlr/www/README.Fedora
echo "Available under https://github.com/radare/radare2-webui" >>                        ./shlr/www/README.Fedora


%build
# Options based on the sys/user.sh and sys/install.sh
# Whereever possible use the system-wide libraries instead of bundles
# with-openssl option is not used, because it is obsoleted and not used in the code
%configure --with-sysmagic --with-syszip --with-syscapstone

# Link binaries to the SO name with version
# HAVE_LIBVERSION=1

CFLAGS="%{optflags} -fPIC -I../include" %make_build \
    LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{_datadir} HAVE_LIBVERSION=1

%check
# Do not run the testsuite yet - it pulls another package https://github.com/radare/radare2-regressions from github
# make tests


%install
NOSUDO=1 make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}

# *.a files not allowed for fedora
find %{buildroot} -name '*.a' -delete


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS.md CONTRIBUTING.md DEVELOPERS.md README.md
%doc doc/3D/ doc/node.js/ doc/pdb/ doc/sandbox/

# Webui removed cuz of having minified js code and missing source code
%doc %{_datadir}/%{name}/%{version}/www/README.Fedora
%doc %{_datadir}/doc/%{name}
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/libr*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/last
%{_mandir}/man1/r*.1.*
%{_mandir}/man7/esil.7.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%dir %{_datadir}/%{name}/%{version}/cons
%dir %{_datadir}/%{name}/%{version}/fcnsign
%{_datadir}/%{name}/%{version}/fcnsign/*.sdb
%dir %{_datadir}/%{name}/%{version}/hud
%{_datadir}/%{name}/%{version}/hud/*
%dir %{_datadir}/%{name}/%{version}/magic
%{_datadir}/%{name}/%{version}/magic/*
%dir %{_datadir}/%{name}/%{version}/opcodes
%{_datadir}/%{name}/%{version}/opcodes/*.sdb
%dir %{_datadir}/%{name}/%{version}/syscall
%{_datadir}/%{name}/%{version}/syscall/*.sdb
%dir %{_datadir}/%{name}/%{version}/flag
%{_datadir}/%{name}/%{version}/flag/*.r2
%{_datadir}/%{name}/last
%{_datadir}/%{name}/%{version}/cons/*
%dir %{_datadir}/%{name}/%{version}/format
%{_datadir}/%{name}/%{version}/format/*


# TODO - no modules built since 2018
# %{_libdir}/%{name}/%{version}/*.so



%files devel
%{_includedir}/libr
%{_libdir}/libr*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Jul 13 2020 Michal Ambroz <rebus at, seznam.cz> 4.4.0-10.20200713gitc52c7ba

* Fri Jun 08 2018 Michal Ambroz <rebus at, seznam.cz> 2.7.0-0.2.20180611gitc52c7ba
- bump to 2.7.0 c52c7bace3a8a4e53baa008d05df8aee75733eee
- fixes https://github.com/radare/radare2/issues/10300

* Fri Jun 08 2018 Michal Ambroz <rebus at, seznam.cz> 2.7.0-0.1.20180608git555e88a
- bump to 2.7.0 alpha release

* Fri Jun 08 2018 Michal Ambroz <rebus at, seznam.cz> 2.6.0-1
- bump to 2.6.0 release - failed to link capstone and zip

* Mon Apr 09 2018 Michal Ambroz <rebus at, seznam.cz> 2.5.0-1
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

