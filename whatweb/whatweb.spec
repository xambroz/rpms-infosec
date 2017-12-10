%global         gituser         urbanadventurer
%global         gitname         WhatWeb
%global         commit          039768f41a6cd45ec70c89b81616b669bc92ac0f
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           whatweb
Version:        0.4.9
Release:        1%{?dist}
Summary:        Web scanner to identify what websites are running

Group:          Applications/Internet

License:        GPLv2
URL:            http://www.morningstarsecurity.com/research/%{name}
#Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#Requires:       ruby(abi) >= 1.8
Requires:       /usr/bin/ruby


%description
Identify content management systems (CMS), blogging platforms, stats/analytic
packages, JavaScript libraries, servers and more. When you visit a website in
your browser the transaction includes many unseen hints about how the web-server
is set up and what software is delivering the web-page. Some of these hints are
obvious, ex. “Powered by XYZ” and others are more subtle. WhatWeb recognizes
these hints and reports what it finds.


%prep
#setup -qn %{gitname}-%{commit}
%setup -qn %{gitname}-%{version}

#Files with Windows ends of lines
sed -i -e 's/\r//' README
sed -i -e 's/\r//' whatweb.xsl


%build
echo "Nothing to build."


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/%{name}


%files
%doc CHANGELOG README whatweb.xsl
%license LICENSE 
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
* Wed Nov 23 2016 Michal Ambroz <rebus at, seznam.cz> - 0.4.8-0.git20161009.1
- bump to current git snapshot of 0.4.8 - 039768f41a6cd45ec70c89b81616b669bc92ac0f

* Mon Jun 20 2016 Michal Ambroz <rebus at, seznam.cz> - 0.4.8-0.git20160611.1
- bump to current git snapshot of 0.4.8 - f467aa2f154aea83b6b58aec85107ba3fa3eb635

* Mon Jun 22 2015 Michal Ambroz <rebus at, seznam.cz> - 0.4.8-0.git20150507.48b9682.1
- bump to current git snapshot of 0.4.8 - 48b9682a0fbf1607f1d3565f9aab3442aee14d12

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
