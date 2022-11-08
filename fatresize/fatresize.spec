%global         gituser         ya-mouse
%global         gitname         fatresize
%global         commit          321973ba156bbf2489e82c47c94b2bca74b16316
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           fatresize
Version:        1.1.0
# Build from git commit
# Release:       0.1.git%%{shortcommit}%%{?dist}
# Build from git release version
Release:        6%{?dist}
License:        GPLv3+
Summary:        FAT16/FAT32 resizer
URL:            https://github.com/ya-mouse/fatresize
#               http://sourceforge.net/projects/fatresize/
# Build from git commit
# Source0:       https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
# Build from git release version
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  parted-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  docbook-utils
BuildRequires:  w3m
BuildRequires: make

%description
The FAT16/FAT32 non-destructive resizer.

%prep
# Build from git commit
# setup -q -n %%{gitname}-%%{commit}
# Build from git release version
%setup -q -n %{gitname}-%{version}

#docbook-to-man not available in Fedora
sed -i -e 's|docbook-to-man|docbook2man|;' Makefile.am

%build
autoreconf -ifv
%configure
%make_build

%install
%make_install

%files
%doc AUTHORS ChangeLog README
%license COPYING
%{_sbindir}/*
%{_mandir}/man1/*

%changelog
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Apr 05 2020 Michal Ambroz <rebus _AT seznam.cz> - 1.1.0-1
- update to release version 1.1.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Michal Ambroz <rebus _AT seznam.cz> - 1.0.4-1
- update to release version 1.0.4

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7.git20161118
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6.git20161118
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5.git20161118
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Nov 18 2016 Michal Ambroz <rebus _AT seznam.cz> - 1.0.3-4.git20161118
- witch to new github repository https://github.com/ya-mouse/fatresize

* Fri Nov 18 2016 Michal Ambroz <rebus _AT seznam.cz> - 1.0.3-3.git20100729
- include license

* Thu Nov 17 2016 Michal Ambroz <rebus _AT seznam.cz> - 1.0.3-2.git20100729
- review changes #1395955 - dist-tag, group, make macro, cosmetics
- fix generation/installation of man-page

* Wed Nov 16 2016 Michal Ambroz <rebus _AT seznam.cz> - 1.0.3-1.git20100729
- update to latest git

* Wed Feb 25 2015 Huaren Zhong <huaren.zhong@gmail.com> - 1.0.3
- Rebuild for Fedora

* Mon Apr 15 2013 Dmitry V. Levin (QA) <qa_ldv@altlinux.org> 1.0.3-alt11.git20090730.qa1
- NMU: rebuilt for debuginfo.

* Thu Apr 01 2010 Eugeny A. Rostovtsev (REAL) <real at altlinux.org> 1.0.3-alt11.git20090730
- Version 1.0.3

* Sun Aug 10 2008 Led <led@altlinux.ru> 1.0.2-alt11
- fixed spec
- added name-1.0.2-alt.patch

* Wed Aug 15 2007 Led <led@altlinux.ru> 1.0.2-alt10
- rebuild with libparted-1.8.so.8
- fixed License

* Mon May 14 2007 Led <led@altlinux.ru> 1.0.2-alt9
- rebuild with libparted-1.8.so.7

* Sun Mar 25 2007 Led <led@altlinux.ru> 1.0.2-alt8
- rebuild with libparted-1.8.so.6

* Mon Mar 19 2007 Led <led@altlinux.ru> 1.0.2-alt7
- rebuild with libparted-1.8.so.4
- added name-1.0.2+libparted-1.8.3.patch

* Tue Jan 16 2007 Led <led@altlinux.ru> 1.0.2-alt6
- rebuild with libparted-1.8.so.2

* Mon Nov 27 2006 Led <led@altlinux.ru> 1.0.2-alt5
- rebuild with libparted-1.8.so.0
- added docs

* Wed Jul 05 2006 ALT QA Team Robot <qa-robot@altlinux.org> 1.0.2-alt4.1
- NMU: rebuild with libparted-1.7.so.1

* Tue Sep 20 2005 Kachalov Anton <mouse@altlinux.ru> 1.0.2-alt4
- LFS support

* Mon Sep 19 2005 Kachalov Anton <mouse@altlinux.ru> 1.0.2-alt3
- restore original partition geometry while resizing EVMS partition

* Thu Sep 15 2005 Kachalov Anton <mouse@altlinux.ru> 1.0.2-alt2
- added default name translation of EVMS partitions
- synced resize code with new cmd-line parted utility 1.6.24

* Wed Sep 07 2005 Kachalov Anton <mouse@altlinux.ru> 1.0.2-alt1
- tell k|M|G and ki|Mi|Gi suffixes
- proper filesystem information
- resize partition only for non-EVMS partitions

* Wed Apr 13 2005 Kachalov Anton <mouse@altlinux.ru> 1.0.1-alt1
- removed translation option: fix new geometry boundary

* Mon Apr 11 2005 Anton D. Kachalov <mouse@altlinux.org> 1.0-alt2
- added translating option

* Fri Apr 08 2005 Anton D. Kachalov <mouse@altlinux.org> 1.0-alt1
- first build
