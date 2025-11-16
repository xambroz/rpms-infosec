Name:           fatresize
Version:        1.1.0
License:        GPL-3.0-or-later
Summary:        FAT16/FAT32 resizer
URL:            https://github.com/ya-mouse/fatresize
VCS:            git:https://github.com/ya-mouse/fatresize

# by default it builds from the git snapshot
# to build from release use rpmbuild --with=releasetag
%bcond_with     releasetag

%global         gituser         ya-mouse
%global         gitname         fatresize
%global         gitdate         20221116
%global         commit          ab78c48fe46d0eb29fcdfa3c6586ade223218433
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%if %{with releasetag}
Release:        %autorelease
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
# Build from git commit
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

# https://github.com/ya-mouse/fatresize/pull/36
# https://bugzilla.redhat.com/show_bug.cgi?id=2256775
# This component makes use of autoconf internals in it configure.ac, which leads to a build failure with 2.72 since the internals have changed.
# As far as "AC_SYS_LARGEFILE" is called, there is no need to modify the CFLAGS as that is done by autoconf if necessary.
Patch0:         fatresize-autoconf2.72.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  parted-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  docbook-utils
BuildRequires:  w3m

%description
The FAT16/FAT32 non-destructive resizer.


%prep
%if %{with releasetag}
# Build from git release version
%autosetup -n %{gitname}-%{version} -p1
%else
%autosetup -n %%{gitname}-%%{commit} -p1
%endif

#docbook-to-man not available in Fedora
sed -i -e 's|docbook-to-man|docbook2man|;' Makefile.am


%build
autoreconf -ifv
%configure
%make_build


%install
%make_install


%check
make check
# dummy test
./fatresize --help > /dev/null


%files
%doc AUTHORS ChangeLog README
%license COPYING
%{_sbindir}/*
%{_mandir}/man1/*

%changelog
%autochangelog
