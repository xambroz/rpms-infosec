Name:           urlcrazy
Version:        0.5
Release:        1%{?dist}
Summary:        Generate and test domain typos and variations to detect typo squatting

Group:          Applications/Internet

#whatweb licensed as GPLv3
License:        GPLv3
URL:            http://www.morningstarsecurity.com/research/%{name}
#Source0:        http://www.morningstarsecurity.com/downloads/%{name}-%{version}.tar.gz
#Dev version of 0.4.8 as downloaded on 20120708 from https://github.com/urbanadventurer/WhatWeb/downloads
#Source0:         https://github.com/DinoTools/sslscan/archive/%{commit}/%{name}-%{version}.tar.gz
Source0:         https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#Switch to ruby 1.9.x
Patch3:         %{name}-ruby19.patch



#Requires:       ruby(abi) >= 1.8
Requires:       /usr/bin/ruby


%description
Generate and test domain typos and variations to detect and perform typo
squatting, URL hijacking, phishing, and corporate espionage.


%prep
%setup -qn %{gitname}-%{commit}
#%setup -q -n %{gituser}-%{gitname}-%{gitversion}
#%patch3 -p 1 -b .ruby

#Files with Windows ends of lines
sed -i -e 's/\r//' README
sed -i -e 's/\r//' whatweb.xsl


%build
echo "Nothing to build."


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README whatweb.xsl
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/addons
%dir %{_datadir}/%{name}/lib
%dir %{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/my-plugins
%dir %{_datadir}/%{name}/plugin-development
%dir %{_datadir}/%{name}/plugins-disabled
%{_datadir}/%{name}/addons/*
%{_datadir}/%{name}/lib/*
%{_datadir}/%{name}/plugins/*
%{_datadir}/%{name}/my-plugins/*
%{_datadir}/%{name}/plugin-development/*
%{_datadir}/%{name}/plugins-disabled/*
%{_mandir}/man1/%{name}.1*


%changelog
* Sun Jul 08 2012 Michal Ambroz <rebus at, seznam.cz> - 0.4.8-0.git20120708.1
- bump to development version 0.4.8

* Wed Apr 06 2011 Michal Ambroz <rebus at, seznam.cz> - 0.4.7-1
- bump to version 0.4.7

* Sun Mar 27 2011 Michal Ambroz <rebus at, seznam.cz> - 0.4.6-1
- bump to version 0.4.6
- cant be used with the current unpatched version of anemone

* Sat Sep 11 2010 Michal Ambroz <rebus at, seznam.cz> - 0.4.5-2
- use system-wide rubygems anemone library insted of local anemone copy

* Mon Aug 23 2010 Michal Ambroz <rebus at, seznam.cz> - 0.4.5-1
- rebuild of new version 0.4.5

* Sun May 30 2010 Michal Ambroz <rebus at, seznam.cz> - 0.4.3-1
- rebuild of new version

* Sat May 1 2010 Michal Ambroz <rebus at, seznam.cz> - 0.4.2-2
- add explicit dependency to /usr/bin/ruby

* Sat May 1 2010 Michal Ambroz <rebus at, seznam.cz> - 0.4.2-1
- initial build for Fedora Project
