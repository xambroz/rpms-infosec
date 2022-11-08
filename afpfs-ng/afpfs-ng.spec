Name:           afpfs-ng
Version:        0.8.1
Release:        40%{?dist}
Summary:        Apple Filing Protocol client


# by default build with the fuse module
# rpmbuild --rebuild afpfs-ng.src.rpm --without fuse
%bcond_without     fuse


License:        GPL+
URL:            http://alexthepuffin.googlepages.com/home
Source0:        http://downloads.sourceforge.net/afpfs-ng/%{name}-%{version}.tar.bz2
Patch0:         afpfs-ng-0.8.1-overflows.patch
Patch1:         afpfs-ng-0.8.1-pointer.patch
# Sent by e-mail to Alex deVries <alexthepuffin@gmail.com>
Patch2:         afpfs-ng-0.8.1-formatsec.patch
Patch3:         afpfs-ng-0.8.1-longoptions.patch

%{?with_fuse:BuildRequires: fuse-devel}
BuildRequires: gcc
BuildRequires: libgcrypt-devel gmp-devel readline-devel
BuildRequires: make
BuildRequires: libtool
BuildRequires: autoconf


%description
A command line client to access files exported from Mac OS system via
Apple Filing Protocol.
%{?with_fuse:The FUSE filesystem module for AFP is in fuse-afp package}


%if 0%{?with_fuse}
%package -n fuse-afp
Summary:        FUSE driver for AFP filesystem

%description -n fuse-afp
A FUSE file system server to access files exported from Mac OS system
via AppleTalk or TCP using Apple Filing Protocol.
The command line client for AFP is in fuse-afp package
%endif


%package devel
Summary:        Development files for afpfs-ng
Requires:       %{name} = %{version}

%description devel
Library for dynamic linking and header files of afpfs-ng.

%prep
%autosetup -p 1
libtoolize
autoreconf

%build
# make would rebuild the autoconf infrastructure due to the following:
# Prerequisite `configure.ac' is newer than target `Makefile.in'.
# Prerequisite `aclocal.m4' is newer than target `Makefile.in'.
# Prerequisite `configure.ac' is newer than target `aclocal.m4'.
touch --reference aclocal.m4 configure.ac Makefile.in

export CFLAGS="${RPM_OPT_FLAGS} -fcommon" 
%configure %{?!with_fuse:--disable-fuse} --disable-static
make %{?_smp_mflags}


%install
%make_install
install -d %{buildroot}%{_includedir}/afpfs-ng
cp -p include/* %{buildroot}%{_includedir}/afpfs-ng
# libtool .la file works different in different versions of libtool, should not be packaged
[ -f %{buildroot}%{_libdir}/libafpclient.la ] && rm -f %{buildroot}%{_libdir}/libafpclient.la

%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%ldconfig_scriptlets
%endif


%files
%license COPYING
%{_bindir}/afpcmd
%{_bindir}/afpgetstatus
%{_mandir}/man1/afpcmd.1*
%{_mandir}/man1/afpgetstatus.1*
%{_libdir}/libafpclient.so.*
%doc AUTHORS ChangeLog docs/README docs/performance docs/FEATURES.txt docs/REPORTING-BUGS.txt


%if 0%{?with_fuse}
%files -n fuse-afp
%license COPYING
%{_bindir}/afp_client
%{_bindir}/afpfs
%{_bindir}/afpfsd
%{_bindir}/mount_afp
%{_mandir}/man1/afp_client.1*
%{_mandir}/man1/afpfsd.1*
%{_mandir}/man1/mount_afp.1*
%doc AUTHORS ChangeLog
%endif


%files devel
%{_includedir}/afpfs-ng
%{_libdir}/*.so

%changelog
* Tue Oct 25 2022 Michal Ambroz <rebus _AT seznam.cz> - 0.8.1-40
- remove the libafpclient.la libtool file

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 17 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.8.1-37
- update embedded libtool (ltmain.sh)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.8.1-35
- modernize spec, push the bugfix to active branches

* Fri Mar 12 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.8.1-34
- fix issue 1507944

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-32
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 22 2020 Michal Ambroz <rebus _AT seznam.cz> - 0.8.1-30
- fix FTBFS - multiple definition of - build legacy code with -fcommon

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.1-27
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Nov 25 2014 <hguemar@fedoraproject.org> - 0.8.1-18
- Fix mount_afp crash (RHBZ #1165296)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tomáš Mráz <tmraz@redhat.com> - 0.8.1-15
- Rebuild for new libgcrypt

* Wed Dec 04 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-14
- Fix build with -Werror=format-security

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-13.3
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-12.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-11.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.1-8.3
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 0.8.1-8.2
- rebuild with new gmp

* Mon Sep 26 2011 Peter Schiffer <pschiffe@redhat.com> - 0.8.1-8.1
- rebuild with new gmp

* Mon Jul  4 2011 Jan F. Chadima <jchadima@redhat.com> - 0.8.1-8
- Repair ponter arithmetic

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.8.1-6
- Rebuild with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-4
- Don't refer to AppleTalk in Summary

* Tue Jul 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-3
- Fix up license tag

* Thu Mar 19 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-2
- Add more include files (Jan F. Chadima)
- Don't needlessly build static library (Stefan Kasal)
- Fix fuse-afp summary (Stefan Kasal)
- Remove redundant license file from -devel (Stefan Kasal)

* Mon Oct 6 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.8.1-1
- Initial packaging attempt
