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
%global         commit          fc5d86b7c7456281ec7c0877d3cb80fa58a09283
%global         gitdate         20201130
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Use systemd unit files on Fedora and RHEL 7 and above.
%bcond_without  systemd
%if (0%{?rhel} && 0%{?rhel} < 7)
%bcond_with     systemd
%endif


# By default build from official release
# leave option here to build from git snapshot instead
%bcond_with     snapshot


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
# Patch8:         dionaea-08_modules_libdir.patch


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

# Re-initialize the git repo, to track changes even on files ignored by the upstream
rm -rf .git
# Remove the .gitignore to prevent ignoring changes in some files
rm -f .gitignore
git init -q
git config user.email "rpmbuild"
git config user.name "rpmbuild"
git add .
git commit -a -m "base"

%autopatch -p 1

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


git commit -a -m "finished prep"


# ============= Build ==========================================================
%build
%cmake3
%cmake3_build

#%%configure --enable-python --with-python=`which python3` --with-glib=glib --with-nl-include=/usr/include/libnl3 --disable-werror
#%%make_build CFLAGS="%{optflags} -Wno-error -D_GNU_SOURCE -std=c99"
cd ../doc
make html
make man
rm -rf build/html/.{doctrees,buildinfo}
cd ..



# ============= Install ========================================================
%install
cd build
%cmake3_install

# Use only the sitearch directory, otherwise python will be confused
# by not having native and python modules in the same directory
#%%make_install PYTHON_SITELIB=%{python3_sitearch} PYTHON_SITEARCH=%{python3_sitearch}

# *.a *.la files not allowed for fedora
find %{buildroot} '(' -name '*.a' -o -name '*.la' ')' -delete

# Fix permissions
chmod -x \
    %{buildroot}%{_sharedstatedir}/%{name}/share/python/http/template/nginx/autoindex.html.j2 \
    %{buildroot}%{_sharedstatedir}/%{name}/share/python/http/template/nginx/error.html.j2

# Move dionaea to sbin dir
# TODO - report upstream
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

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
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/%{name}
%{_bindir}/gnuplotsql
%{_bindir}/readlogsqltree
%{_libdir}/%{name}/
%exclude %{_libdir}/%{name}/python.so
%{_mandir}/man1/%{name}.1.*
%attr(0750,dionaea,dionaea) %dir %{_localstatedir}/log/%{name}
%attr(0750,dionaea,dionaea) %dir %{_sharedstatedir}/%{name}
%attr(0750,dionaea,dionaea) %dir %{_sharedstatedir}/%{name}/binaries
%attr(0750,dionaea,dionaea) %dir %{_sharedstatedir}/%{name}/bistreams
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/roots/
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/share/
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/dionaea.sqlite
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/dionaea_incident.sqlite
%attr(-,dionaea,dionaea)        %{_sharedstatedir}/%{name}/sipaccounts.sqlite




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
%dir %{python3_sitearch}/%{name}
%{_libdir}/%{name}/python.so
%{python3_sitearch}/%{name}/*
%{python3_sitearch}/%{name}-*egg-info


%changelog
* Tue Jun 22 2021 Michal Ambroz <rebus at, seznam.cz> 0.11.0-1
- bump to 0.11.0

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

