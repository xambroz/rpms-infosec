Name:           burpsuite_pro
Version:        1.2.17
Release:        1%{?dist}
Summary:        Security tool for analyzing web application security

Group:          Applications/System
License:        Burp Profesional Proprietary License
URL:            http://portswigger.net/suite/
Source0:        http://portswigger.net/suite/burpsuite_v1.2.17_pro.zip
Source1:        %{name}.in
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
NoSource:       0

BuildRequires:  sed
Requires:       java

%description


Burp suite allows an attacker to combine manual and automated techniques 
to enumerate, analyse, attack, and exploit Web applications. The various burp
tools work together effectively to share information and allow findings
identified within one tool to form the basis of an attack using another.
Numerous interfaces are implemented between the different tools, designed 
to facilitate and speed up the process of attacking a Web application. 
All tools share the same robust framework for handling HTTP requests, 
authentication, downstream proxies, logging, alerting, and extensibility. 
Burp suite is extensible via the IBurpExtender interface.


%prep
%setup -q -n burpsuite_v%{version}_pro


%build
%__sed -e "s:@@datadir@@:%{_datadir}:g" \
    -e "s:@@version@@:%{version}:g" \
    -e "s:@@name@@:%{name}:g" < %{SOURCE1} > %{name}

%install
%__rm -rf $RPM_BUILD_ROOT
%__mkdir -p  $RPM_BUILD_ROOT%{_datadir}/%{name}/
%__install *.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/

%__install -Dp -m 0755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
%__rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc readme\ -\ running\ burp.txt terms\ and\ conditions.txt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.jar
%{_bindir}/%{name}

%changelog
* Fri Jan 15 2010 Michal Ambroz <rebus at, seznam.cz> 1.2.17-1
- Initial burpsuite_pro package for Fedora

