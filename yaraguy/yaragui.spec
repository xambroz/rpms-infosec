%global         gituser         sigint9
%global         gitname         yaragui
%global         commit          86533d833d162d804659cd8ef1d49742f7176909
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           yaragui
Version:        3.5.0
Release:        1.%{shortcommit}%{?dist}
Summary:        This is a GUI for the YARA pattern matching scanner
#Group needed for EPEL packages
Group:          Applications/Engineering
License:        Unknown
URL:            https://github.com/pombredanne/yaragui
# Was           https://github.com/sigint9/yaragui
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz


BuildRequires:  gcc
BuildRequires:  boost-devel
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel


%description
The %{name} is Qt5 gui making patter yara development and execution 
easier and to visualize results.


%prep
%setup -q -n %{gitname}-%{commit}


%build
CFLAGS="%{optflags}" cmake .
CFLAGS="%{optflags}" make %{?_smp_mflags} LIBDIR=%{_libdir} PREFIX=%{_prefix} DATADIR=%{_datadir} LDFLAGS="%{__global_ldflags}"


%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}
find %{buildroot} -name '*.a' -delete


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS README.md TODO
%license COPYING
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}*.1.*



%changelog
* Mon Jan 09 2017 Michal Ambroz <rebus at, seznam.cz> 3.5.0-1
- initial build for Fedora


