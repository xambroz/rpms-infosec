Name:           amap
Version:        5.4
Release:        %autorelease
Summary:        Network tool for application protocol detection
Group:          Applications/System
License:        AMAP License
#License        AMAP non-commercial rules added to GPLv2
URL:            http://thc.org/
# was           http://freeworld.thc.org/thc-amap/

Source0:        https://github.com/hackerschoice/THC-Archive/raw/refs/heads/master/Tools/%{name}-%{version}.tar.gz
# was Source0:        http://freeworld.thc.org/releases/%%{name}-%%{version}.tar.gz
Patch0:         %{name}-destdir.patch
Patch1:         %{name}-path.patch
Patch2:         %{name}-ldflags.patch
# Patch3:       %%{name}-new-homepage.patch
Patch4:         %{name}-system-pcre.patch
Patch5:         %{name}-optflags.patch
Patch6:         %{name}-lnamap6.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel

%description
THC Amap is a next-generation tool for assisting network penetration testing.
It performs fast and reliable application protocol detection, independent
on the TCP/UDP port they are being bound to.

%prep
%autosetup -p 1

%build
#%%configure
./configure --prefix=%{_prefix} --libdir=%{_libdir}
OPT="$RPM_OPT_FLAGS" make %{?_smp_mflags}


%install
%make_install

%clean
rm -rf %{buildroot}

%files
%doc CHANGES README TODO LICENCE.AMAP LICENSE.GNU
%{_bindir}/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}

%changelog
%autochangelog
