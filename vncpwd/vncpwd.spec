Name:           vncpwd
License:        GPLv2+
Version:        0.0
Summary:        VNC Password Decrypter
URL:            https://github.com/jeroennijhof/vncpwd
VCS:            https://github.com/jeroennijhof/vncpwd
%global         rel             3


%global         gituser         jeroennijhof
%global         gitname         vncpwd
%global         gitdate         20180223
%global         commit          58d585cbbc861bd6dbd9f6709ce8cb7f2afb75ba
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %{rel}.%{gitdate}git%{shortcommit}%{?dist}

Group:          Applications/System

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
The vncpwd decrypts the VNC password.

%prep
%autosetup -n %{name}-%{commit}


%build
%make_build


%install
install -m 755 -D %{name} "%{buildroot}/%{_bindir}/%{name}"


%files
%license README
%{_bindir}/%{name}

%changelog
* Sun Apr 18 2021 Michal Ambroz <rebus at, seznam.cz> 0.0-3.20180223git58d585c
- rebuild for f34

* Thu Apr 13 2017 Michal Ambroz <rebus at, seznam.cz> 0.0-2.gitdafebe0
- removed unused macro, adding README as license file

* Sat Mar 18 2017 Michal Ambroz <rebus at, seznam.cz> 0.0-1.gitdafebe0
- initial build for Fedora
