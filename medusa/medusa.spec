Summary:        Parallel brute forcing password cracker
Name:           medusa
Version:        2.2
%global         baserelease     23
License:        GPLv2
URL:            http://www.foofus.net/jmk/medusa/medusa.html
#               https://github.com/jmk-foofus/medusa/releases


%define         gituser         jmk-foofus
%define         gitname         medusa
%global         gitdate         20220728
%global         commit          079696350faa1dadbd581d30970bb9ba75068748
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Build source is tarball release=1 or git commit=0
%global         build_release   0

%if 0%{?build_release}  > 0
# Build from the targball release
Release:        %{baserelease}%{?dist}
#Source0:       http://www.foofus.net/jmk/tools/%{name}-%{upversion}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

%else
# Build from the git commit snapshot
# Release is not starting with 0 as usual, because the next release will be 1.6
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif
#build_release




BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: apr-devel libssh2-devel
BuildRequires: subversion-devel libpq-devel pcre-devel
BuildRequires: afpfs-ng-devel libgcrypt-devel
BuildRequires: perl-Carp
BuildRequires: freerdp-devel
BuildRequires: openssl-devel


%description
Medusa is a speedy, massively parallel, modular,
login brute-forcer for network services.
Some of the key features of Medusa are:

    * Thread-based parallel testing. Brute-force
      testing can be performed against multiple hosts,
      users or passwords concurrently.
    * Flexible user input. Target information
      (host/user/password) can be specified in a variety of ways.
      For example, each item can be either a single
      entry or a file containing multiple entries.
      Additionally, a combination file format allows
      the user to refine their target listing.
    * Modular design. Each service module exists
      as an independent .mod file.
      This means that no modifications are necessary
      to the core application in order to extend
      the supported list of services for brute-forcing.

%prep
%if 0%{?build_release} > 0
# Build from tarball release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif


%build
autoreconf -vif

# required type off64_t is not available under all environments, ugly hack for ugly system headers
export CPPFLAGS="-Doff64_t=__off64_t %{optflags} -fcommon"
export CFLAGS="-Doff64_t=__off64_t %{optflags} -fcommon"
%{configure} --enable-module-afp=yes --with-default-mod-path=%{_libdir}/medusa/modules

make %{?_smp_mflags} V=1

%install
# required type off64_t is not available under all environments, ugly hack for ugly system headers
export CPPFLAGS="-Doff64_t=__off64_t %{optflags}" ; export CFLAGS="-Doff64_t=__off64_t %{optflags}"
make DESTDIR=%{buildroot} install
 
%files
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_libdir}/medusa
%{_libdir}/medusa/*

%changelog
* Sun Apr 12 2020 Michal Ambroz <rebus AT seznam.cz> - 2.2-23.20220728git0796963
- bump to current git snapshot from 20220728

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-22.20181216git292193b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 2.2-21.20181216git292193b
- Rebuild for updated FreeRDP.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-20.20181216git292193b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-19.20181216git292193b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.2-18.20181216git292193b
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-17.20181216git292193b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 15 2021 Simone Caronni <negativo17@gmail.com> - 2.2-16.20181216git292193b
- Rebuild for updated FreeRDP.

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 2.2-15.20181216git292193b
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-14.20181216git292193b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-13.20181216git292193b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Simone Caronni <negativo17@gmail.com> - 2.2-12.20181216git292193b
- Rebuild for updated FreeRDP.
- Fix for "warning: extra tokens at the end of endif directive in line 34".

* Sun Apr 12 2020 Michal Ambroz <rebus AT seznam.cz> - 2.2-11.20181216git292193b
- switch to git commit to be able to build with contemporary openssl

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 13 2017 Michal Ambroz <rebus _AT seznam.cz> - 2.2-3
- Fix FTBFS by using compat-openssl10.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 04 2016 Michal Ambroz <rebus AT seznam.cz> - 2.2-1
- bump to official 2.2 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-0.rc1.4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 20 2015 Kalev Lember <klember@redhat.com> - 2.2-0.rc1.4.2
- Rebuilt for freerdp soname bump

* Sun Oct 11 2015 Michal Ambroz <rebus AT seznam.cz> - 2.2-0.rc1.4
- bug 1262258 - explicit libs for 64bit no longer needed

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.rc1.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Michal Ambroz <rebus AT seznam.cz> - 2.2-0.rc1.3
- improve Freerdp detection

* Fri May 29 2015 Michal Ambroz <rebus AT seznam.cz> - 2.2-0.rc1.2
- add dependency to Freerdp

* Thu May 28 2015 Michal Ambroz <rebus AT seznam.cz> - 2.2-0.rc1
- update to version 2.2 rc1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.1-2
- drop ncpfs as no longer in Fedora
- Cleanup spec

* Sat Feb 02 2013 Michal Ambroz <rebus AT seznam.cz> - 2.1.1-1
- update to version 2.1.1

* Sat Feb 02 2013 Michal Ambroz <rebus AT seznam.cz> - 2.1-3
- fix buffer overflow in medusa-trace.c related to printing special chars in hex formatting

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Michal Ambroz <rebus AT seznam.cz> - 2.1-1
- bump to version 2.1

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0-3
- Rebuild against PCRE 8.30
- Fix compilation with newer GCC

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.0-1
- Bump version to 2.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.5-11
- bump for libssh2 rebuild

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.5-10
- rebuild for libssh2 1.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.5-9
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Jan F. Chadima <jchadima@redhat.com> - 1.5-7
- enable afpfs_ng backend

* Tue Mar 24 2009 Jan F. Chadima <jchadima@redhat.com> - 1.5-5
- drop empty NEWS file

* Fri Mar 20 2009 Jan F. Chadima <jchadima@redhat.com> - 1.5-4
- fix license type
- fix description

* Fri Mar 20 2009 Jan F. Chadima <jchadima@redhat.com> - 1.5-3
- add missing build reqs

* Thu Mar 19 2009 Jan F. Chadima <jchadima@redhat.com> - 1.5-2
- repair summary and url according to recomendations
- switch afp support off by default

* Mon Mar 16 2009 Jan F. Chadima <jchadima@redhat.com> - 1.5-1
- initial build
