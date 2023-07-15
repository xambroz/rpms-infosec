Name:           capstone
Version:        5.0
Release:        1%{?dist}
Summary:        A lightweight multi-platform, multi-architecture disassembly framework

%global         gituser         capstone-engine
%global         gitname         capstone
# 5.0.0
%global         gitdate         20230705
%global         commit          650e85dcf23b3a3bff69144511533b7339436238
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

License:        BSD
URL:            http://www.capstone-engine.org/
VCS:            https://github.com/aquynh/capstone/
#               https://github.com/aquynh/capstone/releases
# Source0:      https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global         common_desc %{expand:
Capstone is a disassembly framework with the target of becoming the ultimate
disasm engine for binary analysis and reversing in the security community.}

# Build with python3 package by default
%bcond_without  python3

# Build without python2 package for newer releases f32+ and rhel8+
%if (0%{?fedora} && 0%{?fedora} >= 32 ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
%bcond_with     python2
%else
%bcond_without  python2
%endif


%global srcname distribute

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  git

%ifarch %{java_arches}
BuildRequires:  jna
BuildRequires:  java-devel
%endif

%if %{with python2}
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif


%description
%{common_desc}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{common_desc}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%if %{with python2}
%package        -n python2-capstone
%{?python_provide:%python_provide python2-capstone}
# Remove before F30
Provides:       %{name}-python = %{version}-%{release}
Provides:       %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python < %{version}-%{release}
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    -n python2-capstone
%{common_desc}
The python2-capstone package contains python bindings for %{name}.
# with_python2
%endif



%if %{with python3}
%package	-n python%{python3_pkgversion}-capstone
%{?python_provide:%python_provide python%{python3_pkgversion}-capstone}
Provides:       %{name}-python%{python3_pkgversion} = %{version}-%{release}
Provides:       %{name}-python%{python3_pkgversion}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python%{python3_pkgversion} < %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Python3 bindings for %{name}


%description    -n python%{python3_pkgversion}-capstone
%{common_desc}
The python%{python3_pkgversion}-capstone package contains python3 bindings for %{name}.
#with python3
%endif


%ifarch %{java_arches}
%package        java
Summary:        Java bindings for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    java
%{common_desc}
The %{name}-java package contains java bindings for %{name}.
%endif


%prep
# autosetup -n %%{gitname}-%%{commit} -S git
autosetup -n %{gitname}-%{version} -S git



%build
V=1 CFLAGS="%{optflags}" \
PREFIX="%{_prefix}" LIBDIRARCH="%{_lib}" INCDIR="%{_includedir}" \
%make_build PYTHON2=%{__python2} PYTHON3=%{__python3}

# Fix pkgconfig file
sed -i 's;%{buildroot};;' capstone.pc
grep -v archive capstone.pc > capstone.pc.tmp
mv capstone.pc.tmp capstone.pc


# build python bindings
pushd bindings/python

%if %{with python2}
%py2_build
%endif

%if %{with python3}
#%%py3_build
%pyproject_wheel
%endif
popd

%ifarch %{java_arches}
# build java bindings needs some python
pushd bindings/java
%if %{with python3}
%make_build PYTHON2=%{__python3} PYTHON3=%{__python3} CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
%else
%make_build PYTHON2=%{__python2} PYTHON3=%{__python2} CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
%endif
popd
%endif



%install
DESTDIR=%{buildroot} PREFIX="%{_prefix}" LIBDIRARCH=%{_lib} \
INCDIR="%{_includedir}" make install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# install python bindings
pushd bindings/python
%if %{with python2}
%py2_install
%endif

%if %{with python3}
#%%py3_install
%pyproject_install
%pyproject_save_files capstone

%endif
popd

%ifarch %{java_arches}
# install java bindings
install -D -p -m 0644 bindings/java/%{name}.jar  %{buildroot}/%{_javadir}/%{name}.jar
%endif


%check
# ln -s libcapstone.so.5 libcapstone.so
make check LD_LIBRARY_PATH="$(pwd)"


%ldconfig_scriptlets



%files
%license LICENSE.TXT LICENSE_LLVM.TXT
%doc CREDITS.TXT ChangeLog README.md SPONSORS.TXT
%{_libdir}/*.so.*
%{_bindir}/cstool



%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*



%if %{with python2}
%files -n python2-capstone
%{python2_sitelib}/*egg-info
%{python2_sitelib}/%{name}
%endif



%if %{with python3}
%files -n python%{python3_pkgversion}-capstone -f %{pyproject_files}
%endif


%ifarch %{java_arches}
%files java
%{_javadir}/
%endif

%changelog
* Sat Jul 15 2023 Jonathan Wright <jonathan@almalinux.org> - 5.0-1
- Update to 5.0
- Remove legacy code from spec
- Modernize spec file

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.0.2-14
- Rebuilt for Python 3.12

* Fri Jan 27 2023 Michal Ambroz <rebus AT_ seznam.cz> - 4.0.2-13
- update the new github page

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
- drop java binding for platforms not in %%{java_arches}

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.2-10
- Rebuilt for Python 3.11

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.0.2-9
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.2-6
- Rebuilt for Python 3.10

* Fri May 14 2021 Michal Ambroz <rebus AT_ seznam.cz> - 4.0.2-5
- modernize specfile, using with bcond and py*_build macros

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.0.2-2
- Use make_build macro instead of make (thanks to tstellar)

* Mon Jul 20 2020 Riccardo Schirone <rschirone91@gmail.com> - 4.0.2-1
- Rebase to upstream version 4.0.2

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 4.0.1-13
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-12
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Kalev Lember <klember@redhat.com> - 4.0.1-10
- Avoid hardcoding /usr prefix

* Tue Oct 15 2019 Michal Ambroz <rebus AT_ seznam.cz> - 4.0.1-9
- do not build python2 package for rhel8

* Thu Oct 10 2019 Michal Ambroz <rebus AT_ seznam.cz> - 4.0.1-8
- fix descriptions of sub-packages
- remove buildroot from the build phase

* Thu Oct 10 2019 Michal Ambroz <rebus AT_ seznam.cz> - 4.0.1-7
- remove python2 from rawhide/fc32 package

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-5
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 12 2019 Richard W.M. Jones <rjones@redhat.com> - 4.0.1-2
- Add upstream patch which fixes libcapstone.pc
  https://github.com/aquynh/capstone/issues/1339

* Fri Jan 11 2019 Michal Ambroz <rebus _AT seznam.cz> - 4.0.1-1
- bump to 4.0.1 release

* Mon Aug 27 2018 Michal Ambroz <rebus _AT seznam.cz> - 3.0.5-1
- bump to 3.0.5

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.4-17
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Michal Ambroz <rebus _AT seznam.cz> - 3.0.4-16
- unify the naming convention for the python packages
- fix the python3 package naming for EPEL7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.4-15
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.4-14
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.4-12
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.4-11
- Python 2 binary package renamed to python2-capstone
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.4-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 27 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.4-4
- Really add dist tag this time

* Sun Oct 25 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.4-3
- Fix issues found during package review: dist tag, git sources

* Thu Jul 16 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.4-2
- Fix EPEL6 build problems

* Wed Jul 15 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.4-1
- new version 3.0.4. Includes security fixes.

* Tue May 12 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.3-2
- Addressed issues found during package review.

* Fri May 08 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.3-1
-  Update to version 3.0.3

* Fri May 08 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.2-3
- Added python3 and hardened build support. Update java building.
- Various cleanups.

* Wed May 06 2015 Stefan Cornelius <scorneli@redhat.com> - 3.0.2-2
- Update to 3.0.2. Fix 64bit issues. add %%check.

* Sat Sep 27 2014 Adel Gadllah <adel.gadllah@gmail.com> - 2.1.2-2
- Addressed issues found during package review.

* Mon May 19 2014 Adel Gadllah <adel.gadllah@gmail.com> - 2.1.2-1
- Initial package
