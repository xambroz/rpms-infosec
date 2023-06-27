%global         gituser         sleuthkit
%global         gitname         scalpel
%global         gitdate         20210326
%global         commit          35e1367ef2232c0f4883c92ec2839273c821dd39
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           scalpel
Version:        2.1
Release:        0.rc2.%{shortcommit}%{?dist}.1
Summary:        Fast file carver working on disk images

License:        GPL-2.0-or-later
URL:            https://github.com/sleuthkit/scalpel
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz

BuildRequires: make
BuildRequires:  gcc-c++
BuildRequires:  tre-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
%ifarch %{java_arches}
BuildRequires:  java-devel
%endif

%description
Scalpel is a fast file carver that reads a database of header and footer
definitions and extracts matching files from a set of image files or raw
device files. Scalpel is independent on used file-system and will carve
files from FATx, NTFS, ext2/3, or raw partitions. It is useful for both
digital forensics investigation and file recovery.

%prep
%setup -q -n %{gitname}-%{commit}

#Remove Windows binary files
rm -rf *.exe *.dll

#Modify conf to have some usable configuration out of the box
#In distribution configuration everything is commented out
#Sed script will uncomment common file extensions
sed -i -e "s/^#[ ]*$//;
           s/\t/        /g;
           s/^#   [ ]*\([a-z][a-z] \)/        \1/;
           s/^#   [ ]*\([a-z][a-z][a-z] \)/        \1/;
           s/^#   [ ]*\([a-z][a-z][a-z][a-z] \)/        \1/;
           s/^\(.*case[ ]*size\)/#\1/" %{name}.conf


%build
export CXXFLAGS="-std=c++14 $RPM_OPT_FLAGS"
./bootstrap
%configure --with-pic
%{__make} %{?_smp_mflags} OPTS="%{optflags}"

%install
rm -rf %{buildroot}

make install  DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}
install -m 644 %{name}.conf %{buildroot}/%{_sysconfdir}/
rm -f  %{buildroot}/%{_libdir}/libscalpel*.a
rm -f  %{buildroot}/%{_libdir}/libscalpel*.la

%ldconfig_scriptlets


%files
%doc README Changelog
%license LICENSE-2.0.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/libscalpel_test
%{_mandir}/man1/%{name}.1*
%{_libdir}/libscalpel*.so*


%changelog
* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc2.35e1367.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Michal Ambroz <rebus at, seznam.cz> 2.1-0.rc2.35e1367
- bump to current git snapshot 2.1-0.rc2.35e1367
- do not build java bindings where not possible

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.1-0.rc1.2.47815c2.15
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Jeff Law <law@redhat.com> - 2.1-0.rc1.2.47815c2.10
- Force C++14 as this code is not C++17 ready

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.1-0.rc1.2.47815c2.9
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.2.47815c2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 29 2016 Michal Ambroz <rebus at, seznam.cz> 2.1-0.rc1.2.47815c2
- change dependency from java to java-devel

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-0.rc1.1.47815c2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 11 2015 Michal Ambroz <rebus at, seznam.cz> 2.1-0.rc1.1.47815c2
- bump to new pre-release 2.1-0.rc1.1.47815c2

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 03 2011 Michal Ambroz <rebus at, seznam.cz> 2.0-1
- bump to new release 2.0-1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 24 2010 Michal Ambroz <rebus at, seznam.cz> 1.60-3
- remove redundant attr permission definitions
- regenerate patch

* Tue Aug 24 2010 Michal Ambroz <rebus at, seznam.cz> 1.60-2
- fix package review issues

* Fri Apr 09 2010 Michal Ambroz <rebus at, seznam.cz> 1.60-1
- initial build for Fedora

