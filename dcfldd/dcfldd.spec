Name:           dcfldd
Version:        1.9.2
Release:        %autorelease
Summary:        Improved dd, useful for forensics and security

#Whole dcfldd is licensed as GPLv2+
#sha1.c sha1.h BSD Type license - Allan Saddi <allan@saddi.com>
#sha2.c sha2.h BSD Type license - Aaron D. Gifford <me@aarongifford.com>
#md5.c Copyright RSA
# Note that we are using the RSA MD5 code without license.
# See: https://fedoraproject.org/wiki/Licensing:FAQ#MD5
# Automatically converted from old format: GPLv2+ and BSD and Copyright only - review is highly recommended.
License:        GPL-2.0-or-later AND LicenseRef-Callaway-BSD AND LicenseRef-Callaway-Copyright-only

URL:            https://github.com/resurrecting-open-source-projects/dcfldd
# Was           http://dcfldd.sourceforge.net/
VCS:            git:%{url}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Was           http://downloads.sourceforge.net/%%{name}/%%{name}-%%{real_version}.tar.gz


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf


%description
dcfldd is an enhanced version of GNU dd with features useful for forensics
and security. dcfldd has the following additional features:

   * Hashing on-the-fly - dcfldd can hash the input data as it is being
     transferred, helping to ensure data integrity.
   * Status output - dcfldd can update the user of its progress in terms of
     the amount of data transferred and how much longer operation will take.
   * Flexible disk wipes - dcfldd can be used to wipe disks quickly
     and with a known pattern if desired.
   * Image/wipe Verify - dcfldd can verify that a target drive is a
     bit-for-bit match of the specified input file or pattern.
   * Multiple outputs - dcfldd can output to multiple files or disks at
     the same time.
   * Split output - dcfldd can split output to multiple files with more
     configuration possibilities than the split command.
   * Piped output and logs - dcfldd can send all its log data and output
     to commands as well as files.

%prep
%autosetup -n %{name}-%{version}

%build
autoreconf -i
export CFLAGS="$CFLAGS -std=c99"
%configure
%make_build

%check
# Sanity check:
# check that the binary can be executed and that it reports current version
src/dcfldd --version | grep %{version} > /dev/null


%install
#%%{__make} install DESTDIR="%%{buildroot}" INSTALL="install -p"
%make_install

%files
%doc AUTHORS ChangeLog README
%license COPYING
%{_mandir}/man1/dcfldd.1*
%{_bindir}/dcfldd

%changelog
%autochangelog
