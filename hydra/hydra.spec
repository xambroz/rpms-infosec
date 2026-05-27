Summary:        Very fast network log-on cracker
Name:           hydra
Version:        9.7
Release:        %autorelease
License:        AGPL-3.0-only
URL:            https://github.com/vanhauser-thc/thc-hydra
VCS:            git:https://github.com/vanhauser-thc/thc-hydra
# Old URL       https://www.thc.org/thc-hydra/

Source0:        https://github.com/vanhauser-thc/thc-hydra/archive/v%{version}/%{name}-%{version}.tar.gz

# Sent upstream via email 20120518
Patch0:         hydra-00-use-system-libpq-fe.patch

# Paths aligned with the Fedora packaging
Patch1:         hydra-01-fix-dpl4hydra-dir.patch

# https://patch-diff.githubusercontent.com/raw/vanhauser-thc/thc-hydra/pull/970
# Migrate to freerdp3
# Patch2:         https://patch-diff.githubusercontent.com/raw/vanhauser-thc/thc-hydra/pull/970.patch#/hydra-02-freerdp3.patch

# From Debian 03_use_bin_path.diff
# Description: Use /usr/bin/hydra path by default in xhydra.
# Forwarded: not-needed
# Author: Julián Moreno Patiño <darkjunix@gmail.com>
# Last-Update: 2022-10-05
Patch3:         hydra-03_use_bin_path.diff

# Upstream fixes for gtk3 support - merged in in v9.7
# https://github.com/vanhauser-thc/thc-hydra/commit/30e6291be7f222530dbd4b6bb7460c9e2a8a5e82
# Patch5:         hydra-05-port-xhydra-gtk3.patch
# https://github.com/vanhauser-thc/thc-hydra/commit/ae1a9087023e6683b0b62b1d96651401e88ad8ad
# Patch6:       hydra-06-more-hydra-gtk.patch
# https://github.com/vanhauser-thc/thc-hydra/commit/31c9b1188b69da372f638b93d48e2322046e3f16
# Patch7:       hydra-07-gtk-last.patch

# Upstream Fix for libbson2/libmongc2
# merged in v9.7 - https://github.com/vanhauser-thc/thc-hydra/commit/e5729446de04b5e65f3c673f0e0fbe5995976573
# Patch8:       hydra-08-libmongoc2.patch

BuildRequires:  afpfs-ng-devel
BuildRequires:  apr-devel
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  firebird-devel
# FreeRDP
BuildRequires:  freerdp-devel
BuildRequires:  gcc
BuildRequires:  gtk3-devel
BuildRequires:  libbson-devel
BuildRequires:  libfbclient2-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libidn-devel
BuildRequires:  libmemcached-devel
# Postgresql
BuildRequires:  libpq-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libssh-devel
# FreeRDP
BuildRequires:  libwinpr-devel
BuildRequires:  make
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  memcached-devel
BuildRequires:  mongo-c-driver-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  pkgconfig
BuildRequires:  subversion-devel

%description
Hydra is a parallelized log-in cracker which supports numerous protocols to
attack. New modules are easy to add, beside that, it is flexible and very fast.

This tool gives researchers and security consultants the possibility to show
how easy it would be to gain unauthorized access from remote to a system.

%package frontend
Summary: The GTK+ front end for hydra
Requires: hydra = %{version}-%{release}
%description frontend
This package includes xhydra, a GTK+ front end for hydra. 

%prep
%autosetup -p 1 -n thc-hydra-%{version}

%build
%configure --nostrip
%make_build

%install
%make_install \
    PREFIX="" \
    BINDIR="%{_bindir}" \
    MANDIR="%{_mandir}/man1" \
    DATADIR="%{_datadir}/%{name}" \
    PIXDIR="%{_datadir}/pixmaps" \
    APPDIR="%{_datadir}/applications"

# Fix dpl4hydra.sh (w/o buildroot prefix)
sed -i 's|^INSTALLDIR=.*|INSTALLDIR=/usr|' %{buildroot}/%{_bindir}/dpl4hydra.sh

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/xhydra.desktop

%files
%doc CHANGES README
%license LICENSE
%{_bindir}/dpl4hydra.sh
%{_bindir}/hydra
%{_bindir}/hydra-wizard.sh
%{_bindir}/pw-inspector
%{_datadir}/%{name}
%{_mandir}/man1/hydra.1*
%{_mandir}/man1/pw-inspector.1*

%files frontend
%{_bindir}/xhydra
%{_datadir}/pixmaps/xhydra.png
%{_datadir}/applications/xhydra.desktop
%{_mandir}/man1/xhydra.1*

%changelog
%autochangelog
