Name:           acr
Version:        2.1.4
Release:        1%{?dist}
Group:          Applications/Internet
Summary:        ACR is an autoconf like tool that allows you to create configure scripts for your programs. 


%global         gituser         radareorg
%global         gitname         acr
%global         gitdate         20230513
%global         commit          ac9f0d400a6152d04fa30cffea2c79c29ab156cd
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


License:        GPL-2.0-or-later
URL:            https://github.com/radareorg/acr
# Releases      https://github.com/radareorg/acr/releases
# Source0:      https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make

%description
ACR is an autoconf like tool that allows you to create configure scripts for
your programs. The main aim of this tool is to teach developers how to create
portable builds of their tools, just using generic functions wrapped by acr
to generate portable shellscript.

%prep
#%setup -q -n %{gitname}-%{commit}
%autosetup -n %{gitname}-%{version}



%build
%configure
%make_build



%install
%make_install



%files
%doc %{_datadir}/doc/%{name}
%{_bindir}/acr
%{_bindir}/acr-cat
%{_bindir}/acr-install
%{_bindir}/acr-sh
%{_bindir}/acr-wrap
%{_bindir}/amr
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/modules/csharp.acr
%{_datadir}/%{name}/modules/java-gtk.acr
%{_datadir}/%{name}/modules/sizes.acr
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*


%changelog
* Fri May 17 2024 Michal Ambroz <rebus at, seznam.cz> - 2.1.4-1
- bump to 2.1.4

* Sat Nov 25 2023 Michal Ambroz <rebus at, seznam.cz> - 2.1.1-1
- bump to 2.1.1

* Fri May 14 2021 Michal Ambroz <rebus at, seznam.cz> - 1.9.4-1
- bump to 1.9.4

* Sun Oct 20 2019 Michal Ambroz <rebus at, seznam.cz> - 1.7.2-1
- bump to 1.7.2

* Thu Oct 06 2016 Michal Ambroz <rebus at, seznam.cz> - 0.10.5-1
- bump to 0.10.5

* Sun Oct 11 2015 Michal Ambroz <rebus at, seznam.cz> - 0.9.9-1
- bump to 0.9.9


* Tue Jun  3 2014 Michal Ambroz <rebus at, seznam.cz> - 0.9.6-1
- initial build for Fedora 20

