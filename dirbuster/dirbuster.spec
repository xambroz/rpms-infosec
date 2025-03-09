Name:           dirbuster
Version:        1.0
Release:        %autorelease -s RC1
Summary:        Brute force directories and files names on web/application servers

Group:          Applications/Internet
License:        LGPL + Creative Commons
URL:            http://www.owasp.org/index.php/Category:OWASP_DirBuster_Project#tab=Download
Source0:        http://downloads.sourceforge.net/dirbuster/DirBuster-%{version}-RC1.tar.bz2
Source1:        %{name}.in
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
#Requires:       

%description
DirBuster is a multi threaded java application designed to brute force 
directories and files names on web/application servers. Often is the 
case now of what looks like a web server in a state of default installation 
is actually not, and has pages and applications hidden within. DirBuster 
attempts to find these. 

%prep
%setup -q -n DirBuster-%{version}


%build
#Nothing to build
%__sed -e "s:@@datadir@@:%{_datadir}:g" \
    -e "s:@@version@@:%{version}:g" \
    -e "s:@@name@@:%{name}:g" < %{SOURCE1} > %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp DirBuster-%{version}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -D -m 0755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
cp *.txt $RPM_BUILD_ROOT%{_datadir}/%{name}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/*
%attr (755,root,root) %{_bindir}/%{name}



%changelog
* Sun Jan 24 2010 Michal Ambroz <rebus at, seznam.cz> 0.12-1
- Initial SPEC for Fedora 12

