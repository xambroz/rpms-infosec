Name:		pdfresurrect
Version:	0.14
Summary:	PDF Analysis and Scrubbing Utility
Group:		Applications/Productivity
License:	GPLv3+
URL:		http://www.757labs.org/projects/pdfresurrect/

%global         gituser         enferex
%global         gitname         pdfresurrect
%global         commit          6ee7a1534bd862e5397f0fe1aba5d6dd1a39249f
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:	1%{?dist}
#Source0:	http://www.757labs.org/projects/pdfresurrect/releases/pdfresurrect-v0_12.tar.bz2
#Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# https://github.com/enferex/pdfresurrect/pull/2/commits/bf9779eb189ce1268fe66d146adcf960fb5afecf.patch
Patch0:         pdfresurrect-fixinstall.patch


%description
PDFResurrect is a tool aimed at analyzing PDF documents. The PDF format
allows for previous document changes to be retained in a more recent
version of the document, thereby creating a running history of changes
for the document. This tool attempts to extract all previous versions
while also producing a summary of changes between versions. This tool
can also "scrub" or write data over the original instances of PDF objects
that have been modified or deleted, in an effort to disguise information
from previous versions that might not be intended for anyone else to read.


%prep
#autosetup -p 1 -n %{gitname}-%{commit} -S git
%autosetup -p 1 -n %{gitname}-%{version} -S git

sed -i 's|@CFLAGS@|%{optflags}|' Makefile.in


%build
%configure
%make_build CFLAGS="%{optflags}"


%install
make install DESTDIR="%{buildroot}"

%files
%doc AUTHORS README
%license LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*


%changelog
* Mon May 07 2018 Michal Ambroz <rebus AT_ seznam.cz> - 0.14-1
- bump to latest upstream version

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.12-1
- Ver. 0.12 (bugfix release)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.11-1
- Ver. 0.11 (bugfix release)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 23 2010 Peter Lemenkov <lemenkov@gmail.com> 0.10-1
- Ver. 0.10

* Thu Nov 12 2009 Peter Lemenkov <lemenkov@gmail.com> 0.9-1
- Ver. 0.9

* Wed Oct 28 2009 Peter Lemenkov <lemenkov@gmail.com> 0.8-1
- Ver. 0.8

* Thu Sep 10 2009 Peter Lemenkov <lemenkov@gmail.com> 0.7-1
- Ver. 0.7

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009 Peter Lemenkov <lemenkov@gmail.com> 0.6-1
- Ver. 0.6

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 22 2008 Peter Lemenkov <lemenkov@gmail.com> 0.04-1
- Initial package

