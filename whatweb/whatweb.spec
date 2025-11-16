Name:           whatweb
Version:        0.6.3
Release:        %autorelease
Summary:        Web scanner to identify what are the websites running
License:        GPL-2.0-or-later
URL:            http://www.morningstarsecurity.com/research/whatweb
#               https://github.com/urbanadventurer/WhatWeb/releases


# The tests are normally disabled in the build phase as whatweb is networking
# tool and Fedora has networking disabled during builds
# In order to try rebuild with tests locally run
# rpmbuild --rebuild whatweb*.src.rpm --with tests
%bcond_with     tests


%global         gituser         urbanadventurer
%global         gitname         WhatWeb
%global         gitdate         20251018
%global         commit          4dceb388015909e97567bcf58a7edaf7eda61593
%global         giturl          https://github.com/%{gituser}/%{gitname}
VCS:            git:%{giturl}

%if 0%{?rhel}
Group:          Applications/Internet
%endif


Source0:        %{giturl}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

Buildrequires:  make
Buildrequires:  sed

# Requires:     ruby(abi) >= 2.0
Requires:       /usr/bin/ruby
Requires:       rubygem-addressable

# On RHEL7 the Recommends statement is not available
%if 0%{?rhel} && 0%{?rhel} <= 8
Requires:       rubygem-bson
Requires:       rubygem-mongo
%else
Recommends:     rubygem-bson
Recommends:     rubygem-mongo
%endif

%if %{with tests}
Requires:       rubygem-minitest
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

# Remove IP2Country database with problematic license
# Reported upstream https://github.com/urbanadventurer/WhatWeb/issues/366
echo "" > plugins/IpToCountry.csv

# Fedora using Rubypick
sed -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|; s|#!/bin/env ruby|#!/usr/bin/ruby|;' \
    whatweb plugin-development/find-common-stuff plugin-development/get-pattern

# Remove unknown macros in manpage - probably Ubuntu specific macros
sed -i -e 's|^\.ni||; s|^\./plugins-disabled|+\./plugins-disabled|' whatweb.1

# Disable bundle install in the Makefile
sed -i -e 's|bundle install|#bundle install|' Makefile

# Add the whatweb shared directory
sed -i -e "s|expand_path(__dir__)), '.')|expand_path(__dir__)), '%{_datadir}/%{name}')|" whatweb

%build
echo "Nothing to build."


%install
%make_install

rm -rf %{buildroot}%{_datadir}/doc/%{name}

# Move the executable from share to bin
rm -f %{buildroot}%{_bindir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# addons and plugin-development not crucial for runtime, move them to documentation
rm -rf %{buildroot}%{_datadir}/%{name}/addons
rm -rf %{buildroot}%{_datadir}/%{name}/plugin-development

chmod -x addons/*
chmod -x plugin-development/*

%check
%if %{with tests}
ruby test/integration.rb
%endif


%files
%license LICENSE
%doc CHANGELOG.md README.md whatweb.xsl
%doc addons
%doc plugin-development
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
%autochangelog

