Name:           beef
Version:        0.4.0.0
Release:        %autorelease
Summary:        Browser exploitation framework

Group:          Applications/Internet
License:        Unknown
URL:            http://www.bindshell.net/tools/%{name}/
Source0:        http://www.bindshell.net/tools/%{name}/%{name}-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  sed
#Requires:       

%description
BeEF is a browser exploitation framework. This tool will demonstrate
the collecting of zombie browsers and browser vulnerabilities in real-time.
It provides a command and control interface which facilitates the targeting
of individual or groups of zombie browsers.

%prep
%setup -q
#Fix php tags
find ./ -name '*.php' | xargs sed -i \
    -e 's/<? /<?php/g;
	s/<?$/<?php/g;
	s/<?=/<?php echo/g;
        s/<?phpecho/<?php echo/g'

chown root /var/www/html/beef/include
chown -R root /var/www/html/beef/cache

%build
#Nothing to build

%install
rm -rf %{buildroot}
cp -r * %{buildroot}/var/www/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc


%changelog
%{?%autochangelog: %autochangelog }
