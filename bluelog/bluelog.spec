Name:           bluelog
Version:        1.0.4
Release:        1%{?dist}
Summary:        Bluetooth scanner to log devices that are in discoverable mode

License:        GPLv2 
URL:            http://www.digifail.com/software/bluelog.shtml
Source0:        ftp://ftp.digifail.com/downloads/software/bluelog/%{name}-%{version}.tar.gz

BuildRequires:  bluez-libs-devel

%description


%prep
%setup -q


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%files
%doc %{_datadir}/doc/%{name}-%{version}
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_sharedstatedir}/%{name}

%changelog
* Tue Jun 19 2012 Michal Ambroz <rebus at, seznam.cz> 1.0.4-1
- initial package for Fedora 17
