Name:           hcxtools
Version:        6.2.7
Release:        1%{?dist}
Summary:        Portable solution for capturing wlan traffic and conversion to hashcat formats
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/ZerBea/hcxtools


%global         gituser         ZerBea
%global         gitname         hcxtools

# Commit of version 6.2.7
%global         gitdate         20220426
%global         commit          23b1fb3bafc2fe1c558f22b7aa031a9b57b1d532
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
Portable solution for capturing wlan traffic and conversion to hashcat formats
(recommended by hashcat) and to John the Ripper formats. hcx: 
h = hash, c = capture, convert and calculate candidates, x = different hashtypes
Small set of tools convert packets from captures 
(h = hash, c = capture, convert and calculate candidates, x = different hashtypes)
for the use with latest hashcat or John the Ripper. The tools are 100% compatible
to hashcat and John the Ripper and recommended by hashcat. 
This branch is pretty closely synced to hashcat git branch 
(that means: latest hcxtools matching on latest hashcat beta)
and John the Ripper git branch ("bleeding-jumbo").
Support for hashcat hash-modes:
    2500, 2501, 4800, 5500, 12000, 16100, 16800, 16801
Support for John the Ripper hash-modes:
    WPAPSK-PMK, PBKDF2-HMAC-SHA1, chap, netntlm, tacacs-plus
After capturing, upload the "uncleaned" cap here 
(https://wpa-sec.stanev.org/?submit) to see if your ap or the client is
vulnerable by using common wordlists. Convert the cap to hccapx and/or
to WPA-PMKID-PBKDF2 hashline (16800) and check if wlan-key or
plainmasterkey was transmitted unencrypted.



%prep
# setup -qn %{gitname}-%{commit}
%autosetup 

# Do not run build twice when invoking install
sed -i -e 's|install: build|install:|g' Makefile


%build
%make_build PREFIX=%{_prefix} CFLAGS="%{optflags}" 


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} CFLAGS="%{optflags}" 
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -D -m 0755 -p man/hcxtools.1 %{buildroot}%{_mandir}/man1/hcxtools.1
# Remove static libraries
# rm %{buildroot}%{_libdir}/lib%{name}.la
# rm %{buildroot}%{_libdir}/lib%{name}.a



%files
%doc README.md
%license license.txt
%{_bindir}/hcx*
%{_bindir}/whoismac
%{_bindir}/wlancap2wpasec
%{_mandir}/man1/hcxtools.1*



%changelog
* Thu Jan 26 2023 Michal Ambroz <rebus at, seznam.cz> - 6.2.7-1
- update to 6.2.7

* Tue Aug 7 2018 Michal Ambroz <rebus at, seznam.cz> - 4.2.1-1
- initial package
