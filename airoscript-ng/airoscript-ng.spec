Name:           airoscript-ng
Version:        1.0
Release:        1%{?dist}
Summary:        Text user interface for aircrack-ng

Group:          Applications/Internet
License:        GPL-2.0-only
URL:            http://airoscript.aircrack-ng.org/
Source0:        http://airoscript.googlecode.com/files/Airoscript-ng%{version}.tgz
Patch0:         %{name}-makefile.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
Requires:       screen
Requires:       aircrack-ng

%description
Airoscript is a complete text user interface for aircrack-ng.
It gives you almost all functionality that aircrack-ng has, allowing you to
save some time from writting commands.


%prep
%setup -q -n Airoscript
%patch0 -p 1 -b .makefile


%build
#Fix permissions on doc files
find doc -type f | xargs chmod -wx
chmod -R go=+rX doc

#Fix permissions for themes
chmod +x src/themes/*

%install
rm -rf $RPM_BUILD_ROOT
export prefix="%{_prefix}" etcdir="%{_sysconfdir}/%{name}" DESTDIR="$RPM_BUILD_ROOT"
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*
%{_mandir}/man1/*
%attr (755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}/*
%{_datadir}/%{name}
%lang(es_ES) %{_datadir}/locale/es_ES/*

%changelog
* Sun Jan 17 2010 Michal Ambroz <rebus at, seznam.cz> 1.0-1
- Initial SPEC for Fedora 12

