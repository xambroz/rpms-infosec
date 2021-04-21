Name:           whatweb
Version:        0.5.5
Release:        1%{?dist}
Summary:        Web scanner to identify what websites are running


%global         gituser         urbanadventurer
%global         gitname         WhatWeb


%if 0%{?rhel}
Group:          Applications/Internet
%endif

License:        GPLv2
URL:            http://www.morningstarsecurity.com/research/whatweb
VCS:            https://github.com/urbanadventurer/WhatWeb
#               https://github.com/urbanadventurer/WhatWeb/releases/

Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

Buildrequires:  make
Buildrequires:  sed

#Requires:      ruby(abi) >= 2.0
Requires:       /usr/bin/ruby
Requires:       rubygem-addressable

%if 0%{?rhel} && 0%{?rhel} <= 8
Requires:       rubygem-bson
Requires:       rubygem-mongo
%else
Recommends:     rubygem-bson
Recommends:     rubygem-mongo
%endif

%description
Identify content management systems (CMS), blogging platforms, stats/analytic
packages, JavaScript libraries, servers and more. When you visit a website in
your browser the transaction includes many unseen hints about how the web-server
is set up and what software is delivering the web-page. Some of these hints are
obvious, ex. “Powered by XYZ” and others are more subtle. WhatWeb recognizes
these hints and reports what it finds.


%prep
%autosetup -p 1 -n %{gitname}-%{version}

# Fedora using Rubypick
sed -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|; s|#!/bin/env ruby|#!/usr/bin/ruby|;' \
    whatweb plugin-development/find-common-stuff plugin-development/get-pattern

# Unknown macros in manpage
sed -i -e 's|^.ni||; s|^\./plugins-disabled|+\./plugins-disabled|' whatweb.1

# Disable bundle install in the Makefile
sed -i -e 's|bundle install|#bundle install|' Makefile

# Add the whatweb shared directory + PR282
sed -i -e "s|expand_path(__dir__)), '.')|expand_path(__dir__)), '%{_datadir}/%{name}')|" whatweb

%build
echo "Nothing to build."


%install
alias bundle='echo'
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/%{name}


%files
%doc CHANGELOG.md README.md whatweb.xsl
%license LICENSE
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/addons
%dir %{_datadir}/%{name}/lib
%dir %{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/my-plugins
%dir %{_datadir}/%{name}/plugin-development
%dir %{_datadir}/%{name}/plugins-disabled
%{_datadir}/%{name}/%{name}
%{_datadir}/%{name}/addons/*
%{_datadir}/%{name}/lib/*
%{_datadir}/%{name}/plugins/*
%{_datadir}/%{name}/my-plugins/*
%{_datadir}/%{name}/plugin-development/*
%{_datadir}/%{name}/plugins-disabled/*
%{_mandir}/man1/%{name}.1*


%changelog
* Sun Apr 18 2021 Michal Ambroz <rebus at, seznam.cz> - 0.5.5-1
- bump to 0.5.5, adding mak+sed as BR

* Sun May 31 2020 Michal Ambroz <rebus at, seznam.cz> - 0.5.1-1
- bump to 0.5.1, rebuild for fedora 32

* Wed Oct 30 2019 Michal Ambroz <rebus at, seznam.cz> - 0.5.0-1
- bump to 0.5.0

* Sat Dec 9 2017 Michal Ambroz <rebus at, seznam.cz> - 0.4.9-1
- bump to 0.4.9

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
