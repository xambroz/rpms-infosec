%global         gituser         libyal
%global         gitname         libesedb
%global         commit          1fc13b4cad3c783cc5d21cdab7ce244d786cb8de
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})



Name:           libesedb
Version:        20140406
Release:        1%{?dist}
Summary:        Libyal library to access the Extensible Storage Engine (ESE) Database File (EDB) format

License:        GPLv3+
#URL:           https://github.com/libyal/libesedb
URL:            https://github.com/%{gituser}/%{gitname}
#Source0:        http://libesedb.googlecode.com/files/%{name}-alpha-%{version}.tar.gz
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/%{version}/%{gitname}-experimental-%{version}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
#Patch0:         %{name}-libs.patch

BuildRequires:  autoconf


%description
Library and tools to access the Extensible Storage Engine (ESE) Database File
(EDB) format. ESEDB is used in may different applications like Windows Search,
Windows Mail, Exchange, Active Directory, etc.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -qn %{gitname}-%{commit}
#setup -qn %{gitname}-%{version}
#patch0 -p 1 -b .libs
#./autogen.sh
autoreconf --force --install
aclocal


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING AUTHORS
%{_libdir}/*.so.*
%{_bindir}/esedbexport
%{_bindir}/esedbinfo
%{_mandir}/man1/esedbinfo.1.*
%{_mandir}/man3/libesedb.3.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libesedb.pc


%changelog
* Thu Jun 04 2015 Michal Ambroz <rebus at, seznam.cz> 20150409-1
- update to 20150409

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120102-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 06 2012 Michal Ambroz <rebus at, seznam.cz> 20120102-3
- updates based on the review of Mario Blättermann

* Sat Oct 06 2012 Michal Ambroz <rebus at, seznam.cz> 20120102-2
- updates based on the review of Mario Blättermann

* Sun May 13 2012 Michal Ambroz <rebus at, seznam.cz> 20120102-1
- initial build for Fedora
