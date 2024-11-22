Name:           xsss
Version:        0.40b
Release:        1%{?dist}
Summary:        Brute force cross site scripting scanner

Group:          Applications/Internet
License:        GPLv2
URL:            http://www.sven.de/xsss/
Source0:        http://www.sven.de/xsss/xsss-0.40b.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
Requires:       perl-WWW-Mechanize

%description
xsss is a brute force cross site scripting scanner.

%prep
%setup -q 


%build
#Nothing to build

%install
rm -rf $RPM_BUILD_ROOT
install -D %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc GPL README
%attr (755,root,root) %{_bindir}/%{name}


%changelog
* Sun Jan 24 2010 Michal Ambroz <rebus at, seznam.cz> 0.40b-1
- Initial SPEC for Fedora 12 
