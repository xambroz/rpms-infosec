Name:           python-volatility
Summary:        Volatile memory extraction utility framework
Version:        2.6.1
%global         baserelease     6

License:        GPLv2+
URL:            http://www.volatilityfoundation.org/
#               https://github.com/volatilityfoundation/volatility


%global         gituser         volatilityfoundation
%global         gitname         volatility
%global         gitdate         20201211
%global         commit          a438e768194a9e05eb4d9ee9338b881c0fa25937
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# By default build from official release
# leave option here to build from git snapshot instead
%bcond_without     snapshot


%if 0%{?with_snapshot}
#               not using 0. on the beginning of release as this git snapshot is past the 0.7.0 release
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{gitname}-%{version}-%{shortcommit}.tar.gz
%else
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{gitname}-%{version}.tar.gz
%endif

Source1:        vol_genprofile
Source2:        volatility.1

# Migrate from pyCrypto to Cryptodome as request of https://pagure.io/fesco/issue/2247
Patch1:         volatility-cryptodome.patch


BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

#Tool dwarfdump from libdwarf-tools used in script vol_genprofile for generation of linux profile
#Requires:      /usr/bin/dwarfdump

%global _description\
The Volatility Framework is a completely open collection of tools, implemented\
in Python under the GNU General Public License, for the extraction of digital\
artifacts from volatile memory (RAM) samples. The extraction techniques are\
performed completely independent of the system being investigated but offer\
unprecedented visibility into the run time state of the system. The framework is\
intended to introduce people to the techniques and complexities associated with\
extracting digital artifacts from volatile memory samples and provide a\
platform for further work into this exciting area of research.\


%description %_description

%package -n python2-volatility
Summary: %summary
Requires:       python2-pycryptodomex
# Requires:     python2-crypto
# pslist is not working without distorm3
Requires:       python2-distorm3
Requires:       libdwarf-tools
%{?python_provide:%python_provide python2-volatility}

%description -n python2-volatility %_description

%prep
%if 0%{?with_snapshot}
# Build from git snapshot
%autosetup -v -p 1 -n %{gitname}-%{commit}
%else
# Build from git release version
%autosetup -v -p 1 -n %{gitname}-%{version}
%endif

# Fix python shabang to explicit state oython version
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python2|' tools/mac/convert.py \
    tools/vtype_diff.py


%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

#Contrib contains plugins which might not work well if loaded all at once
#thus can't be loaded by default from plugins
mkdir -p %{buildroot}%{python2_sitelib}/volatility/contrib
mv %{buildroot}/usr/contrib/_* %{buildroot}%{python2_sitelib}/volatility/contrib/
mv %{buildroot}/usr/contrib/library_example %{buildroot}%{python2_sitelib}/volatility/contrib/
mv %{buildroot}/usr/contrib/plugins/* %{buildroot}%{python2_sitelib}/volatility/contrib/
touch %{buildroot}%{python2_sitelib}/volatility/contrib/__init__.py
touch %{buildroot}%{python2_sitelib}/volatility/contrib/malware/__init__.py

mkdir -p %{buildroot}/%{_datadir}/%{name}
mv %{buildroot}/usr/tools %{buildroot}/%{_datadir}/%{name}/tools

mv %{buildroot}/%{_datadir}/%{name}/tools/vtype_diff.py %{buildroot}/%{_bindir}/
mv %{buildroot}%{_bindir}/vol.py %{buildroot}/%{_bindir}/vol2
ln -s vol2 %{buildroot}/%{_bindir}/volatility2

install -m 755 %{SOURCE1} %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_mandir}/man1/
install -m 644 %{SOURCE2} %{buildroot}/%{_mandir}/man1/
gzip %{buildroot}/%{_mandir}/man1/volatility.1
ln -s volatility.1.gz %{buildroot}/%{_mandir}/man1/vol.1.gz
ln -s volatility.1.gz %{buildroot}/%{_mandir}/man1/vol_genprofile.1.gz

# pytho2-volatility is default up to fc31
%if 0%{?fedora} <= 31
ln -s vol2 %{buildroot}%{_bindir}/vol
ln -s volatility2 %{buildroot}%{_bindir}/volatility
%endif



%files -n python2-volatility
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt LEGAL.txt
%doc AUTHORS.txt CHANGELOG.txt CREDITS.txt README.txt

%{python2_sitelib}/*
%{_datadir}/%{name}/
%{_bindir}/vol2
%{_bindir}/volatility2
%if 0%{?fedora} <= 31
%{_bindir}/vol
%{_bindir}/volatility
%endif
%{_bindir}/vol_genprofile
%{_bindir}/vtype_diff.py
%{_mandir}/man1/volatility.*
%{_mandir}/man1/vol.*
%{_mandir}/man1/vol_genprofile.*

%changelog
* Mon May 18 2020 Michal Ambroz <rebus at, seznam.cz> - 2.6.1-6
- switch to git snapshot from 2020-12-11 for bugfixes

* Mon May 18 2020 Michal Ambroz <rebus at, seznam.cz> - 2.6.1-5
- switch to git snapshot for bugfixes

* Wed Oct 30 2019 Michal Ambroz <rebus at, seznam.cz> - 2.6.1-4
- prepare binary links for side by side with python-volatility3
  and replacement in fc32+

* Tue Oct 22 2019 Michal Ambroz <rebus at, seznam.cz> - 2.6.1-3
- replace pyCrypto with better maintained Cryptodome as part of the
  python2 exception https://pagure.io/fesco/issue/2247

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 Michal Ambroz <rebus at, seznam.cz> - 2.6.1-1
- bump to current git release of 2.6.1
- especially fixing the dwarf on newer 4.9 kernels 

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.6.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.0-4
- Python 2 binary package renamed to python2-volatility
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Michal Ambroz <rebus at, seznam.cz> - 2.6.0-1
- bump to current git release of 2.6.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 16 2016 Michal Ambroz <rebus at, seznam.cz> - 2.5.0-7
- adding manpage from Debian

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Michal Ambroz <rebus at, seznam.cz> - 2.5.0-3
- fix project URL 

* Wed Nov 11 2015 Michal Ambroz <rebus at, seznam.cz> - 2.5.0-2
- fix location of contribs 

* Wed Nov 11 2015 Michal Ambroz <rebus at, seznam.cz> - 2.5.0-1
- bump to current git release of 2.5.0

* Mon Jun 22 2015 Michal Ambroz <rebus at, seznam.cz> - 2.4.1-1
- bump to current git release of 2.4.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Alon Levy <alevy@redhat.com> - 2.3.1-2
- Add Requires pycrypto needed by multiple plugins

* Thu Nov 21 2013 Alon Levy <alevy@redhat.com> - 2.3.1-1
- New upstream.

* Mon Sep 16 2013 Alon Levy <alevy@redhat.com> - 2.2-3
- Fix FSF address and wrong shebang lines, rhbx#948359 comment 11

* Sat Sep 14 2013 Alon Levy <alevy@redhat.com> - 2.2-2
- Addressed review comments, rhbx#948359 comment 7

* Sat Sep 14 2013 Alon Levy <alevy@redhat.com> - 2.2-1
- Initial package (rhbz#948359)
