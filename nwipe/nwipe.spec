Name:           nwipe
Version:        0.43
Release:        %autorelease
Summary:        Securely erase disks using a variety of recognized methods


%global forgeurl https://github.com/martijnvanbrummelen/nwipe
%forgemeta

License:        GPL-2.0-only
# used to be    http://nwipe.sourceforge.net
URL:            %{forgeurl}
# Releases      https://github.com/martijnvanbrummelen/nwipe/releases

Source0:        %{forgesource}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libconfig-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  parted-devel

# Runtime dependencies
Requires:       coreutils
Requires:       dmidecode
Requires:       hdparm
Requires:       kmod
Requires:       smartmontools


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
%autosetup -n %{archivename} -p 1


%build
autoreconf -vif
%configure
%make_build


%install
%make_install


%check
%make_build check


%files
%license COPYING
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8.gz


%changelog
%autochangelog
