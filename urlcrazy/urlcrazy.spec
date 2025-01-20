Name:           urlcrazy
Version:        0.7.3
Release:        %autorelease
Summary:        Generate and test domain typos and variations to detect typo squatting
License:        GPLv3
URL:            http://www.morningstarsecurity.com/research/urlcrazy
VCS:            git:https://github.com/urbanadventurer/urlcrazy

Group:          Applications/Internet

%global         gituser         urbanadventurer
%global         gitname         urlcrazy
%global         gitdate         20210414
%global         commit          93e910c4ab76dec8cc989d3b9db465ffa266bf5e


# Source0:      http://www.morningstarsecurity.com/downloads/%{name}-%{version}.tar.gz
# Source0:      https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildArch:      noarch

# Switch to ruby 1.9.x
# Patch3:         %{name}-ruby19.patch

Requires:       /usr/bin/ruby


%description
Generate and test domain typos and variations to detect and perform typo
squatting, URL hijacking, phishing, and corporate espionage.


%prep
#%%autosetup -p 1 -n %{gitname}-%{commit}
%autosetup -p 1 -n %{name}-%{version}


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
%{?%autochangelog: %autochangelog }
