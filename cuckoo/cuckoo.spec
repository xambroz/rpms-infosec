%global         gituser         cuckoosandbox
%global         gitname         cuckoo
%global         commit          743fe2c5410ff12a39dc158e343b7f8a044ff120
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global		gitrelease	rc1
Name:           cuckoo
Version:        2.0
Release:        %{gitrelease}.1%{?dist}
Summary:        Cuckoo Sandbox - malware analysis system

Group:          Applications/Internet

#Special exception to allow linking against the OpenSSL libraries
License:        GPLv3+ with exceptions


URL:             http://www.cuckoosandbox.org/about.html
Source0:         https://github.com/cuckoobox/%{name}/archive/%{version}-%{gitrelease}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel

%description
Cuckoo Sandbox is a malware analysis system. It automates execution of malware in isolated
environment and performing behavioral, static and dynamic analysis of the malware samples.

%prep
#setup -qn %{name}-%{commit}
%setup -qn %{name}-%{version}-%{gitrelease}


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changelog README.md LICENSE TODO
%attr (755,root,root) %{_bindir}/%{name}
%attr (644,root,root) %{_mandir}/man1/%{name}.1*

%changelog
* Wed Oct 19 2016 Michal Ambroz <rebus at, seznam.cz> 2.0-rc1.1
- bump

* Sat Jan 25 2014 Michal Ambroz <rebus at, seznam.cz> 1.10.1-1
- initial package of cuckoo for Fedora

