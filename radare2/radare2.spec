%global         gituser         radare
%global         gitname         radare2
#global         commit          a093958b6d24015d82782eb20a2e10d8f4afcd85
#global        commit          5a3dab0a86e1452c0bb0c13d869f95b41f50b9a9
%global         commit          9c39df6806b09306ebb102b1c41de8367ac1a7c9
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           radare2
Version:        0.10.0
Release:        2%{?dist}
Summary:        The %{name} reverse engineering framework
Group:          Applications/Engineering
License:        LGPLv3
URL:            http://radare.org/
#Source0:        http://radare.org/get/\{name}-\{version}.tar.gz
#Source0:        http://radare.org/get/\{name}-\{version}.tar.xz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz


BuildRequires:  file-devel
BuildRequires:  libzip-devel
#BuildRequires:  capstone-devel >= 3.0.4


%description
The %{name} is a reverse-engineering framework that is multi-architecture,
multi-platform, and highly scriptable.  %{name} provides a hexadecimal
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
#%setup -q -n %{name}-%{version}
%setup -q -n %{gitname}-%{commit}


%build
%configure --with-sysmagic --with-syszip #--with-syscapstone
CFLAGS="%{optflags} -fPIC -I../include" make %{?_smp_mflags} LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{DATADIR}

# Do not run the testsuite yet
# %check
# make tests


%install
rm -rf %{buildroot}
NOSUDO=1 make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}
cp shlr/sdb/src/libsdb.a %{buildroot}/%{_libdir}/libsdb.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS.md CONTRIBUTING.md DEVELOPERS.md README.md TODO.md doc/*
%license COPYING
%{_bindir}/r*
%{_libdir}/libr*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/last
%{_libdir}/%{name}/%{version}/*.so
%dir %{_libdir}/%{name}/%{version}/fcnsign
%{_libdir}/%{name}/%{version}/fcnsign/*.sdb
%dir %{_libdir}/%{name}/%{version}/hud
%{_libdir}/%{name}/%{version}/hud/*
%dir %{_libdir}/%{name}/%{version}/magic
%{_libdir}/%{name}/%{version}/magic/*
%dir %{_libdir}/%{name}/%{version}/opcodes
%{_libdir}/%{name}/%{version}/opcodes/*.sdb
%dir %{_libdir}/%{name}/%{version}/syscall
%{_libdir}/%{name}/%{version}/syscall/*.sdb
%{_mandir}/man1/r*.1.*
%{_mandir}/man7/esil.7.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%dir %{_datadir}/%{name}/%{version}/cons
%{_datadir}/%{name}/last
%{_datadir}/%{name}/%{version}/cons/*
%dir %{_datadir}/%{name}/%{version}/format
%{_datadir}/%{name}/%{version}/format/*
%dir %{_datadir}/%{name}/%{version}/r2pm
%{_datadir}/%{name}/%{version}/r2pm/*
%dir %{_datadir}/%{name}/%{version}/www
%{_datadir}/%{name}/%{version}/www/*


%files devel
%{_includedir}/libr
%{_libdir}/libsdb.a
%{_libdir}/pkgconfig/*.pc

%post -n %{name}-devel -p /sbin/ldconfig
%postun -n %{name}-devel -p /sbin/ldconfig


%changelog
* Thu Jan 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.0-2
- build for Fedora for release of 0.10.0

* Sat Oct 10 2015 Michal Ambroz <rebus at, seznam.cz> 0.10.0-1
- build for Fedora for alpha of 0.10.0

* Sun Nov 09 2014 Pavel Odvody <podvody@redhat.com> 0.9.8rc3-0
- Initial tito package

