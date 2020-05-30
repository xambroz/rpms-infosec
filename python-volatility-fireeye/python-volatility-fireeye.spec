%global         gituser         fireeye
%global         gitname         Volatility-Plugins
%global         gitdate         20160705
%global         commit          8094e1e41864e33ee6aa5c2da087e7e1dd2f3849
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           python-volatility-fireeye
Version:        2.5.0
Release:        1%{?dist}
Summary:        Plugins for Volatility framework from FireEye

License:        GPLv2+
URL:            http://github.com/fireeye/Volatility-Plugins
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{gitname}-%{version}-%{shortcommit}.tar.gz
Source1:        vol_genprofile

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools
Requires:       pycrypto

#Used in script vol_genprofile for generation of linux profile
BuildRequires:  python-volatility

%description
Volatility plugins from fireeye - currently only the shimcachemem.


%prep
%setup -qn %{gitname}-%{commit}


%build
#%{__python2} setup.py build

%install
#%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{python2_sitelib}/volatility/plugins/fireeye
cp -p -R * %{buildroot}%{python2_sitelib}/volatility/plugins/fireeye/
find %{buildroot}%{python2_sitelib}/volatility/plugins/fireeye -type d -exec touch '{}/__init__.py' ';'


%files
%{!?_licensedir:%global license %%doc}
#%license LICENSE.txt
%doc README.md

%dir %{python2_sitelib}/volatility/plugins/fireeye
%{python2_sitelib}/volatility/plugins/fireeye/*


%changelog
* Fri Mar 9 2018 Michal Ambroz <rebus at, seznam.cz> - 2.6.0-1
- update with commits for Windows 10

* Wed Nov 11 2015 Michal Ambroz <rebus at, seznam.cz> - 2.5.0-1
- initial package for Fedora
