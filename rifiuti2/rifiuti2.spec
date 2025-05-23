%define debug_package %{nil}

Summary:	Examine the contents of INFO2 in the Windows Recycle bin

Packager:	Lawrence R. Rogers

Vendor:		cert.org
Name:		rifiuti2
Version:	0.7.0
Release:	20%{?dist}
URL:		https://abelcheung.github.io/rifiuti2/

License:	GPL

Group:		Applications/Forensics Tools

Source:		%{name}-%{version}.tar.gz
Patch1:		%{name}-%{version}-patch-001

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version} 
BuildRequires:	gcc-c++, libstdc++-devel glib2-devel
BuildRequires:	autoconf automake pkgconfig gettext-devel libtool

%description
Rifiuti, the Italian word meaning "trash", was developed to examine
the contents of the INFO2 file in the Recycle Bin. Rifiuti will parse
the information in an INFO2 file and output the results in a field
delimited manner so that it may be imported into your favorite spreadsheet
program. Rifiuti is built to work on multiple platforms and will execute
on Windows (through Cygwin), Mac OS X, Linux, and *BSD platforms.

%prep
%autosetup -n %{name}-%{version}

%build
if [ -f autogen.sh ]; then sh autogen.sh; else autoreconf -f -i -v; fi
%configure 
%{__make}

%install
%makeinstall
/bin/mv %{buildroot}%{_bindir}/rifiuti %{buildroot}%{_bindir}/rifiuti2
cd %{buildroot}/%{_mandir}/man1/; /bin/mv rifiuti.1 rifiuti2.1; /bin/rm rifiuti-vista.1; /bin/ln -s rifiuti2.1 rifiuti-vista.1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc 
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/zh_HK/LC_MESSAGES/rifiuti2.mo

%changelog
* Mon Nov  8 2021 Lawrence R. Rogers <lrr@cert.org) 0.7.0-20
* Release 0.7.0-20
	Version 0.7.0-20: rev to so as to not conflict with Fedora updates

* Fri Oct 30 2020 Lawrence R. Rogers <lrr@cert.org) 0.7.0-5
* Release 0.7.0-5
	Version 0.7.0-5: rev to so as to not conflict with Fedora updates

* Tue May  5 2020 Lawrence R. Rogers <lrr@cert.org) 0.7.0-4
* Release 0.7.0-4
	Version 0.7.0-4: rev to so as to not conflict with Fedora updates

* Mon Nov  4 2019 Lawrence R. Rogers <lrr@cert.org) 0.7.0-3
* Release 0.7.0-3
	Version 0.7.0-3: rev to so as to not conflict with Fedora updates

* Thu Jul  4 2019 Lawrence R. Rogers <lrr@cert.org) 0.7.0-2
* Release 0.7.0-2
	Version 0.7.0-2: rev to so as to not conflict with Fedora updates

* Thu May 21 2015 Lawrence R. Rogers <lrr@cert.org) 0.6.1-1
* Release 0.6.1-1
	Version 0.6.1

