Name:           rsakeyfind
Version:        1.0
Release:        1%{?dist}
# 3-clause BSD license
License:        BSD
Summary:        Locate BER-encoded RSA private and public keys in memory images

URL:            https://citp.princeton.edu/our-work/memory/
# Current code: https://citp.princeton.edu/our-work/memory/code
# Original URL: https://citp.princeton.edu/research/memory/
# Mirror        https://github.com/DonnchaC/coldboot-attacks

#               https://citpsite.s3.amazonaws.com/memory-content/src/rsakeyfind-1.0.tar.gz
# Original      https://citp.princeton.edu/memory-content/src/rsakeyfind-1.0.tar.gz
#               https://web.archive.org/web/20160501132651/https://citp.princeton.edu/memory-content/src/rsakeyfind-1.0.tar.gz
#               http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%%{name}-%%{version}.tar.gz
Source0:        https://citpsite.s3.amazonaws.com/memory-content/src/%{name}-%{version}.tar.gz

#               https://citpsite.s3.amazonaws.com/memory-content/src/rsakeyfind-1.0.tar.gz.asc
#               https://web.archive.org/web/20160501132651/https://citp.princeton.edu/memory-content/src/rsakeyfind-1.0.tar.gz.asc
#               http://citpsite.s3-website-us-east-1.amazonaws.com/oldsite-htdocs/memory-content/src/%%{name}-%%{version}.tar.gz.asc
Source1:        https://citpsite.s3.amazonaws.com/memory-content/src/%{name}-%{version}.tar.gz.asc

# The authenticator public key obtained from aeskeyfind release 1.0
# gpg2 -vv aeskeyfind-1.0.tar.gz.asc
# Signed by Jacob Appelbaum <jacob () appelbaum net>
# gpg2 --search-key B8841A919D0FACE4
# gpg2 --search-key 12E404FFD3C931F934052D06B8841A919D0FACE4
# gpg2 --list-public-keys 12E404FFD3C931F934052D06B8841A919D0FACE4
# gpg2 --export --export-options export-minimal 12E404FFD3C931F934052D06B8841A919D0FACE4 > gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg
Source2:        gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg

# Manual page from Debian
Source3:        rsakeyfind.1

# Honor the CXXFLAGS environment settings for the standard hardening/optimalization
Patch1:         rsakeyfind-10_add-GCC-hardening.patch

# Fix missing includes
Patch2:         rsakeyfind-20_includes.patch


Buildrequires:  gcc
Buildrequires:  make
BuildRequires:  gnupg2



%description
The rsakeyfind tool locates BER-encoded RSA private and public keys in 
captured memory images. It can either try to locate keys based on a provided
hex-dump of a modulus of a known public key, or based on fixed pattern in
BER-encoded RSA version field.


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
%doc README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Feb 28 2020 Michal Ambroz <rebus at, seznam.cz> - 1.0-1
- package based on the aeskeyfind

