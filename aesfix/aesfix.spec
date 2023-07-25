Name:           aesfix
Version:        1.0.1
Release:        3%{?dist}
# 3-clause BSD license
License:        BSD-3-Clause
Summary:        Correct bit errors in AES-128 key schedule

URL:            https://citp.princeton.edu/our-work/memory/
# Current code: https://citp.princeton.edu/our-work/memory/code
# Original URL: https://citp.princeton.edu/research/memory/
# Mirror        https://github.com/DonnchaC/coldboot-attacks

#               https://citpsite.s3.amazonaws.com/memory-content/src/aesfix-1.0.1.tar.gz
# Original      https://citp.princeton.edu/memory-content/src/aesfix-1.0.1.tar.gz
#               https://web.archive.org/web/20160501132651/https://citp.princeton.edu/memory-content/src/aesfix-1.0.1.tar.gz
#               http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%%{name}-%%{version}.tar.gz
Source0:        https://citpsite.s3.amazonaws.com/memory-content/src/%{name}-%{version}.tar.gz

#               https://citpsite.s3.amazonaws.com/memory-content/src/aesfix-1.0.1.tar.gz.asc
#               https://web.archive.org/web/20160501132651/https://citp.princeton.edu/memory-content/src/aesfix-1.0.1.tar.gz.asc
#               http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%%{name}-%%{version}.tar.gz.asc
Source1:        https://citpsite.s3.amazonaws.com/memory-content/src/%{name}-%{version}.tar.gz.asc

# The authenticator public key obtained from release 1.0.1
# gpg2 -vv aeskeyfind-1.0.1.tar.gz.asc
# Signed by Jacob Appelbaum <jacob () appelbaum net>
# gpg2 --search-key B8841A919D0FACE4
# gpg2 --search-key 12E404FFD3C931F934052D06B8841A919D0FACE4
# gpg2 --list-public-keys 12E404FFD3C931F934052D06B8841A919D0FACE4
# gpg2 --export --export-options export-minimal 12E404FFD3C931F934052D06B8841A919D0FACE4 > gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg
Source2:        gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg

# Manual page from Debian
Source3:        aesfix.1

# Original Debian patch to allow build hardening by usage of CFLAGS and LDFLAGS
# Author: Joao Eriberto Mota Filho <eriberto@debian.org>
Patch1:         aesfix-10_add-GCC-hardening.patch


Buildrequires:  gcc-c++
Buildrequires:  make
BuildRequires:  gnupg2


%description
The aesfix tool illustrates a technique for correcting bit errors in an
AES key schedule. This program is limited to AES-128 key schedules
and it can only correct unidirectional 1->0 bit errors.
For the most part it has been optimized for readability rather than
performance.


%prep
#check signature
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{name}


%build
%set_build_flags
%make_build


%install
install -Dp -m755 %{name} %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{_mandir}/man1
install -p -m644 %{SOURCE3} %{buildroot}%{_mandir}/man1


%files
%license LICENSE
%doc README samples
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Tue Jul 25 2023 Michal Ambroz <rebus at, seznam.cz> - 1.0.1-3
- switch to SPDX license reference - BSD-3-Clause

* Fri Feb 28 2020 Michal Ambroz <rebus at, seznam.cz> - 1.0.1-2
- uppercase the summary

* Fri Feb 28 2020 Michal Ambroz <rebus at, seznam.cz> - 1.0.1-1
- package based on the aeskeyfind

