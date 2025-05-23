Autoreqprov: 0
Name:		tln_tools
Version:	20110729
Release:	1%{?dist}
Summary:	Timeline tools - Open Source code for Windows Forensic Analysis and Incident Response

Group:		Applications/File
License:	GPLv3
URL:		http://code.google.com/p/winforensicaanalysis/downloads/list
Source0:	http://winforensicaanalysis.googlecode.com/files/tln_tools.zip
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Patch0:		%{name}-%{version}-patch-001

Requires:	perl
BuildArch:	noarch

%description
Timeline tools - Open Source code for Windows Forensic Analysis and Incident Response

%prep
mkdir -p $RPM_BUILD_DIR/%{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}/
unzip %{SOURCE0}
%patch0 -p1
for file in *.pl
do
    #convert from CRLF to LF
    perl -pi -e 's/\x0D$//' $file
    #make shebang valid on linux
    perl -pi -e 's?^#!.*?#!/usr/bin/env perl?' $file
done


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_DIR/%{name}-%{version}
for file in *.pl; do install -Dp -m0755 $RPM_BUILD_DIR/%{name}-%{version}/$file %{buildroot}%{_bindir}/`basename $file .pl`; done
rm %{buildroot}%{_bindir}/tln2
rm %{buildroot}%{_bindir}/urlcache


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,0755)
%{_bindir}/*


%changelog
* Tue Aug 2 2011 Morgan Weetman <mweetman@redhat.com> - 20110729-1
- Initial package

