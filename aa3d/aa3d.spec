Name:           aa3d
Version:        1.0
Release:        1%{?dist}
Summary:        ASCII art stereogram generator

License:        GPLv2+
URL:            http://aa-project.sourceforge.net/aa3d/
Source0:        http://downloads.sourceforge.net/aa-project/%{name}-%{version}.tar.gz

%description
AA-project releases so called technology demo for it's 3d stereogram
technology (ASCII-3D-2000). It uses well known and popular random dot
stereograms in ASCII ART.

%prep
%setup -q

%build
%make_build %{?_smp_mflags} CFLAGS="%{optflags}"


%install
install -m 555 -D %{name} "%{buildroot}/%{_bindir}/%{name}"


%files
%doc README logo pyramid
%license COPYING
%{_bindir}/%{name}

%changelog
* Sat Feb 16 2013 Michal Ambroz <rebus at, seznam.cz> 1.0-1
- initial build for Fedora
