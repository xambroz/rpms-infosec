Name:           burpsuite_community
Version:        2024.9.5
Release:        1%{?dist}
Summary:        Security tool for analyzing web application security

Group:          Applications/System

#               Proprietary Free to Use
License:        Burp License

URL:            http://portswigger.net/suite/
#               http://portswigger.net/burp/burpsuite_free_v1.6.jar
#               https://portswigger.net/Burp/Releases/Download?productId=100&version=%%{version}6&type=Jar
# Source0:      http://portswigger.net/burp/burpsuite_free_v%%{version}.jar

# Download the Source0 automatically during the rebuild of RPM package
%undefine       _disable_source_fetch

# Source0:      https://portswigger.net/Burp/Releases/Download?productId=100&version=2024.9.5&type=Jar#/burpsuite_community_2024.9.5.jar
Source0:        https://portswigger.net/Burp/Releases/Download?productId=100&version=%{version}&type=Jar#/burpsuite_community_%{version}.jar
# Do not copy the Source0 file to the SRPM package
NoSource:       0
%define         SHA256SUM0 78c00c8fdbff4f549a65b9159a4ac4896345e388ee83d1694cae0caeeee32af0


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
# Do not unpack the jar file
#%%setup -q -n %%{name}_v%%{version}

# Check that the jar file is present (that it was downloaded)
if [ ! -f %{SOURCE0} ] ; then
    echo "ERROR: file %{SOURCE0} missing"
    exit 1
fi

# Check the checksum
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
if [ $? -ne 0 ] ; then
    echo "ERROR: file %SOURCE0 sha256 checksum is not %SHA256SUM0"
    exit 2
fi


# Unpack the license file
jar xvf %{SOURCE0} resources/Legal/EulaCommunity.txt


%build
sed -e "s:@@datadir@@:%{_datadir}:g" \
    -e "s:@@version@@:%{version}:g" \
    -e "s:@@name@@:%{name}:g" < %{SOURCE1} > %{name}

%install
mkdir -p  %{buildroot}%{_datadir}/%{name}/
install %{SOURCE0} %{buildroot}%{_datadir}/%{name}/

install -Dp -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications/

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=%{name}
Name=Burp Suite Community
Comment=Security tool for analyzing web application security
GenericName=Burpsuite Community Edition
Icon=%{name}
Terminal=false
Categories=System;Security;
StartupNotify=true
EOF

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{16x16,20x20,28x28,32x32,64x64}/apps
cd %{buildroot}/%{_datadir}/icons/hicolor
jar xvf %{SOURCE0} resources/Media/icon16community.png \
                   resources/Media/icon20community.png \
                   resources/Media/icon28community.png \
                   resources/Media/icon32community.png \
                   resources/Media/icon64community.png
mv resources/Media/icon16community.png ./16x16/apps/%{name}.png
mv resources/Media/icon20community.png ./20x20/apps/%{name}.png
mv resources/Media/icon28community.png ./28x28/apps/%{name}.png
mv resources/Media/icon32community.png ./32x32/apps/%{name}.png
mv resources/Media/icon64community.png ./64x64/apps/%{name}.png
rm -rf burp



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
#%%doc readme\ -\ running\ burp.txt
%license resources/Legal/EulaCommunity.txt
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
* Tue Feb 12 2019 Michal Ambroz <rebus at, seznam.cz> 1.7.36-1
- bump to 1.7.36

* Wed Apr 04 2018 Michal Ambroz <rebus at, seznam.cz> 1.7.33-1
- bump to 1.7.33

* Tue Jun 07 2016 Michal Ambroz <rebus at, seznam.cz> 1.7.03-1
- bump to 1.7.03

* Fri Jan 15 2010 Michal Ambroz <rebus at, seznam.cz> 1.3-1
- Initial burpsuite package for Fedora
