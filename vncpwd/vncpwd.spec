%global         gituser         jeroennijhof
%global         gitname         vncpwd
%global         commit          dafebe087e697e4c8d0a8b795a07748850fe86e8
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           vncpwd
Version:        0.0
Release:        2.git%{shortcommit}%{?dist}
Summary:        VNC Password Decrypter

License:        GPLv2+
URL:            https://github.com/jeroennijhof/vncpwd
Group:          Applications/System

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:  gcc

%description
The vncpwd decrypts the VNC password.

%prep
%setup -q -n %{name}-%{commit}

%build
CFLAGS="%{optflags}" make


%install
install -m 755 -D %{name} "%{buildroot}/%{_bindir}/%{name}"


%files
%license README
%{_bindir}/%{name}

%changelog
* Thu Apr 13 2017 Michal Ambroz <rebus at, seznam.cz> 0.0-2.gitdafebe0
- removed unused macro, adding README as license file

* Sat Mar 18 2017 Michal Ambroz <rebus at, seznam.cz> 0.0-1.gitdafebe0
- initial build for Fedora
