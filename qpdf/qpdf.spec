Summary: Command-line tools and library for transforming PDF files
Name:    qpdf
Version: 8.0.0
Release: 2%{?dist}
# MIT: e.g. libqpdf/sha2.c
License: Artistic 2.0
URL:     http://qpdf.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/qpdf/qpdf-%{version}.tar.gz

Patch0:  qpdf-doc.patch

# gcc and gcc-c++ are no longer in buildroot by default
# gcc is needed for qpdf-ctest.c
BuildRequires: gcc
# gcc-c++ is need for everything except for qpdf-ctest
BuildRequires: gcc-c++

BuildRequires: zlib-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: pcre-devel

# for fix-qdf and test suite
BuildRequires: perl-interpreter
BuildRequires: perl-generators
BuildRequires: perl(Digest::MD5)

# for autoreconf
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%package libs
Summary: QPDF library for transforming PDF files

%package devel
Summary: Development files for QPDF library
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%package doc
Summary: QPDF Manual
BuildArch: noarch
Requires: %{name}-libs = %{version}-%{release}

%description
QPDF is a command-line program that does structural, content-preserving
transformations on PDF files. It could have been called something
like pdf-to-pdf. It includes support for merging and splitting PDFs
and to manipulate the list of pages in a PDF file. It is not a PDF viewer
or a program capable of converting PDF into other formats.

%description libs
QPDF is a C++ library that inspect and manipulate the structure of PDF files.
It can encrypt and linearize files, expose the internals of a PDF file,
and do many other operations useful to PDF developers.

%description devel
Header files and libraries necessary
for developing programs using the QPDF library.

%description doc
QPDF Manual

%prep
%setup -q

# fix 'complete manual location' note in man pages
%patch0 -p1 -b .doc

sed -i -e '1s,^#!/usr/bin/env perl,#!/usr/bin/perl,' qpdf/fix-qdf

%build
# work-around check-rpaths errors
autoreconf --verbose --force --install

%configure --disable-static \
           --enable-show-failed-test-output

%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/libqpdf.la

%check
make check

%ldconfig_scriptlets libs

%files
%{_bindir}/fix-qdf
%{_bindir}/qpdf
%{_bindir}/zlib-flate
%{_mandir}/man1/*

%files libs
%doc README.md TODO ChangeLog
%license Artistic-2.0
%{_libdir}/libqpdf.so.21*

%files devel
%doc examples/*.cc examples/*.c
%{_includedir}/qpdf/
%{_libdir}/libqpdf.so
%{_libdir}/pkgconfig/libqpdf.pc

%files doc
%{_pkgdocdir}


%changelog
* Tue Feb 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 8.0.0-2
- use %%license, %%ldconfig_scriptlets, %%make_build, %%make_install
- %%files: track files more closely, libqpdf soname in particular

* Mon Feb 26 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.0-1
- rebase to 8.0.0

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 7.1.1-4
- gcc and gcc-c++ are no longer in buildroot by default

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 7.1.1-2
- remove old stuff

* Mon Feb 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 7.1.1-1
- rebase to 7.1.1

* Tue Sep 19 2017 Zdenek Dohnal <zdohnal@redhat.com> - 7.0.0-1
- rebase to 7.0.0

* Fri Aug 11 2017 Zdenek Dohnal <zdohnal@redhat.com> - 6.0.0-10
- adding patches for CVE back (cups-filters needed to rebuild)

* Mon Aug 07 2017 Zdenek Dohnal <zdohnal@redhat.com> - 6.0.0-9
- removing patches for CVEs, because they break other things now

* Thu Aug 03 2017 Zdenek Dohnal <zdohnal@redhat.com> - 6.0.0-8
- 1477213 - Detect recursions loop resolving objects
- 1454820 - CVE-2017-9208
- 1454820 - CVE-2017-9209
- 1454820 - CVE-2017-9210

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 03 2016 Jiri Popelka <jpopelka@redhat.com> - 6.0.0-3
- %%{_defaultdocdir}/qpdf/ -> %%{_pkgdocdir}

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Jiri Popelka <jpopelka@redhat.com> - 6.0.0-1
- 6.0.0

* Mon Nov 09 2015 Jiri Popelka <jpopelka@redhat.com> - 5.2.0-1
- 5.2.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Jiri Popelka <jpopelka@redhat.com> - 5.1.3
- New upstream release 5.1.3

* Tue Apr 14 2015 Jiri Popelka <jpopelka@redhat.com> - 5.1.2-5
- rebuilt

* Mon Feb 16 2015 Jiri Popelka <jpopelka@redhat.com> - 5.1.2-4
- rebuilt

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Jiri Popelka <jpopelka@redhat.com> - 5.1.2-2
- Use %%_defaultdocdir instead of %%doc

* Mon Jun 09 2014 Jiri Popelka <jpopelka@redhat.com> - 5.1.2-1
- 5.1.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Jiri Popelka <jpopelka@redhat.com> - 5.1.1-1
- 5.1.1

* Wed Dec 18 2013 Jiri Popelka <jpopelka@redhat.com> - 5.1.0-1
- 5.1.0

* Mon Oct 21 2013 Jiri Popelka <jpopelka@redhat.com> - 5.0.1-1
- 5.0.1

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 5.0.0-4
- Perl 5.18 rebuild

* Mon Jul 22 2013 Jiri Popelka <jpopelka@redhat.com> - 5.0.0-3
- change shebang to absolute path (#987040)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.0.0-2
- Perl 5.18 rebuild

* Thu Jul 11 2013 Jiri Popelka <jpopelka@redhat.com> - 5.0.0-1
- 5.0.0

* Mon Jul 08 2013 Jiri Popelka <jpopelka@redhat.com> - 4.2.0-1
- 4.2.0

* Thu May 23 2013 Jiri Popelka <jpopelka@redhat.com> - 4.1.0-3
- fix 'complete manual location' note in man pages (#966534)

* Tue May 07 2013 Jiri Popelka <jpopelka@redhat.com> - 4.1.0-2
- some source files are under MIT license

* Mon Apr 15 2013 Jiri Popelka <jpopelka@redhat.com> - 4.1.0-1
- 4.1.0

* Tue Mar 05 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0.1-3
- work around gcc 4.8.0 issue on ppc64 (#915321)
- properly handle overridden compressed objects

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jiri Popelka <jpopelka@redhat.com> 4.0.1-1
- 4.0.1

* Wed Jan 02 2013 Jiri Popelka <jpopelka@redhat.com> 4.0.0-1
- 4.0.0

* Fri Sep 07 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.2-1
- 3.0.2

* Thu Aug 16 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.1-3
- the previously added requirement doesn't need to be arch-specific

* Thu Aug 16 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.1-2
- doc subpackage requires libs subpackage due to license file (#848466)

* Wed Aug 15 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.1-1
- initial spec file
