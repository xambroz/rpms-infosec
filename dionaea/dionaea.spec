Name:           dionaea
Version:        0.6.0
Summary:        Low interaction honeypot
Group:          Applications/System

# Dionaea package is licensed with GPLv2
# On top of that it is granting one exception extra - it is permitted by the license
# to link modified binary files in the src/ directory against the openssl libraries.
License:        GPLv2 with exceptions
URL:            https://dionaea.readthedocs.io/
#    Current source:
#               https://github.com/DinoTools/dionaea
#    Original site (dissappeared in 2013, but still available from archives):
#               https://dionaea.carnivore.it -> https://web.archive.org/web/20150820080019/https://dionaea.carnivore.it
#    Another forks:
#               https://github.com/rep/dionaea
#               https://gitlab.labs.nic.cz/honeynet/dionaea/
#               https://github.com/devwerks/dionaea
#               https://github.com/RootingPuntoEs/DionaeaFR/
#    Installation:
#               https://www.aldeid.com/wiki/Dionaea/Installation



# Specification of the used GIT commit
%global         gituser         DinoTools
%global         gitname         dionaea
%global         commit          1748f3b3936aa1da2d92500251ae8010fe181dfc
%global         gitdate         20180326
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Use systemd unit files on Fedora and RHEL 7 and above.
%global         _with_systemd   1

%if (0%{?rhel} && 0%{?rhel} < 7)
    %global     _with_systemd   0
%endif


# Build source is github release=1 or git commit=0
%global         build_release    0

%global         rel              5

%if 0%{?build_release}  > 0
Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
#               not using 0. on the beginning of release as this git snapshot is past the 0.6.0 release
Release:        %{rel}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release

Source1:        %{name}.sysconfig
Source2:        %{name}.initd 
Source3:        %{name}.service 
Source4:        %{name}.logrotate



# Use the glib CFLAGS and LDFLAGS during build where necessary
# https://github.com/DinoTools/dionaea/issues/161
# https://github.com/DinoTools/dionaea/pull/160
# Merged in in https://github.com/DinoTools/dionaea/commit/1748f3b3936aa1da2d92500251ae8010fe181dfc
# Patch1:         dionaea-01_glib.patch

# Get rid of the warning about not used return value from chdir.
# https://github.com/DinoTools/dionaea/issues/162
# https://github.com/DinoTools/dionaea/pull/163
# Merged in in https://github.com/DinoTools/dionaea/commit/ea5d54060af53250abfe3dde9f36af399fa30524
# Patch2:         dionaea-02_warnerror.patch

# ipv6 structures in <netinet/in.h> are used by the <sys/socket.h>
# ipv6 structures needs explicit CFLAGS " -D_GNU_SOURCE" to compile on linux
# just cosmetics - not reported yet to upstream
Patch3:         dionaea-03_in6_pktinfo.patch

# Unbundle the pyev library and use the system one
# https://github.com/DinoTools/dionaea/issues/166
Patch4:         dionaea-04_pyev.patch

# Have a dedicated variable for the python sitelib, so it can be easily changed externally when building the system package.
# https://github.com/DinoTools/dionaea/issues/164
# https://github.com/DinoTools/dionaea/pull/165
# Merged in in https://github.com/DinoTools/dionaea/commit/890ae5e85f55130be928b03b751b5f7cd1032f21
# Patch5:         dionaea-05_sitelib.patch

# Fix warnings during the generation of documentation
# https://github.com/DinoTools/dionaea/issues/170
# https://github.com/DinoTools/dionaea/pull/179
Patch6:         dionaea-06_docswarn.patch

# Fix configure not finding the cython on RHEL7/Centos7
# https://github.com/DinoTools/dionaea/pull/180
Patch7:         dionaea-07_cython_el7.patch

# Fix hardcoded lib dir
# https://github.com/DinoTools/dionaea/pull/181
Patch8:         dionaea-08_modules_libdir.patch

# Call setgroups before setresuid
# https://github.com/DinoTools/dionaea/issues/177
# https://github.com/DinoTools/dionaea/pull/178
Patch9:         dionaea-09_setgroups_before_setresuid.patch

# Call chdir before chroot
# https://github.com/DinoTools/dionaea/issues/176
# https://github.com/DinoTools/dionaea/pull/175
Patch10:        dionaea-10_chdir_before_chroot.patch

# Not use obsolete m4 macros
# https://github.com/DinoTools/dionaea/pull/182
Patch11:        dionaea-11_obsolete_m4.patch


BuildRequires:  autoconf
BuildRequires:  automake
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
BuildRequires:  glib-devel
BuildRequires:  curl-devel
BuildRequires:  readline-devel
BuildRequires:  libpcap-devel
BuildRequires:  libsq3-devel
BuildRequires:  sqlite

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-Cython

%if 0%{?fedora} >= 26
BuildRequires:  compat-openssl10-devel
%else
BuildRequires:  openssl-devel
%endif

%if 0%{?_with_systemd}
BuildRequires:  systemd-units
%endif


# Optional dependencies
BuildRequires:  loudmouth-devel
BuildRequires:  libnetfilter_queue-devel
BuildRequires:  libnl3-devel


# Missing dependencies


# Documentation generation
%if  0%{?rhel} <= 7
BuildRequires:  python-sphinx
%else
BuildRequires:  python3-sphinx
%endif

Requires:       logrotate

%if 0%{?_with_systemd}
%{?systemd_requires}
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif


%description
Dionaea honeypot is meant to be a nepenthes successor, embedding python
as scripting language, using libemu to detect shellcodes, supporting
ipv6 and tls.



# ============= documentation package ==========================================
%package doc
Summary:        Documentation for the dionaea honeypot package
Group:          Development/Libraries
BuildArch:      noarch


%description doc
This is documentation for the dionaea honeypot package.
Dionaea honeypot is meant to be a nepenthes successor, embedding python
as scripting language, using libemu to detect shellcodes, supporting
ipv6 and tls.



# ============= python3 package ================================================
%package -n python%{python3_pkgversion}-%{gitname}
Summary:        Python3 binding for the dionaea honeypot
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}

# Runtime dependencies
Requires:       python%{python3_pkgversion}-pyev
Requires:       python%{python3_pkgversion}-bson

%description -n python%{python3_pkgversion}-%{gitname}
This is a Python3 library that gives access to dionaea honeypot functionality.



# ============= preparation ====================================================
%prep
%if 0%{?build_release} > 0
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version} -S git

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit} -S git
%endif

# Unbundle the pyev library and use the system one
# https://github.com/DinoTools/dionaea/issues/169
rm -rf modules/python/pyev


# Fix paths - remove the hardcoded prefix /opt/dionaea
# https://github.com/DinoTools/dionaea/issues/168
sed -i -e "s|/opt/dionaea[/]*|/|g;" \
    modules/python/util/readlogsqltree.py \
    modules/python/util/logsql2postgres.py \
    modules/python/util/gnuplotsql.py \
    modules/python/util/updateccs.py \
    src/dionaea.c \
    vagrant/build.sh


# replace in documentation the prefix/destdir /opt/dionaea with variable ${DESTDIR}
# https://github.com/DinoTools/dionaea/issues/168
sed -i -e "s|/opt/dionaea/var/dionaea|${DESTDIR}/var/lib/dionaea|g;" \
    doc/html/index.html \
    doc/source/tips_and_tricks.rst \
    doc/source/old/configuration.rst \
    doc/source/old/utils.rst \
    modules/python/util/readlogsqltree.py


# move /var/dionaea to /var/lib/dionaea according to LFS
# Fedora specific - not reported upstream
sed -i -e "s|/var/dionaea|/var/lib/dionaea|g;" \
    modules/python/util/readlogsqltree.py \
    modules/python/util/gnuplotsql.py

# move /var/dionaea to /var/lib/dionaea according to LFS
# Fedora specific - not reported upstream
sed -i -e 's|\$(localstatedir)/dionaea/|\$(localstatedir)/lib/dionaea/|g;' \
    Makefile.am

# move /var/dionaea to /var/lib/dionaea according to LFS
# Fedora specific - not reported upstream
sed -i -e 's|@LOCALESTATEDIR@/dionaea/|@LOCALESTATEDIR@/lib/dionaea/|g;' \
    conf/dionaea.cfg.in \
    conf/ihandlers/fail2ban.yaml.in \
    conf/ihandlers/log_db_sql.yaml.in \
    conf/ihandlers/log_incident.yaml.in \
    conf/ihandlers/log_json.yaml.in \
    conf/ihandlers/log_sqlite.yaml.in \
    conf/ihandlers/virustotal.yaml.in \
    conf/services/sip.yaml.in \
    conf/services/http.yaml.in \
    conf/services/ftp.yaml.in \
    conf/services/tftp.yaml.in \
    conf/services/upnp.yaml.in

# Change the hardoced minor python3.2 version especially in shabang to python3
# https://github.com/DinoTools/dionaea/issues/169
sed -i -e 's|python3.2|python3|g;' \
    m4/az_python.m4 \
    doc/html/index.html \
    modules/python/util/readlogsqltree.py

# Scripts should run with /usr/bin/python3 shabang and not /bin/python3
sed -i -e 's|#!/bin/python3|#!/usr/bin/python3|;' \
    modules/python/util/readlogsqltree.py \
    modules/python/util/logsql2postgres.py \
    modules/python/util/gnuplotsql.py \
    modules/python/util/updateccs.py



# ============= Build ==========================================================
%build
autoreconf -vif
%configure --enable-python --with-python=`which python3` --with-glib=glib --with-nl-include=/usr/include/libnl3
make %{?_smp_mflags} CFLAGS="%{optflags} -Wno-error -D_GNU_SOURCE -std=c99"
cd doc
make html
make man
rm -rf build/html/.{doctrees,buildinfo}
cd ..



# ============= Install ========================================================
%install
# Use only the sitearch directory, otherwise python will be confused
# by not having native and python modules in the same directory
%make_install PYTHON_SITELIB=%{python3_sitearch} PYTHON_SITEARCH=%{python3_sitearch}

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
%if 0%{?_with_systemd}
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


mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/roots/tftp

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/bistreams



# ============= Scriptlets ==========================================================
%post
%if 0%{?_with_systemd}
  %systemd_post %{name}.service
%else
  /sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?_with_systemd}
  %systemd_preun %{name}.service
%else
  if [ $1 -eq 0 ] ; then
     /sbin/service %{name} stop >/dev/null 2>&1 || :
     /sbin/chkconfig --del %{name}
  fi
%endif

%postun
%if 0%{?_with_systemd}
  %systemd_postun %{name}.service
%else
  if [ $1 -eq 1 ] ; then
     /sbin/service %{name} condrestart >/dev/null 2>&1 || :
  fi
%endif



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
%{_sharedstatedir}/%{name}/

%if 0%{?_with_systemd}
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

