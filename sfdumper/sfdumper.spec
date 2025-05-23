%define debug_package %{nil}

Summary:	A Selective File Dumper program built on top of the Sleuthkit

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		sfdumper
Version:	2.2
Release:	1%{?dist}
URL:		http://sfdumper.sourceforge.net/

License: GPL

Group: Applications/Forensics Tools

Source0:	%{name}_v%{version}.zip
Requires:	sleuthkit foremost md5deep afflib afftools libewf mount_ewf
BuildArch:	noarch
BuildRoot:	%{buildroot}
Patch1: 	sfdumper-patch-001

%description
SFDumper is a Selective File Dumper program built on top of the Sleuthkit.
There is a windowed interface named sfdumper-gui.

%prep
pwd
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
unzip -o $RPM_SOURCE_DIR/%{name}_v%{version}.zip
%patch1 -p1

%build

%install
cd %{name}-%{version}
%__install -d %{buildroot}%{_bindir}
%__install %{name}.sh %{buildroot}%{_bindir}/%{name}
%__install -d %{buildroot}%{_docdir}/%{name}
%__install Readme_EN_.txt %{buildroot}%{_docdir}/%{name}/README.txt

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%attr(555,bin,bin)	%{_bindir}/%{name}
%attr(444,bin,bin)	%{_docdir}/%{name}/*

%changelog
