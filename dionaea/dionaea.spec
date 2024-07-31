Name:           dionaea
Version:        0.11.0
Summary:        Low interaction honeypot
# Show as the RPM release number (keep same number line for tarball and git builds)
%global         baserelease     1

%if 0%{?rhel}
# Group needed for EPEL
Group:          Applications/System
%endif

# Dionaea package is licensed with GPLv2
# On top of that it is granting one exception extra - it is permitted by the license
# to link modified binary files in the src/ directory against the openssl libraries.
License:        GPLv2 with exceptions
URL:            https://dionaea.readthedocs.io/
#    Current source:
VCS:            https://github.com/DinoTools/dionaea
#    Original site (dissappeared in 2013, but still available from archives):
#               https://dionaea.carnivore.it -> https://web.archive.org/web/20150820080019/https://dionaea.carnivore.it
#    Another forks:
#               https://github.com/rep/dionaea
#               https://gitlab.labs.nic.cz/honeynet/dionaea/
#               https://github.com/devwerks/dionaea
#               https://github.com/RootingPuntoEs/DionaeaFR/
#               https://github.com/ManiacTwister/dionaea/
#               https://github.com/tklengyel/dionaea
#               https://github.com/rep/dionaea
#    Installation:
#               https://www.aldeid.com/wiki/Dionaea/Installation



# Specification of the used GIT commit
%global         gituser         DinoTools
%global         gitname         dionaea
%global         commit          4e459f1b672a5b4c1e8335c0bff1b93738019215
%global         gitdate         20210228
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Use systemd unit files on Fedora and RHEL 7 and above.
%bcond_without  systemd
%if (0%{?rhel} && 0%{?rhel} < 7)
%bcond_with     systemd
%endif


# By default build from official release
# leave option here to build from git snapshot instead
%bcond_without     snapshot


%if 0%{?with_snapshot}
#               not using 0. on the beginning of release as this git snapshot is past the 0.7.0 release
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%else
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Source1:        %{name}.sysconfig
Source2:        %{name}.initd
Source3:        %{name}.service
Source4:        %{name}.logrotate



# ipv6 structures in <netinet/in.h> are used by the <sys/socket.h>
# ipv6 structures needs explicit CFLAGS " -D_GNU_SOURCE" to compile on linux
# just cosmetics - not reported yet to upstream
Patch3:         dionaea-03_in6_pktinfo.patch


# Fix hardcoded lib dir
# https://github.com/DinoTools/dionaea/pull/181
# https://github.com/DinoTools/dionaea/pull/209
# Patch8:       dionaea-08_modules_libdir.patch


# Patch to explicitly state the python module version to the setup.py
# Patch12:        dionaea-12_py_module_version.patch

# Replace deprecated PyUnicode_GetSize with PyUnicode_GetLength
# Patch13:        dionaea-13_GetSize_deprecated.patch

# Trying to identify the mole
# Patch14:        dionaea-14_safe_load.patch

# Python 3.13 compatibility
# Change PyEval_CallObject to PyObject_CallObject
Patch15:        dionaea-15_pyeval_callobject.patch

# Cmake list APPEND operation is adding unwanted semicolon to CFLAGS
Patch16:        dionaea-16_cmake_append_flags.patch

# Cmake dirs
Patch17:        dionaea-17_cmake_dirs.patch

# A lot of regexes in dionaea project is not declared as raw strings
# python3 tries to resolve the escape sequences
Patch18:        dionaea-18_python_regex.patch

# Switch from distutils to setuptools
# do not install to egg directory
Patch19:        dionaea-19_setuptools.patch


%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  cmake
BuildRequires:  cmake-rpm-macros
%else
BuildRequires:  cmake3
%endif

BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  pkgconfig
BuildRequires:  sqlite
BuildRequires:  git

BuildRequires:  libev-devel
BuildRequires:  libemu-devel
BuildRequires:  udns-devel
BuildRequires:  libnl3-devel
BuildRequires:  glib2-devel
BuildRequires:  curl-devel
BuildRequires:  readline-devel
BuildRequires:  libpcap-devel
BuildRequires:  libsq3-devel
BuildRequires:  sqlite
BuildRequires:  openssl-devel

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-Cython

%if 0%{?with_systemd}
BuildRequires:  systemd-units
%endif


# Optional dependencies
BuildRequires:  loudmouth-devel
BuildRequires:  libnetfilter_queue-devel
BuildRequires:  libnl3-devel


# Missing dependencies


# Documentation generation
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-sphinx
%else
BuildRequires:  python3-sphinx
%endif
BuildRequires: make

Requires:       logrotate

# Base package can't run without the python module
Requires:       python%{python3_pkgversion}-dionaea

%if 0%{?with_systemd}
%{?systemd_requires}
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

Requires(pre): shadow-utils

%description
Dionaea is low interaction honeypot. It is meant to be a nepenthes successor,
embedding python as scripting language, using libemu to detect shell-codes,
supporting ipv6 and TLS.


# ============= documentation package ==========================================
%package doc
Summary:        Documentation for the dionaea honeypot package
BuildArch:      noarch


%description doc
This is documentation for the dionaea honeypot package.
Dionaea is low interaction honeypot. It is meant to be a nepenthes successor,
embedding python as scripting language, using libemu to detect shell-codes,
supporting ipv6 and TLS.



# ============= python3 package ================================================
%package -n python%{python3_pkgversion}-%{gitname}
Summary:        Python3 binding for the dionaea honeypot
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}

# Runtime dependencies
Requires:       python%{python3_pkgversion}-bson
Requires:       python%{python3_pkgversion}-PyYAML
Requires:       python%{python3_pkgversion}-scapy
Requires:       python%{python3_pkgversion}-sqlalchemy

%description -n python%{python3_pkgversion}-%{gitname}
This is a Python3 library that gives access to dionaea honeypot functionality.



# ============= preparation ====================================================
%prep
%if 0%{?with_snapshot}
# Build from git snapshot
%autosetup -p 1 -n %{gitname}-%{commit} -N
%else
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version} -N
%endif

%autopatch -p 1

# Unbundle the pyev library and use the system one
# https://github.com/DinoTools/dionaea/issues/169
rm -rf modules/python/pyev

# Fix paths:
# - remove the hardcoded prefix /opt/dionaea
# - move /var/dionaea to /var/lib/dionaea according to Linux FHS
# https://github.com/DinoTools/dionaea/issues/168
# https://github.com/DinoTools/dionaea/issues/256
sed -i -e "s|/opt/dionaea[/]*|/|g; s|/var/dionaea|/var/lib/dionaea|g;" \
    modules/python/util/gnuplotsql.py \
    modules/python/util/readlogsqltree.py \
    doc/source/tips_and_tricks.rst \
    doc/html/index.html \
    doc/source/old/configuration.rst \
    doc/source/old/seagfaults.rst \
    doc/source/old/utils.rst \
    doc/source/run.rst \
    doc/source/tips_and_tricks.rst


# Change var/dionaea to var/lib/dionaea for the location of sip user database
sed -i -e "s|var/dionaea|var/lib/dionaea|g;" \
    modules/python/dionaea/sip/extras.py



# Scripts should run with /usr/bin/python3 shabang and not /usr/bin/env python3 or /bin/python3
# Fedora specific - not reported upstream
sed -i -e 's|#!/bin/python3|#!/usr/bin/python3|g; s|#!/usr/bin/env python3|#!/usr/bin/python3|g;' \
    modules/python/util/readlogsqltree.py \
    modules/python/util/logsql2postgres.py \
    modules/python/util/gnuplotsql.py \
    modules/python/util/updateccs.py




# ============= Build ==========================================================
%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
#%%configure --enable-python --with-python=`which python3` --with-glib=glib --with-nl-include=/usr/include/libnl3 --disable-werror
#%%make_build CFLAGS="%{optflags} -Wno-error -D_GNU_SOURCE -std=c99"

# cmake build with higher parralelism ends up with errors for Fedora
%cmake3 \
    -L \
    -DCMAKE_INSTALL_FULL_SYSCONFDIR:PATH=%{_sysconfdir} \
    -DCMAKE_INSTALL_FULL_LIBDIR:PATH=%{_libdir} \
    -DCMAKE_INSTALL_FULL_LOCALSTATEDIR:PATH=%{_localstatedir} \
    -DDIONAEA_PYTHON_SITELIBDIR:PATH=%{python3_sitearch}

%cmake3_build -j1 --verbose --verbose

cd doc
make html
make man
rm -rf build/html/.{doctrees,buildinfo}
cd ..



# ============= Install ========================================================
%install
%cmake3_install

# Use only the sitearch directory, otherwise python will be confused
# by not having native and python modules in the same directory
#%%make_install PYTHON_SITELIB=%{python3_sitearch} PYTHON_SITEARCH=%{python3_sitearch}

# *.a *.la files not allowed for fedora
find %{buildroot} '(' -name '*.a' -o -name '*.la' ')' -delete


# Install the manpage
# TODO - report upstream
install -d %{buildroot}%{_mandir}/man1/
install -p -D -m 644 doc/build/man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
mv doc/build/html/ ./html

# install the service parameter configuration
# TODO - report upstream
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# install the service init files
%if 0%{?with_systemd}
  # install systemd service files
  mkdir -p %{buildroot}%{_unitdir}
  install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
%else
  # install legacy SysV init scripts
  mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
  install -p -D -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%endif

# Install logrotate
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Create the log directory
mkdir -p %{buildroot}%{_localstatedir}/log/%{name} || :

# Create directories to capture binaries and payloads
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/binaries || :
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/bistreams || :

# Create directory for the content templates
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/roots/ftp  || :
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/roots/tftp || :
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/roots/www  || :
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/roots/upnp || :

touch %{buildroot}%{_sharedstatedir}/%{name}/dionaea.sqlite
touch %{buildroot}%{_sharedstatedir}/%{name}/dionaea_incident.sqlite
touch %{buildroot}%{_sharedstatedir}/%{name}/sipaccounts.sqlite

# leave this for the %%license tag
rm -f %{buildroot}/usr/share/doc/dionaea/LICENSE \
    %{buildroot}/usr/share/doc/dionaea/LICENSE.openssl



# ============= Scriptlets ==========================================================
%post
%if 0%{?with_systemd}
  %systemd_post %{name}.service
%else
  /sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?with_systemd}
  %systemd_preun %{name}.service
%else
  if [ $1 -eq 0 ] ; then
     /sbin/service %{name} stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del %{name}
  fi
%endif

%postun
%if 0%{?with_systemd}
  %systemd_postun %{name}.service
%else
  if [ $1 -eq 1 ] ; then
     /sbin/service %{name} condrestart >/dev/null 2>&1 || :
  fi
%endif


%pre
getent group dionaea >/dev/null || groupadd -r dionaea || :
getent passwd dionaea >/dev/null || \
    useradd -r -g dionaea -d /home/dionaea -s /sbin/nologin \
    -c "Dionaea honeypot" dionaea || :




# ============= package files ==================================================
%files
%license LICENSE src/LICENSE.openssl
%doc README.md CHANGELOG.rst CONTRIBUTING.rst
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/%{name}
%{_libdir}/%{name}/
%exclude %{_libdir}/%{name}/python.so
%{_mandir}/man1/%{name}.1.*
%attr(0750,dionaea,dionaea) %dir %{_localstatedir}/log/%{name}
%attr(0750,dionaea,dionaea) %dir %{_sharedstatedir}/%{name}
%attr(0750,dionaea,dionaea) %dir %{_sharedstatedir}/%{name}/binaries
%attr(0750,dionaea,dionaea) %dir %{_sharedstatedir}/%{name}/bistreams
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/roots/
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/dionaea.sqlite
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/dionaea_incident.sqlite
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/sipaccounts.sqlite
%{_sharedstatedir}/%{name}/http

# TODO python utils currently not packed
# %%{_bindir}/gnuplotsql
# %%{_bindir}/readlogsqltree



%if 0%{?with_systemd}
%{_unitdir}/*.service
%else
%{_initrddir}/*
%endif



%files doc
%doc README.md
%doc html



%files -n python%{python3_pkgversion}-%{gitname}
%license LICENSE
%doc README.md
%{_libdir}/%{name}/python.so
%{python3_sitearch}/%{name}*
# %%{python3_sitearch}/%%{name}-*egg-info


%changelog
* Thu Jul 04 2024 Michal Ambroz <rebus at, seznam.cz> 0.11.0-1
- bump to 0.11.0

* Mon Mar 25 2024 Nils Philippsen <nils@tiptoe.de> - 0.7.0-28
- Revert constraining SQLAlchemy version

* Tue Mar 19 2024 Nils Philippsen <nils@tiptoe.de> - 0.7.0-27
- Add dependency on setuptools Python package

* Tue Mar 19 2024 Nils Philippsen <nils@tiptoe.de> - 0.7.0-26
- Depend on SQLAlchemy < 2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Michal Ambroz <rebus at, seznam.cz> 0.7.0-22
- add version metadata to the python module to fix FTBFS

* Sun Jul 23 2023 Python Maint <python-maint@redhat.com> - 0.7.0-21
- Rebuilt for Python 3.12

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.7.0-19
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.7.0-16
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.7.0-14
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.7.0-12
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-9
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Michal Ambroz <rebus at, seznam.cz> 0.7.0-7
- switch to glib2 based on #1766678 to modernize and prepare for epel8

* Thu Oct 24 2019 Michal Ambroz <rebus at, seznam.cz> 0.7.0-6
- rebuilt rawhide after ressurection of libdasm/libemu

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-5.3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Adam Williamson <awilliam@redhat.com> - 0.7.0-5
- Disable -Werror to fix build (see upstream #225)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-4.1
- Rebuilt for Python 3.7

* Mon Jun 18 2018 Michal Ambroz <rebus at, seznam.cz> 0.7.0-4
- anothe improvement of logrotate script
- add the empty files for dionaea.sqlite dionaea_incident.sqlite sipaccounts.sqlite

* Mon Jun 04 2018 Michal Ambroz <rebus at, seznam.cz> 0.7.0-3
- fix logrotate script
- use the current version of openssl (needs to be same as curllib is using)

* Thu May 10 2018 Michal Ambroz <rebus at, seznam.cz> 0.7.0-1
- bump to release 0.7.0

* Mon May 07 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-10.20180326git1748f3b
- cosmetics, changing description in the systemd service

* Mon Apr 30 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-9.20180326git1748f3b
- add runtime python dependencies
- fix location of sip user database

* Mon Apr 30 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 0.6.0-8.20180326git1748f3b
- Fix condition for python-sphinx on Fedora

* Fri Apr 20 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-7.20180326git1748f3b
- fix the link creation to python core library 

* Mon Apr 09 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-6.20180326git1748f3b
- fix log rotation, move the logs to /var/log/dionaea
- create user dionaea:dionaea
- grant shared stare dir/files to the dionaea user account

* Mon Apr 09 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-5.20180326git1748f3b
- clean-up based on review in #1564716

* Fri Apr 06 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-4.20180326git1748f3b
- update to current git snapshot, add logrotate and service files

* Wed Mar 21 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-3.20180313gitd2efb76
- fix openssl dependency for EPEL7 build

* Wed Mar 21 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-2.20180313gitd2efb76
- bump to commit d2efb768e753a7f1ddca6dbf402548d741f33574
- unbundle pyev and refer to system-installed pyev
- remove the hardcoded default prefix /opt/dionaea
- move from /var/dionaea to /var/lib/dionaea
- fix the doc generation warnings

* Thu Dec 28 2017 Michal Ambroz <rebus at, seznam.cz> 0.6.0-1
- initial package

