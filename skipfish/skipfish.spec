Name:           skipfish
Epoch:          2
Version:        2.10
Release:        %autorelease -p -e b
Summary:        Web application security scanner


# Whole package licensed with ASL 2.0 license except 
# string-inl.h which has BSD type license
# icons which are licensed under LGPLv3
License:        ASL 2.0 and BSD and LGPLv3

URL:            http://code.google.com/p/skipfish/
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/skipfish/%{name}-%{version}b.tgz
# was:          http://%%{name}.googlecode.com/files/%%{name}-%%{version}b.tgz

# Use common paths and fedora build options and use fedora policy compiler flag
Patch01:         skipfish-01-makefile-format-security.patch

# Patch to build with GCC10 where -fno-common is the default
# overlaps with skipfish-03-fix-for-openssl-1.1.patch
# Patch02:         skipfish-02-gcc10.patch

# Patches from Debian/Kali linux
# https://gitlab.com/kalilinux/packages/skipfish/-/tree/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches

# From:         Igor Bezzubchenko <garikello@gmail.com>
# Date:         Sun, 3 Jan 2021 22:49:21 +0300
# Subject:      Fix for openssl 1.1
# Origin:       https://gitlab.com/kalilinux/packages/skipfish/-/merge_requests/1
Patch3:         https://gitlab.com/kalilinux/packages/skipfish/-/raw/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches/Fix-for-openssl-1.1.patch#/skipfish-03-fix-for-openssl-1.1.patch

# From: Sophie Brun <sophie@offensive-security.com>
# Date: Wed, 6 Jan 2021 15:31:58 +0100
# Subject: Fix small syntax issues in manpage
Patch4:         https://gitlab.com/kalilinux/packages/skipfish/-/raw/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches/Fix-small-syntax-issues-in-manpage.patch#/skipfish-04-fix-small-sytax-issues-in-manpage.patch

# From 21a6780ce8b5a17ffe2b17eda2abf5ca60fd6f46 Mon Sep 17 00:00:00 2001
# From: Igor Bezzubchenko <garikello@gmail.com>
# Date: Thu, 7 Jan 2021 14:21:32 +0300
# Subject: [PATCH] fixing broken ciphersuite evaluation for newer OpenSSLs
Patch5:         https://gitlab.com/kalilinux/packages/skipfish/-/raw/0f290396a860634cb16848f23bca36a9ba8209bb/debian/patches/Fix-broken-ciphersuite-evaluation-for-newer-OpenSSLs.patch#/skipfish-05-fix-broken-ciphersuite-evaluation-for-newer-OpenSSLs.patch

# Replace obsolete gethostbyname with getaddrinfo as suggested by rpmlint
Patch6:         skipfish-06-gethostbyname.patch




BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  libidn-devel
BuildRequires:  make
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel

%description
High-performance, easy, and sophisticated Web application security testing
tool. It features a single-threaded multiplexing HTTP stack, heuristic 
detection of obscure Web frameworks, and advanced, differential security
checks capable of detecting blind injection vulnerabilities, stored XSS,
and so forth.

%prep
%autosetup -p 1 -n %{name}-%{version}b
cp -p assets/COPYING COPYING.icons


%build
sed -i 's|^// #define PROXY_SUPPORT|#define PROXY_SUPPORT|' src/config.h
%make_build CFLAGS="%{optflags} -fno-common"



%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_datadir}/%{name}/assets/COPYING
rm -f doc/skipfish.1


%files
%doc COPYING ChangeLog README 
%doc doc/
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/assets
%dir %{_datadir}/%{name}/dictionaries
%dir %{_datadir}/%{name}/signatures
%{_datadir}/%{name}/dictionaries/*
%{_datadir}/%{name}/signatures/*
%{_datadir}/%{name}/assets/index.html
%{_bindir}/%{name}
%{_bindir}/sfscandiff
%{_mandir}/man1/%{name}.1*



#Icons are licensed as LGPLv3 http://www.everaldo.com/crystal/
%doc COPYING.icons
%{_datadir}/%{name}/assets/*.png


%changelog
%autochangelog
