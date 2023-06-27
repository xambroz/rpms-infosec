Name:           pince
Version:        0.0.0
%global         baserelease       1
%global         upversion         %{version}

Summary:        Reverse engineering tool for linux games

License:        GPL-3.0-or-later
VCS:            https://github.com/korcankaraokcu/PINCE
#               https://github.com/korcankaraokcu/PINCE/releases
URL:            https://github.com/korcankaraokcu/PINCE

# Tutorial      https://www.youtube.com/watch?v=hUPvk2ejYTk


%global         gituser         korcankaraokcu
%global         gitname         PINCE
%global         gitdate         20230226
# Commit of version 0.0.0
%global         commit          7e95dcd360d56f87b920441ede8163b836245383
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_with     release


# Build from git release version
%if %{with release}
# Source0:      https://github.com/%%{gituser}/%%{gitname}/archive/v%%{version}.tar.gz#/%%{name}-%%{version}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{upversion}.tar.gz#/%{name}-%{upversion}.tar.gz
Release:        %{baserelease}%{?dist}
%else
# Build from git commit baseline
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Release:        0.%{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
%endif


BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  readline-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pyqt6
BuildRequires:  python3-psutil
BuildRequires:  python3-pexpect
BuildRequires:  python3-distorm3
BuildRequires:  python3-pygdbmi
BuildRequires:  python3-keyboard

Requires:       gdb

%description



%prep
%if %{with release}
    %{gitname}-%{upversion} -p 1 -S git
%else
    %autosetup -n %{gitname}-%{commit} -p 1 -S git
%endif

%build
%make_build


%install
%make_install


%check

%files
%license COPYING
%doc AUTHORS CONTRIBUTORS README.md
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}c.1*




%changelog
* Wed Mar 08 2023 Michal Ambroz <rebus at, seznam.cz> - 0.0.0-1
- initial package