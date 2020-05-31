%global         gituser         radareorg
%global         gitname         cutter
%global         commit          c127772dc115717f8ca2e0c08d69d92c70b28a2d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           cutter
Version:        1.10.3
#Release:       0.1.git%{shortcommit}%{?dist}
Release:        1%{?dist}
Summary:        GUI for radare2 reverse engineering framework
Group:          Development/Tools


License:        GPLv3+
URL:            https://github.com/radareorg/cutter
#               https://github.com/radareorg/cutter
#Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  qt5-qtbase-devel
# BuildRequires:  /usr/bin/qmake


%description
A Qt and C++ GUI for radare2 reverse engineering framework (originally named Iaito).


%package devel
Summary:        Development files for the %{name} package
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the %{name} package. See %{name} package for more
information.


%prep
#setup -q -n %{gitname}-%{commit}
%setup -q -n %{gitname}-%{version}


# ====================================================================
%build
./build.sh



# ====================================================================
%check
# Do not run the testsuite yet - it pulls another package https://github.com/radare/radare2-regressions from github
# make tests



# ====================================================================
%install
NOSUDO=1 make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix}

# *.a files not allowed for fedora
find %{buildroot} -name '*.a' -delete



# ====================================================================
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig



# ====================================================================
%files
%doc AUTHORS.md CONTRIBUTING.md DEVELOPERS.md README.md
%doc doc/3D/ doc/node.js/ doc/pdb/ doc/sandbox/

# Webui removed cuz of having minified js code and missing source code
%doc %{_datadir}/%{name}/%{version}/www/README.Fedora
%doc %{_datadir}/doc/%{name}
%license COPYING COPYING.LESSER
%{_bindir}/r*
%{_libdir}/libr*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%{_libdir}/%{name}/last
%{_mandir}/man1/r*.1.*
%{_mandir}/man7/esil.7.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%dir %{_datadir}/%{name}/%{version}/cons
%dir %{_datadir}/%{name}/%{version}/fcnsign
%{_datadir}/%{name}/%{version}/fcnsign/*.sdb
%dir %{_datadir}/%{name}/%{version}/hud
%{_datadir}/%{name}/%{version}/hud/*
%dir %{_datadir}/%{name}/%{version}/magic
%{_datadir}/%{name}/%{version}/magic/*
%dir %{_datadir}/%{name}/%{version}/opcodes
%{_datadir}/%{name}/%{version}/opcodes/*.sdb
%dir %{_datadir}/%{name}/%{version}/syscall
%{_datadir}/%{name}/%{version}/syscall/*.sdb
%{_datadir}/%{name}/last
%{_datadir}/%{name}/%{version}/cons/*
%dir %{_datadir}/%{name}/%{version}/format
%{_datadir}/%{name}/%{version}/format/*


# TODO - no modules built since 2018
# %{_libdir}/%{name}/%{version}/*.so



%files devel
%{_includedir}/libr
%{_libdir}/libr*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Feb 11 2018 Michal Ambroz <rebus at, seznam.cz> 2.4.0-1
- bump to 2.4.0 release

* Mon Feb 05 2018 Michal Ambroz <rebus at, seznam.cz> 2.3.0-1
- bump to 2.3.0 release
- drop the web-interface for now

* Tue Nov 14 2017 Michal Ambroz <rebus at, seznam.cz> 2.0.1-1
- bump to 2.0.1 release

* Fri Aug 04 2017 Michal Ambroz <rebus at, seznam.cz> 1.6.0-1
- bump to 1.6.0 release

* Thu Jun 08 2017 Michal Ambroz <rebus at, seznam.cz> 1.5.0-1
- bump to 1.5.0 release

* Sun Apr 23 2017 Michal Ambroz <rebus at, seznam.cz> 1.4.0-1
- bump to 1.4.0 release

* Sat Mar 18 2017 Michal Ambroz <rebus at, seznam.cz> 1.3.0-1
- bump to 1.3.0 release

* Sat Feb 18 2017 Michal Ambroz <rebus at, seznam.cz> 1.3.0-0.1.gita37af19
- switch to git version fixing sigseg in radiff2

* Wed Feb 08 2017 Michal Ambroz <rebus at, seznam.cz> 1.2.1-1
- bump to 1.2.1
- removed deprecated post postun calling of /sbin/ldconfig

* Sat Oct 22 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.6-1
- bump to 0.10.6

* Sun Aug 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.5-1
- bump to 0.10.5

* Mon Aug 01 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.4-1
- bump to 0.10.4

* Sun Jun 05 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.3-1
- build for Fedora for release of 0.10.3

* Mon Apr 25 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.2-1
- build for Fedora for release of 0.10.2

* Thu Jan 21 2016 Michal Ambroz <rebus at, seznam.cz> 0.10.0-2
- build for Fedora for release of 0.10.0

* Sat Oct 10 2015 Michal Ambroz <rebus at, seznam.cz> 0.10.0-1
- build for Fedora for alpha of 0.10.0

* Sun Nov 09 2014 Pavel Odvody <podvody@redhat.com> 0.9.8rc3-0
- initial radare2 package

