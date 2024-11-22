Summary:	DNS database debugger
Name:		dnswalk
Version:	2.0.2
Release:	1%{?dist}
License:Artistic-2.0
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-perlpath.patch
Patch1:		%{name}-delete-filterout.patch
URL:		http://sourceforge.net/projects/dnswalk/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dnswalk is a DNS debugger. It performs zone transfers of specified
domains, and checks the database in numerous ways for internal
consistency, as well as accuracy.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p0

%build
#Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1}
install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO makereports sendreports rfc1912.txt do-dnswalk
%attr(755,root,root) %{_sbindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Jan 14 2010 Michal Ambroz <rebus at, seznam.cz> 2.0.2-1
- Initial SPEC for Fedora 12 using SPEC and patches from PLD
- Original SPEC by sparky glen baggins qboosh glen 

