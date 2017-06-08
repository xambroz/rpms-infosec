Name:           radare2
Version:        0.9.8
Release:        1%{?dist}
Summary:        The reverse engineering framework

License:        LGPLv3
URL:            http://radare.org/y/
#Source0:        http://radare.org/get/%{name}-%{version}.tar.gz
Source0:        http://radare.org/get/%{name}-%{version}.tar.xz

BuildRequires:  vala-devel
BuildRequires:  valabind
BuildRequires:	file-devel
BuildRequires:  libzip-devel
BuildRequires:  libewf-devel
BuildRequires:  gmp-devel
BuildRequires:  lua-devel


#Requires:       

%description
Opensource tools to disasm, debug, analyze, manipulate binary files and more...


%package devel
Summary:        Development files for radare2
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for use with  %{name}.


%prep
%setup -q


%build
%configure --with-syszip --with-sysmagic --with-openssl 
CFLAGS="%{optflags} -fPIC -I../include" make %{?_smp_mflags} LIBDIR=%{_libdir}



%install
rm -rf %{buildroot}
NOSUDO=1 make install DESTDIR=%{buildroot} LIBDIR=%{_libdir}
cp shlr/sdb/src/libsdb.a %{buildroot}/%{_libdir}/libsdb.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc %{_datadir}/doc/%{name}
%{_bindir}/r2
%{_bindir}/rabin2
%{_bindir}/r2agent
%{_bindir}/radare2
%{_bindir}/radiff2
%{_bindir}/rafind2
%{_bindir}/ragg2
%{_bindir}/ragg2-cc
%{_bindir}/rahash2
#%{_bindir}/ranal2
%{_bindir}/rarun2
%{_bindir}/rasm2
%{_bindir}/rax2
%{_libdir}/libr*
%{_libdir}/%{name}/%{version}/*.so
#%{_libdir}/%{name}/%{version}/*.py*
#%{_libdir}/%{name}/%{version}/*.lua
#%{_libdir}/%{name}/%{version}/*.rb
%{_libdir}/%{name}/%{version}/syscall
%{_libdir}/%{name}/%{version}/opcodes
%{_libdir}/%{name}/%{version}/magic
%{_mandir}/man1/r*.1.*
%dir %{_datadir}/%{name}/%{version}/www
%{_datadir}/%{name}/%{version}/www/*


%files devel
%{_includedir}/libr
%{_libdir}/libsdb.a
%{_libdir}/pkgconfig/*.pc



%changelog
* Sun Mar 11 2012 Michal Ambroz <rebus at, seznam.cz> 0.9-1
- Initial build for Fedora

