Name:		cowrie
Version:	2.5.0
Release:	1%{?dist}
Summary:	Medium interaction SSH honeypot
License:	BSD
# was           http://www.micheloosterhof.com/cowrie/
# was URL:      https://github.com/micheloosterhof/cowrie/
URL:            https://github.com/cowrie/cowrie/
# Releases      https://github.com/cowrie/cowrie/releases


%global         gituser         cowrie
%global         gitname         cowrie
%global         commit          000116838246ce522b1f6953c6f108a3a4f0611c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

#Source0:        https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel python-setuptools openssl-devel libffi-devel
BuildRequires:  python3-cffi
Requires:       python3-twisted
Requires:       python3-cryptography
Requires:       python3-virtualenv
# configparser is the built-in feature of python3
Requires:       python3-pyOpenSSL
Requires:       python3-pyparsing
Requires:       python3-packaging
Requires:       python3-appdirs
Requires:       python3-pyasn1-modules
Requires:       python3-attrs
Requires:       python-service-identity
Requires:       python3-dateutil
Requires:       python-tftpy

%description
Cowrie is a medium interaction SSH and telnet honeypot designed to log brute force attacks
and, most importantly, the entire shell interaction performed by the attacker.

%prep
#setup -q -n %{gitname}-%{commit}
%setup -q -n %{gitname}-%{version}

#Change implicit "env python" to explicit versioned python shebang
#https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
for I in setup.py bin/* ; do
	sed -i -e 's|^#!/usr/bin/env python|#!%{__python3}|' "$I"
done


%build
echo "Nothing to build"

%install
mkdir -p %{buildroot}/opt/cowrie
cp -rp * %{buildroot}/opt/cowrie/
mkdir -p %{buildroot}/etc/cowrie
ln -s ../../opt/cowrie/cowrie.cfg %{buildroot}/etc/cowrie/cowrie.cfg
mkdir -p %{buildroot}/etc/cowrie

%pre
getent group cowrie >/dev/null || groupadd -r cowrie
getent passwd cowrie >/dev/null || \
    useradd -r -g cowrie -d /opt/cowrie -s /sbin/nologin \
    -c "Cowrie Honeypot" cowrie



%files
%license LICENSE.rst
/opt/cowrie/
/etc/cowrie/


%doc README.rst CHANGELOG.rst docs/


%changelog
* Thu Sep 19 2019 Michal Ambroz <rebus _AT seznam.cz> - 1.6.0-1
- bump to 1.6.0

* Sun Nov 12 2017 Michal Ambroz <rebus _AT seznam.cz> - 1.2.0-1.git20171109
- Initial package
