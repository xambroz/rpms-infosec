Name:           nwipe
Version:        0.38
Release:        %autorelease
Summary:        Securely erase disks using a variety of recognized methods


%global         gituser         martijnvanbrummelen
%global         gitname         nwipe
%global         commit          28271712db2609eee7f842fc67a6654b5a87140b
%global         gitdate         20240510
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


License:        GPL-2.0-only
# used to be    http://nwipe.sourceforge.net
URL:            https://github.com/martijnvanbrummelen/nwipe
VCS:            git:https://github.com/martijnvanbrummelen/nwipe
# Releases      https://github.com/martijnvanbrummelen/nwipe/releases

#Source0:       https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  parted-devel
BuildRequires:  ncurses-devel
BuildRequires:  libconfig-devel
BuildRequires:  autoconf
BuildRequires:  automake

# Runtime dependencies
Requires:       /usr/bin/readlink
Requires:       /usr/sbin/dmidecode
Requires:       hdparm
Requires:       /usr/sbin/modprobe
Requires:       /usr/sbin/smartctl


# Recommends only supported on fedora and rhel8+
%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
# used to provide serial number of drive over supported USB to SATA interface
Recommends:     smartmontools
# provide SMBIOS/DMI host data to log file
Recommends:     dmidecode
%endif


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

# On RHEL7 it is needed to explicitly pregress to c99 compatibility mode
%if 0%{?rhel} && 0%{?rhel} <= 7
export CFLAGS="%{optflags} -std=c99 -D_XOPEN_SOURCE=500"
%endif

autoreconf -vif

%configure
# make %%{?_smp_mflags}
%make_build


%install
# make install DESTDIR=%%{buildroot} LDFLAGS="-lncurses -lpanel"
%make_install


%files
%license COPYING
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8.gz


%changelog
%{?%autochangelog: %autochangelog }
