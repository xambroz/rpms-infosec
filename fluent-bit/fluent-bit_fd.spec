%define _build_id_links none

Name:           fluent-bit
Summary:        Fast and Lightweight Log processor and forwarder for Linux, BSD and OSX
Version:        1.7.4
Release:        1%{?dist}
License:        ASL 2.0
Distribution:   RHEL7
URL:            https://fluentbit.io
#Source0:       https://github.com/fluent/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake3

%description
Fluent Bit is a fast Log Processor and Forwarder for Linux, Embedded Linux, MacOS and BSD 
family operating systems. It's part of the Fluentd Ecosystem and a CNCF sub-project.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q

%build
cd build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} ..
%make_build
#%%cmake_build

%install
cd build
make install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%exclude /usr/src/debug
/lib/systemd/system/fluent-bit.service
%{_bindir}/*
/usr/etc/fluent-bit/*

%files devel
%{_includedir}/*
/usr/lib64/fluent-bit/*.so

%changelog
* Thu Apr 22 2021 Florian Dubourg <florian.dubourg@dhl.com> 1.7.4-1
- Original version for DHL
