Name:           sdb
Version:        1.9.6
Summary:        The string database from radare reverse engineering framework
#Group needed for EPEL packages
Group:          Applications/Engineering
License:        MIT
URL:            https://github.com/radareorg/sdb/
%global         baserelease     3

# by default it builds from the released version of sdb
%bcond_with     release

# as python binding is not built anymore, vala is not needed
%bcond_with     vala


%global         gituser         radareorg
%global         gitname         sdb

%global         gitdate         20230217
%global         commit          aca75fc9e610db4cf31b1b3d2dcff9edcb03b5f2
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%if %{with release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  glib2-devel
%if %{with vala}
BuildRequires:  vala
%endif

#Needed for check
BuildRequires:  leveldb-devel
BuildRequires:  time

%if %{with vala}
#binding python
#BuildRequires:  valabind
%endif

#binding nodejs
#BuildRequires:  v8-devel
#BuildRequires:  nodejs-devel


%description
The sdb is a simple string key/value database based on djb's cdb disk
storage and supports JSON and arrays introspection.
There's also the sdbtypes: a vala library that implements several data
structures on top of an sdb.


%package devel
Summary:        Development files for the %{name} package
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the %{name} package. See %{name} package for more
information.


%prep
%if %{with release}
# Build from git release version
%autosetup -n %{gitname}-%{version}
%else
# Build from git commit
%autosetup -n %{gitname}-%{commit}
# Rename internal "version-git" to "version"
# sed -i -e "s|%{version}-git|%{version}|g;" configure.acr
%endif


%build
%set_build_flags
%if %{with vala}
%make_build LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{_datadir} LDFLAGS="%{__global_ldflags}" HAVE_VALA=1
%else
%make_build LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{_datadir} LDFLAGS="%{__global_ldflags}" HAVE_VALA=
%endif


%install
%if %{with vala}
# make install DESTDIR=%%{buildroot} LIBDIR=%%{_libdir} PREFIX=%%{_prefix}
%make_install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix} HAVE_VALA=1
%else
%make_install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix} HAVE_VALA=
%endif
find %{buildroot} -name '*.a' -delete


%check
%if %{with vala}
make test HAVE_VALA=1
%else
make test HAVE_VALA=
%endif


%ldconfig_scriptlets


%files
%doc AUTHORS README.md TODO
%license COPYING
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}*.1.*


%files devel
%dir %{_includedir}/sdb
%{_includedir}/sdb/*
%{_libdir}/libsdb.so
%{_libdir}/pkgconfig/*.pc
%if %{with vala}
%{_datadir}/vala/vapi/%{name}.vapi
%{_datadir}/vala/vapi/%{name}types.vapi
%endif

%changelog
* Sun Feb 19 2023 Michal Ambroz <rebus at, seznam.cz> 1.9.6-1
- bump to 1.9.6

* Wed Apr 14 2021 Michal Ambroz <rebus at, seznam.cz> 1.7.0-1
- bump to 1.7.0

* Sat Oct 22 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.6-1.a4eab7b
- bump to 0.10.6

* Mon Sep 12 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.5-3.bf6575a
- improve buildrequires, move vapi to devel subpackage

* Sun Aug 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.5-2.bf6575a
- drop ldconfig for sdb-devel package

* Sun Aug 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.5-1.bf6575a
- bump to git state relevant to radare2 version 0.10.5

* Sun Oct 11 2015 Michal Ambroz <rebus at, seznam.cz> 0.9.8-1.0e133f1
- initial build for Fedora for alpha of 0.9.8

