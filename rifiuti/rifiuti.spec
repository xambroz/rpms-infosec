%define debug_package %{nil}

Summary:	Examine the contents of INFO2 in the Windows Recycle bin

Packager:	Lawrence R. Rogers

Vendor:		cert.org
Name:		rifiuti
Version:	20040505_1
Release:	1%{?dist}
URL:		http://www.mcafee.com/us/downloads/free-tools/rifiuti.aspx

License:	GPL

Group:		Applications/Forensics Tools

Source:		%{name}_%{version}.tar.gz

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version} 
BuildRequires:	gcc-c++, libstdc++-devel

%description
Rifiuti, the Italian word meaning "trash", was developed to examine
the contents of the INFO2 file in the Recycle Bin. Rifiuti will parse
the information in an INFO2 file and output the results in a field
delimited manner so that it may be imported into your favorite spreadsheet
program. Rifiuti is built to work on multiple platforms and will execute
on Windows (through Cygwin), Mac OS X, Linux, and *BSD platforms.

%prep
%setup -n %{name}_%{version}/src

%build
%{__make}

%install
%__install -Dp %{name} %{buildroot}%{_bindir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc 
%attr(555,bin,bin)	%{_bindir}/rifiuti

%changelog
