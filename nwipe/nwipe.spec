Name:           nwipe
Version:        0.41
Release:        %autorelease
Summary:        Securely erase disks using a variety of recognized methods


%global         gituser         martijnvanbrummelen
%global         gitname         nwipe
%global         commit          7fe250480a2f49ab6686dbd3665c8039eca7e998
%global         gitdate         20260515
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


License:        GPL-2.0-only
# used to be    http://nwipe.sourceforge.net
URL:            https://github.com/martijnvanbrummelen/nwipe
VCS:            git:https://github.com/martijnvanbrummelen/nwipe
# Releases      https://github.com/martijnvanbrummelen/nwipe/releases

#Source0:       https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libconfig-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  parted-devel

# Runtime dependencies
Requires:       hdparm
Requires:       /usr/bin/readlink
Requires:       /usr/sbin/dmidecode
Requires:       /usr/sbin/modprobe
Requires:       /usr/sbin/smartctl


# Recommends only supported on fedora and rhel8+
# used to provide serial number of drive over supported USB to SATA interface
Recommends:     smartmontools
# provide SMBIOS/DMI host data to log file
Recommends:     dmidecode


%description
The nwipe is a command that will securely erase disks using a variety of 
recognized methods. It is a fork of the dwipe command used by Darik's 
Boot and Nuke (dban). Nwipe was created out of need to run the DBAN dwipe
command outside of DBAN. This allows it to use any host distribution which
gives better hardware support. It is essentially the same as dwipe, with 
a few changes:
- pthreads is used instead of fork
- The parted library is used to detect drives
- The code is designed to be compiled with gcc
- Increased number of wipe methods
- Smartmontools is used to provide USB serial #
- DmiDecode is used to provide host info to nwipes log 

%prep
#autosetup -n %%{gitname}-%%{commit} -p 1
%autosetup -n %{gitname}-%{version} -p 1


%build
autoreconf -vif
%configure
%make_build


%install
%make_install


%check
make check


%files
%license COPYING
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8.gz


%changelog
%autochangelog
