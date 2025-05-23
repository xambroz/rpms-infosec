%define debug_package %{nil}

Summary:	silk-ipa - SiLK with the IPA Suite and PostgreSQL

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		silk-ipa
Version:	1.0
Release:	1%{?dist}
URL:		http://www.cert.org/forensics/repository

License:	GPL

Group:		Applications/Forensics Tools
Source:		%{name}.tar.gz

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}
BuildArch:	noarch

%description
This package contains a script named EnableSilkWithIPA that 
enables the forensics-sip (Silk with Ipa and Postgresql)
repostory, installs needed packages, and then provides a
URL to configure these tools

%prep
%setup -n %{name}

%build
echo Nothing to build

%install
%{__install} -Dp -m755 EnableSilkWithIPA %{buildroot}%{_bindir}/EnableSilkWithIPA

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc 
%attr(755, root, root)	%{_bindir}/EnableSilkWithIPA

%changelog
* Wed Mar 26 2014 Lawrence R. Rogers <lrr@cert.org> 1.0-1
- Initial release
