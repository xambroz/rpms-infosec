%global         gituser         radare
%global         gitname         radare2
%global         commit          91daa516ebf44f0bc422c1f6054a1938df16e25f
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           radare2
Version:        1.5.0
#Release:       1.git%{shortcommit}%{?dist}
Release:        1%{?dist}
Summary:        The radare2 reverse engineering framework
Group:          Development/Tools

# Whole package is licensed as GPLv3+, some code has originally different license:
# shlr/grub/grubfs.c - LGPL
# shlr/java - Apache 2.0
# shlr/sdb/src - MIT
# shlr/spp - MIT
# shlr/squashfs/src - GPLv2+
# shlr/tcc - LGPLv2+
# shlr/udis86 - 2 clause BSD
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
# shlr/wind - LGPL v3+
# shlr/spp - MIT
# shlr/zip/zlib - 3 clause BSD (system installed sared zlib is used instead)


License:        GPLv3+
URL:            http://radare.org/
#URL:           https://github.com/radare/radare2
#Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

#Backport from git https://github.com/radare/radare2/commit/d9d5f79278c0413582e056850184cb5ee0767727?diff=unified
#will be in 1.4.0
Patch0:         %{name}-capstone4.patch


BuildRequires:  pkgconfig
BuildRequires:  file-devel
BuildRequires:  libzip-devel
BuildRequires:  capstone-devel >= 3.0.4


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
#setup -q -n %{gitname}-%{commit}
%setup -q -n %{gitname}-%{version}
#%patch0 -p 1 -b .capstone4


%build
%configure --with-sysmagic --with-syszip --with-syscapstone
CFLAGS="%{optflags} -fPIC -I../include" make %{?_smp_mflags} LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{_datadir}

# Do not run the testsuite yet - it pulls another package https://github.com/radare/radare2-regressions from github
# %check
# make tests


%install
NOSUDO=1 make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS.md CONTRIBUTING.md DEVELOPERS.md README.md
%doc doc/3D/ doc/node.js/ doc/pdb/ doc/sandbox/
%doc %{_datadir}/doc/%{name}
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/libr*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/last
%{_libdir}/%{name}/%{version}/*.so
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
%{_datadir}/%{name}/last
%{_datadir}/%{name}/%{version}/cons/*
%dir %{_datadir}/%{name}/%{version}/format
%{_datadir}/%{name}/%{version}/format/*
%dir %{_datadir}/%{name}/%{version}/www
%{_datadir}/%{name}/%{version}/www/*


%files devel
%{_includedir}/libr
%{_libdir}/pkgconfig/*.pc



%changelog
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
- Initial tito package

