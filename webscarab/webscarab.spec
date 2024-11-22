Name:           webscarab
Version:        20090427
Release:        1304%{?dist}
Summary:        OWASP web proxy for application security testing

Group:          Applications/Internet
License:        GPL-2.0-only
URL:            http://www.owasp.org/index.php/Category:OWASP_WebScarab_Project
Source0:        http://dawes.za.net/rogan/webscarab/webscarab-current.zip
Source1:        %{name}.in
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
#Requires:       

%description
WebScarab is a framework for analysing applications that communicate using the 
HTTP and HTTPS protocols. It is written in Java, and is thus portable to many
platforms. WebScarab has several modes of operation, implemented by a number 
of plugins. In its most common usage, WebScarab operates as an intercepting
proxy, allowing the operator to review and modify requests created by the 
browser before they are sent to the server, and to review and modify 
responses returned from the server before they are received by the browser.
WebScarab is able to intercept both HTTP and HTTPS communication.


%prep
%setup -q -n %{name}-%{version}-1304


%build
#nothing to build
%__sed -e "s:@@datadir@@:%{_datadir}:g" \
    -e "s:@@version@@:%{version}:g" \
    -e "s:@@name@@:%{name}:g" < %{SOURCE1} > %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp %{name}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -D -m 0755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog  LICENSE  README
%{_datadir}/%{name}/*
%{_bindir}/%{name}

%changelog
* Sun Jan 24 2010 Michal Ambroz <rebus at, seznam.cz> 20090427-1304
- Initial SPEC for Fedora 12

