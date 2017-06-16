Name:           radare
Version:        1.5.2
Release:        1%{?dist}
Summary:        The reverse engineering framework

License:        LGPLv3
URL:            http://radare.org/y/
Source0:        http://radare.org/get/%{name}-%{version}.tar.gz
Patch0:         radare-fedora17.patch

BuildRequires:  vala-devel
BuildRequires:	file-devel
BuildRequires:  libewf-devel
BuildRequires:  gmp-devel
BuildRequires:  lua-devel
BuildRequires:  libusb-devel
BuildRequires:  gtk2-devel
BuildRequires:  vte-devel


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
%patch0 -b .fc17 -p 1


%build
%configure
make %{?_smp_mflags}



%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc %{_datadir}/doc/%{name}
%dir %{_libdir}/python2.7/site-packages/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%dir %{_libdir}/ruby/1.8/%{name}
#%dir %{_libexec}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/gradare
%dir %{_datadir}/%{name}/gradare/Config
%dir %{_datadir}/%{name}/gradare/Debugger
%dir %{_datadir}/%{name}/gradare/Disassembly
%dir %{_datadir}/%{name}/gradare/Flags
%dir %{_datadir}/%{name}/gradare/Hacks
%dir %{_datadir}/%{name}/gradare/Movement
%dir %{_datadir}/%{name}/gradare/Shell
%dir %{_datadir}/%{name}/gradare/Visual
%{_bindir}/gradare
%{_bindir}/rabin
%{_bindir}/radare
%{_bindir}/radiff
%{_bindir}/rahash
%{_bindir}/rasc
%{_bindir}/rasm
%{_bindir}/rax
%{_bindir}/rfile
%{_bindir}/rsc
%{_bindir}/xrefs
%{_libdir}/libfdsniff.so
%{_libdir}/libusbsniff.so
%{_libdir}/python2.7/site-packages/%{name}/*.py*
%{_libdir}/ruby/1.8/%{name}/*.rb
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.lua
%{_libdir}/%{name}/bin/*
%{_datadir}/%{name}/*
%{_mandir}/man1/r*.1.*
%{_mandir}/man1/gr*.1.*
%{_mandir}/man1/xrefs.1.*
%{_mandir}/man5/r*.5.*



%changelog
* Sun May 13 2012 Michal Ambroz <rebus at, seznam.cz> 1.5.2-1
- Initial build for Fedora

