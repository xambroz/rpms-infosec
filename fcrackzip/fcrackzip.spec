Summary:	A Free/Fast Zip Password Cracker
Name:		fcrackzip
Version:	1.0
Release:	1%{?dist}
URL:		http://oldhome.schmorp.de/marc/fcrackzip.html

License:	GPL

Group:		Applications/Forensics Tools
Source:		http://oldhome.schmorp.de/marc/data/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	gcc
BuildRequires:	make

%description
Fcrackzip searches each zipfile given for encrypted files and tries to
guess the password. All files must be encrypted with the same password,
the more files you provide, the better.

%prep
%autosetup

%build
mv configure.in configure.ac
autoreconf -i
%configure
%make_build

%install
%make_install
mv %{buildroot}/%{_bindir}/zipinfo %{buildroot}/%{_bindir}/fczipinfo


%files
%license COPYING
%doc NEWS THANKS AUTHORS TODO README ChangeLog
%{_bindir}/%{name}
%{_bindir}/fczipinfo
%{_mandir}/man1/%{name}.1*

%changelog
* Fri Jun 5 2020 Michal Ambroz <rebus _AT seznam.cz> 1.0-2
- rebuild for Fedora32 / gcc10

* Tue Mar 18 2014 Lawrence R. Rogers <lrr@cert.org> 1.0-1
	Initial version

