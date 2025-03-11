Name:           mdk4
Version:        4.2
Summary:        Wireless penetration testing tool
License:        GPL-3.0+
URL:            https://github.com/aircrack-ng/mdk4
VCS:            git:https://github.com/aircrack-ng/mdk4/
#               https://github.com/aircrack-ng/mdk4/releases/


%global         common_description %{expand:
MDK is a proof-of-concept tool to exploit common IEEE 802.11 protocol
weaknesses. It is intended to demonstrate these weaknesses and help
administrators and security auditors identify vulnerable access points.
}

%bcond_without  release

%global         gituser         aircrack-ng
%global         gitname         mdk4

# Commit of version 4.2
# %%global         gitdate         20211015
# %%global         commit          683e074f081624418f50090641a09db53ce0378d

%global         gitdate         20240816
%global         commit          36ca143a2e6c0b75b5ec60143b0c5eddd3d2970c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Build from git release version
%if %{with release}
Release:        %autorelease
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

%else
# Build from git commit baseline
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif


Patch01:        mdk4-01-manpage_example.patch
Patch02:        mdk4-02-makefile_osdep_parallel_build_fix.patch
Patch03:        mdk4-03-fix-x-mode-bug.patch
Patch04:        mdk4-04-Declare-functions-before-using-it.patch
Patch05:        mdk4-05-ftbfs-with-gcc-14.patch

Patch06:        mdk4-06-destdir.patch


BuildRequires:  git
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libnl3-devel


%description
%{common_description}


%prep
%if %{with release}
    %autosetup -n %{gitname}-%{version} -p 1 -S git
%else
    %autosetup -n %{gitname}-%{commit} -p 1 -S git
%endif



%build
export CFLAGS="$CFLAGS -std=gnu99 -D_XOPEN_SOURCE=500 -D_DEFAULT_SOURCE -D_BSD_SOURCE"
%make_build


%install
%make_install PREFIX=%{_prefix}

# Wrong naming for the manpage
if [ -f %{buildroot}%{_mandir}/man8/mdk4.2.gz ] ; then
    mv %{buildroot}%{_mandir}/man8/mdk4.2.gz %{buildroot}%{_mandir}/man8/mdk4.8.gz
fi





%check
# Dummpy check
cd src
./mdk4 --fullhelp | grep -e "mdk4 requires root privileges." > /dev/null




%files
%license COPYING
%doc AUTHORS CHANGELOG README.md TODO
%exclude %{_prefix}/src/%{name}/pocs/*
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.*




%changelog
%autochangelog
