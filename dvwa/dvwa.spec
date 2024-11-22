Name:           dvwa
Version:        1.0.6
Release:        1%{?dist}
Summary:        Damn Vulnerable Web Application

Group:          Applications/Internet

#DVWA is licensed as GPLv3+ and it contains phpids library with LGPLv3+ license
License:        GPLv3+ and LGPLv3+
URL:            http://www.dvwa.co.uk/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  dos2unix

%description
Damn Vulnerable Web App (DVWA) is a PHP/MySQL web application that is damn
vulnerable. Its main goals are to be an aid for security professionals to
test their skills and tools in a legal environment, help web developers
better understand the processes of securing web applications and aid
teachers/students to teach/learn web application security in a class
room environment.

%prep
%setup -q
find ./ -type f -name '*.php' | xargs dos2unix
find ./ -type f -name '*.js'  | xargs dos2unix
find ./ -type f -name '*.css' | xargs dos2unix
find ./ -type f -name '*.ini' | xargs dos2unix


%build
#Nothing to build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/var/www/html
cp -p -R dvwa %{buildroot}/var/www/html
rm -rf %{buildroot}/var/www/html/dvwa/docs

rm -f %{buildroot}/var/www/html/dvwa/CHANGELOG.txt
rm -f %{buildroot}/var/www/html/dvwa/COPYING.txt
rm -f %{buildroot}/var/www/html/dvwa/README.txt

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc dvwa/CHANGELOG.txt dvwa/COPYING.txt dvwa/README.txt dvwa/docs/DVWA\ Article\ for\ OWASP\ Turkey.pdf
%dir /var/www/html/dvwa
/var/www/html/dvwa/*
/var/www/html/dvwa/.*




%changelog
