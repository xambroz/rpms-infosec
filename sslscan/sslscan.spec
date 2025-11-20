Name:           sslscan
Version:        2.2.0
%global         bundled_openssl_version    3.5.4
Release:        %autorelease
Summary:        Security assessment tool for SSL/TLS

# Special exception to allow linking against the OpenSSL libraries
# Automatically converted from old format: GPLv3+ with exceptions - review is highly recommended.
License:        LicenseRef-Callaway-GPLv3+-with-exceptions

# By default build with bundled openssl, with explicitly enabled weak ciphers
# use --without bundled_openssl to override and build with system openssl
%bcond_without     bundled_openssl

# rbsec sslscan fork
URL:            https://github.com/rbsec/sslscan/
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Source1:        https://www.openssl.org/source/openssl-%{bundled_openssl_version}.tar.gz
Patch0:         sslscan-override-CFLAGS.patch
Patch1:         sslscan-disable-opensslpull.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

%if %{with bundled_openssl}
# Bundled openssl is used to explicitly enable weak ciphers for the purpose of the scan
Provides: bundled(openssl) = %{bundled_openssl_version}
%endif

%description
SSLScan queries SSL services, such as HTTPS, in order to determine the ciphers
that are supported. SSLScan is designed to be easy, lean and fast. 
The output includes preferred ciphers of the SSL service, the certificate
and is in text and XML formats.

%prep
%autosetup -n %{name}-%{version}

%if %{with bundled_openssl}
mkdir openssl
cd openssl
tar xvf %{SOURCE1} --strip-components=1
%endif

%build
%if %{with bundled_openssl}
make %{?_smp_mflags} CFLAGS="%{optflags}" static
%else
make %{?_smp_mflags} CFLAGS="%{optflags}"
%endif

%install
make install DESTDIR=%{buildroot} BINPATH=%{_bindir}/ MANPATH=%{_mandir}/

%files
%doc Changelog README.md INSTALL
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
