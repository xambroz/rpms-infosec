Name:		cowrie
Version:	1.2.0
Release:	git20170930.1%{?dist}
Summary:	Medium interaction SSH honeypot
License:	BSD


%global         gituser         micheloosterhof
%global         gitname         cowrie
%global         commit          f09c91292ef65649508f8efa40056fc7dc378e14
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

#               http://www.micheloosterhof.com/cowrie/
#               https://github.com/micheloosterhof/cowrie/
URL:            https://github.com/%{gituser}/%{gitname}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildArch:	noarch
BuildRequires:	python2-devel python-setuptools openssl-devel libffi-devel
BuildRequires:  python2-cffi
Requires:       python2-virtualenv
Requires:       python2-twisted
Requires:       python2-cryptography
Requires:       python2-configparser
Requires:       pyOpenSSL
Requires:       python2-pyparsing
Requires:       python2-packaging
Requires:       python2-appdirs
Requires:       python2-pyasn1-modules
Requires:       python2-attrs
Requires:       python-service-identity
Requires:       python2-dateutil
Requires:       python-tftpy

%description
Cowrie is a medium interaction SSH and telnet honeypot designed to log brute force attacks
and, most importantly, the entire shell interaction performed by the attacker.

%prep
%setup -q -n %{gitname}-%{commit}

#Change implicit "env python" to explicit versioned python shebang
#https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
for I in bin/playlog bin/fsctl bin/createfs bin/asciinema ; do
	sed -e 's|^#!/usr/bin/env python|#!%{__python2}|' "$I" > "${I}.new"
	touch -r "$I" "${I}.new"
	mv "${I}.new" "$I"
done


%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}/opt/cowrie
cp -rp * %{buildroot}/opt/cowrie/
mkdir -p %{buildroot}/etc/cowrie
ln -s /opt/cowrie/cowrie.cfg %{buildroot}/etc/cowrie/cowrie.cfg
mkdir -p %{buildroot}/etc/cowrie

%pre
getent group cowrie >/dev/null || groupadd -r cowrie
getent passwd cowrie >/dev/null || \
    useradd -r -g cowrie -d /opt/cowrie -s /sbin/nologin \
    -c "Cowrie Honeypot" cowrie



%files
%license LICENSE.md
/opt/cowrie/
/etc/cowrie/


%doc README.md CHANGELOG.md doc/


%changelog
* Tue Nov 12 2017 Michal Ambroz <rebus _AT seznam.cz> - 1.2.0-1.git20171109
- Initial package
