Name:           burpsuite
Version:        1.6
Release:        1%{?dist}
Summary:        Security tool for analyzing web application security

Group:          Applications/System
License:        Burp License
#License:        Proprietary Free to Use
URL:            http://portswigger.net/suite/
#http://portswigger.net/burp/burpsuite_free_v1.6.jar
Source0:        http://portswigger.net/burp/burpsuite_free_v%{version}.jar
Source1:        %{name}.in
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  sed
BuildRequires:  java
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
#%setup -q -n %{name}_v%{version}


%build
%__sed -e "s:@@datadir@@:%{_datadir}:g" \
    -e "s:@@version@@:%{version}:g" \
    -e "s:@@name@@:%{name}:g" < %{SOURCE1} > %{name}

%install
%__rm -rf %{buildroot}
%__mkdir -p  %{buildroot}%{_datadir}/%{name}/
%__install %{SOURCE0} %{buildroot}%{_datadir}/%{name}/

%__install -Dp -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications/

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=%{name}
Name=burpsuite
Comment=Security tool for analyzing web application security
GenericName=Burpsuite Free Edition
Icon=burpsuite
Terminal=false
Categories=System;Security;
StartupNotify=true
EOF

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{16x16,20x20,28x28,32x32,64x64}/apps
cd %{buildroot}/%{_datadir}/icons/hicolor
jar xvf %{SOURCE0} burp/media/icon16.png burp/media/icon20.png burp/media/icon28.png burp/media/icon32.png burp/media/icon64.png
mv burp/media/icon16.png ./16x16/apps/%{name}.png
mv burp/media/icon20.png ./20x20/apps/%{name}.png
mv burp/media/icon28.png ./28x28/apps/%{name}.png
mv burp/media/icon32.png ./32x32/apps/%{name}.png
mv burp/media/icon64.png ./64x64/apps/%{name}.png
rm -rf burp


%clean
%__rm -rf %{buildroot}

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
        touch --no-create %{_datadir}/icons/hicolor &>/dev/null
        gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
#%doc readme\ -\ running\ burp.txt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.jar
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/20x20/apps/%{name}.png
%{_datadir}/icons/hicolor/28x28/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png



%changelog
* Fri Jan 15 2010 Michal Ambroz <rebus at, seznam.cz> 1.3-1
- Initial burpsuite package for Fedora
