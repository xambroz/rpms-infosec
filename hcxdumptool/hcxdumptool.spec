Name:           hcxdumptool
Version:        4.2.1
Release:        1%{?dist}
Summary:        Small tool to capture packets from wlan devices.
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/ZerBea/hcxdumptool


%global         gituser         ZerBea
%global         gitname         hcxdumptool

# Commit of version 4.2.1
%global         commit          ee3f2ed606602ead948865aed6aecc7bae993701
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Build from git release version
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  libpcap-devel



%description
Small tool to capture packets from wlan devices. 
Convert the cap to hccapx and/or to WPA-PMKID-PBKDF2 hashline (16800) with
hcxpcaptool (hcxtools) and check if wlan-key or plainmasterkey was transmitted
unencrypted.


%prep
# setup -qn %{gitname}-%{commit}
%autosetup 

# Do not run build twice when invoking install
sed -i -e 's|install: build|install:|g' Makefile


%build
make %{?_smp_mflags} PREFIX=%{_prefix} CFLAGS="%{optflags}" 


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} CFLAGS="%{optflags}" 

# Remove static libraries
# rm %{buildroot}%{_libdir}/lib%{name}.la
# rm %{buildroot}%{_libdir}/lib%{name}.a



%files
%doc README.md
%license license.txt
%{_bindir}/hcxdumptool


%changelog
* Tue Aug 7 2018 Michal Ambroz <rebus at, seznam.cz> - 4.2.1-1
- initial package
