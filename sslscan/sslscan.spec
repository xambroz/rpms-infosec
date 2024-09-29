Name:           sslscan
Version:        2.1.5
Release:        %autorelease
Summary:        Security assessment tool for SSL/TLS

# Special exception to allow linking against the OpenSSL libraries
# Automatically converted from old format: GPLv3+ with exceptions - review is highly recommended.
License:        LicenseRef-Callaway-GPLv3+-with-exceptions

# rbsec sslscan fork
URL:            https://github.com/rbsec/sslscan/
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://www.openssl.org/source/openssl-1.1.1g.tar.gz
Patch0:         Makefile-override-CFLAGS.patch
Patch1:         Makefile-disable-opensslpull.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

%description
SSLScan queries SSL services, such as HTTPS, in order to determine the ciphers
that are supported. SSLScan is designed to be easy, lean and fast. 
The output includes preferred ciphers of the SSL service, the certificate
and is in text and XML formats.

%prep
%autosetup -n %{name}-%{version}
mkdir openssl
cd openssl
tar xvf %{SOURCE1} --strip-components=1

%build
make %{?_smp_mflags} CFLAGS="%{optflags}" static

%install
make install DESTDIR=%{buildroot} BINPATH=%{_bindir}/ MANPATH=%{_mandir}/

%files
%doc Changelog README.md TODO
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
