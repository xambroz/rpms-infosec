Name:           aeskeyfind
Version:        1.0
Release:        10%{?dist}
# 3-clause BSD license
License:        BSD
Summary:        Locate 128-bit and 256-bit AES keys in a captured memory image


# Original URL: https://citp.princeton.edu/research/memory/
# https://citp.princeton.edu/our-work/memory/
# https://citp.princeton.edu/our-work/memory/code
URL:            https://citp.princeton.edu/our-work/memory/
# New mirror on github
# Mirror        https://github.com/DonnchaC/coldboot-attacks
# Fork          https://github.com/makomk/aeskeyfind

#               https://citp.princeton.edu/memory-content/src/aeskeyfind-1.0.tar.gz
#               https://web.archive.org/web/20160501132651/https://citp.princeton.edu/memory-content/src/aeskeyfind-1.0.tar.gz
#               http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%%{name}-%%{version}.tar.gz
Source0:        http://citpsite.s3-website-us-east-1.amazonaws.com/memory-content/src/%{name}-%{version}.tar.gz

#               https://web.archive.org/web/20160501132651/https://citp.princeton.edu/memory-content/src/aeskeyfind-1.0.tar.gz.asc
#               http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%%{name}-%%{version}.tar.gz.asc
Source1:        http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%{name}-%{version}.tar.gz.asc

# The authenticator public key obtained from release 1.0
# gpg2 -vv aeskeyfind-1.0.tar.gz.asc
# Signed by Jacob Appelbaum <jacob () appelbaum net>
# gpg2 --search-key B8841A919D0FACE4
# gpg2 --search-key 12E404FFD3C931F934052D06B8841A919D0FACE4
# gpg2 --list-public-keys 12E404FFD3C931F934052D06B8841A919D0FACE4
# gpg2 --export --export-options export-minimal 12E404FFD3C931F934052D06B8841A919D0FACE4 > gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg
Source2:        gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg

# Manual page from Debian
Source3:        aeskeyfind.1

# Original Debian patch to allow build hardening by usage of CFLAGS and LDFLAGS
# Author: Joao Eriberto Mota Filho <eriberto@debian.org>
Patch1:         aeskeyfind-10_add-GCC-hardening.patch

# Original Debian patch to fix the size of the sbox
# Author: Samuel Henrique <samueloph@gmail.com>
Patch2:         aeskeyfind-20_sbox-size.patch

Buildrequires:  gcc
Buildrequires:  make
BuildRequires:  gnupg2



%description
This program illustrates automatic techniques for locating 128-bit and
256-bit AES keys in a captured memory image.

The program uses various algorithms and also performs a simple entropy
test to filter out blocks that are not keys. It counts the number of
repeated bytes and skips blocks that have too many repeats.

This method works even if several bits of the key schedule have been
corrupted due to memory decay.

This package is useful to several activities, as forensics investigations.


%prep
#check signature
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{name}


%build
%set_build_flags
%make_build %{?_smp_mflags}


%install
install -Dp -m755 %{name} %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{_mandir}/man1
install -p -m644 %{SOURCE3} %{buildroot}%{_mandir}/man1


%files
%license LICENSE
%doc README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 10 2020 Michal Ambroz <rebus at, seznam.cz> - 1.0-7
- cosmetic changes in the signature verification

* Sun Oct 20 2019 Michal Ambroz <rebus at, seznam.cz> - 1.0-6
- check the signatures, fix man permission, comment patch

* Mon Apr 01 2019 Michal Ambroz <rebus at, seznam.cz> - 1.0-5
- package based on the cert.ord package by Lawrence R. Rogers (lrr@cert.org)

