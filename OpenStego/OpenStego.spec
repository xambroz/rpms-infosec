Name:           OpenStego
Version:        0.8.6
Release:        1%{?dist}
Summary:        Free Steganography solution
Summary(fr):    Solution libre pour la steganographie

%global         gituser         syvaidya
%global         gitname         openstego
%global         gitdate         20230130
%global         commit          1414072420e181f40e120c26e08be52608cbf572
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

License:        GPL-2.0-only
URL:            https://www.openstego.com/
VCS:            https://github.com/syvaidya/openstego
# Releases      https://github.com/syvaidya/openstego/releases
# Formerly      http://openstego.sourceforge.net/index.html
# Source0:      http://downloads.sourceforge.net/project/openstego/openstego/openstego-%%{version}/openstego-src-%%{version}.zip
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{gitname}-%{version}.tar.gz
Source1:        openstego.desktop

# Patch the ant build script to build only the binary package out of java sources
Patch0:         %{name}-antbuild.patch

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  ant
BuildRequires:  desktop-file-utils
Requires:       java-headless
Requires:       jpackage-utils


%description
OpenStego is a tool implemented in Java for generic steganography,
with support for password-based encryption of the data. It supports
plugins for various steganographic algorithms.

%description -l fr
OpenStego est un outil implanté en Java pour la steganographie générique,
avec le support de l'encryption des données basé sur mot de passe. Il
supporte les plugins pour des algorithmes steganographiques variés.


%package javadoc
BuildArch: noarch
Requires:  jpackage-utils
Summary:   Javadoc generated documentation for Openstego
Summary(fr):    Documentation javadoc générée pour Openstego

%description javadoc
Javadoc generated documentation for Openstego.

%description javadoc -l fr
Documentation javadoc générée pour Openstego


%prep
%autosetup -n %{gitname}-%{gitname}-%{version} -p 1
find . -name *.class -delete
find . -name *.jar -delete
# Delete file for Windows :
rm -f openstego.bat


%build
ant package doc


%install
mkdir -p %{buildroot}%{_javadir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_javadocdir}/openstego
cp -p ./lib/openstego.jar %{buildroot}%{_javadir}/openstego.jar
cp -p ./src/image/ImagesVectorSource.svg %{buildroot}%{_datadir}/pixmaps/openstego.svg
cp -pr ./doc/api/* %{buildroot}%{_javadocdir}/openstego
%jpackage_script com.openstego.desktop.OpenStego "" "" openstego.jar openstego true

# Install openstego.desktop
desktop-file-install                       \
--dir=%{buildroot}%{_datadir}/applications \
%{SOURCE1}


%files
%doc README
%license LICENSE
%{_bindir}/openstego
%{_javadir}/openstego.jar
%{_datadir}/pixmaps/openstego.svg
%{_datadir}/applications/openstego.desktop

%files javadoc
%doc LICENSE
%{_javadocdir}/openstego/


%changelog
* Sat Nov 04 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.8.6-1
- bump to new upstream version 0.8.6

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0.7.4-6
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0.7.4-5
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 29 2020 Michal Ambroz <rebus _AT seznam.cz> - 0.7.4-1
- bump to new upstream version 0.7.4

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0.7.3-6
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Michal Ambroz <rebus _AT seznam.cz> - 0.7.3-1
- bump to new upstream version 0.7.3

* Fri Feb 16 2018 Michal Ambroz <rebus _AT seznam.cz> - 0.7.2-1
- bump to new upstream version 0.7.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.5.2-13
- Use Requires: java-headless rebuild (#1067528)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.5.2-10
- Add French translation in spec file
- Remove Group tags in spec file

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.5.2-8
- fix categorie error in .desktop file

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-6.1
- fix koji build

* Thu Dec 01 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-6
- rename openstego OpenStego
- change description

* Sun Nov 06 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-5
- remove "defattr" line in javadoc subpackage

* Sat Nov 05 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-4
- fixing directory ownerships
- fixing desktop file errors
- add LICENSE in javadoc subpackage

* Tue Oct 04 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-3
- add javadoc subpackage

* Mon Sep 26 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-2
- clean up spec file

* Sat Sep 24 2011 Matthieu Saulnier <casper.le.fantom@gmail.com> 0.5.2-1
- Initial RPM
