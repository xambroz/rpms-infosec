Name:           urlcrazy
Version:        0.7.3
Release:        %autorelease
Summary:        Generate and test domain typos and variations to detect typo squatting

Group:          Applications/Internet

%global         gituser         urbanadventurer
%global         gitname         urlcrazy
%global         gitdate         20210414
%global         commit          93e910c4ab76dec8cc989d3b9db465ffa266bf5e


License:        GPLv3
URL:            http://www.morningstarsecurity.com/research/urlcrazy
VCS:            https://github.com/urbanadventurer/urlcrazy
# Source0:        http://www.morningstarsecurity.com/downloads/%{name}-%{version}.tar.gz
#Source0:         https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:         https://github.com/%{gituser}/%{gitname}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


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
%autochangelog
