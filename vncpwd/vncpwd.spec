Name:           vncpwd
License:        GPL-2.0-or-later
Version:        0.1
Summary:        VNC Password Decrypter
URL:            https://github.com/jeroennijhof/vncpwd
VCS:            https://github.com/jeroennijhof/vncpwd
Group:          Applications/System
%global         baserelease             1


# by default it builds from the git snapshot version of faup
# to build from release use rpmbuild --with=releasetag
%bcond_without  release


%global         gituser         jeroennijhof
%global         gitname         vncpwd
%global         gitdate         20180223
%global         commit          58d585cbbc861bd6dbd9f6709ce8cb7f2afb75ba
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


%if %{with release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.zip
%endif


BuildRequires:  gcc
BuildRequires:  make

%description
The vncpwd decrypts the VNC password.

%prep
%if %{with release}
    %autosetup -n %{gitname}-%{version} -p 1
%else
    %autosetup -n %{gitname}-%{commit} -p 1
%endif


%build
%make_build


%install
install -m 755 -D %{name} "%{buildroot}/%{_bindir}/%{name}"


%files
%license README
%{_bindir}/%{name}

%changelog
* Thu Mar 23 2023 Michal Ambroz <rebus at, seznam.cz> 0.1-1
- bump to release tag

* Sun Apr 18 2021 Michal Ambroz <rebus at, seznam.cz> 0.0-3.20180223git58d585c
- rebuild for f34

* Thu Apr 13 2017 Michal Ambroz <rebus at, seznam.cz> 0.0-2.gitdafebe0
- removed unused macro, adding README as license file

* Sat Mar 18 2017 Michal Ambroz <rebus at, seznam.cz> 0.0-1.gitdafebe0
- initial build for Fedora
