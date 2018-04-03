Name:           dionaea
Version:        0.6.0
Summary:        Low interaction honeypot.
Group:          Applications/System
# Exception - it is permitted to link modified binary files in the src/ directory against
# the openssl libraries without breaking the license of dionaea
License:        GPLv2 with exceptions
URL:            https://dionaea.readthedocs.io/
#    Current source:
#               https://github.com/DinoTools/dionaea
#    Original site (dissappeared in 2013, but still available from archives):
#               https://dionaea.carnivore.it
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
%global         commit          d2efb768e753a7f1ddca6dbf402548d741f33574
%global         gitdate         20180313
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})



# Build source is github release=1 or git commit=0
%global         build_release    0

%if 0%{?build_release}  > 0
Release:        3%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
#               not using 0. on the beginning of release as this git snapshot is past the 0.6.0 release
Release:        3.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release


# Use the glib CFLAGS and LDFLAGS during build where necessary
# https://github.com/DinoTools/dionaea/issues/161
Patch1:         dionaea-01_glib.patch

# Get rid of the warning about not used return value from chdir.
# https://github.com/DinoTools/dionaea/issues/162
Patch2:         dionaea-02_warnerror.patch

# ipv6 structures in <netinet/in.h> are used by the <sys/socket.h>
# ipv6 structures needs explicit CFLAGS " -D_GNU_SOURCE" to compile on linux
# just cosmetics - not reported yet to upstream
Patch3:         dionaea-03_in6_pktinfo.patch

# Unbundle the pyev library and use the system one
# https://github.com/DinoTools/dionaea/issues/166
Patch4:         dionaea-04_pyev.patch

# Have a dedicated variable for the python sitelib, so it can be easily changed externally when building the system package.
# https://github.com/DinoTools/dionaea/issues/164
Patch5:         dionaea-05_sitelib.patch

# Fix warnings during the generation of documentation
# Patch6:         dionaea-06_docswarn.patch

# Fix configure not finding the cython on RHEL7/Centos7
Patch7:         dionaea-07_cython_el7.patch

# Fix hardcoded lib dir
Patch8:         dionaea-08_modules_libdir.patch


BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  pkgconfig
BuildRequires:  sqlite

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

%if 0%{?fedora} >= 26
BuildRequires:  compat-openssl10-devel
%else
BuildRequires:  openssl-devel
%endif


# Optional dependencies
BuildRequires:  loudmouth-devel
BuildRequires:  libnetfilter_queue-devel
BuildRequires:  libnl3-devel

# Missing dependencies


BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-Cython


# Documentation generation
%if  0%{?rhel} == 7
BuildRequires:  python-sphinx
%else
BuildRequires:  python3-sphinx
%endif


%description
Dionaea honeypot is meant to be a nepenthes successor, embedding python
as scripting language, using libemu to detect shellcodes, supporting
ipv6 and tls.



# ============= documentation package ==========================================
%package -n %{name}-doc
Summary:        Documentation for the dionaea honeypot package
Group:          Development/Libraries

%description -n %{name}-doc
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
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
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
    conf/services/sip.yaml.in \
    conf/services/http.yaml.in \
    conf/services/ftp.yaml.in \
    conf/ihandlers/log_db_sql.yaml.in \
    conf/ihandlers/virustotal.yaml.in \
    conf/ihandlers/log_incident.yaml.in \
    conf/ihandlers/fail2ban.yaml.in \
    conf/ihandlers/log_json.yaml.in

# Change the hardoced minor python3.2 version especially in shabang to python3
# https://github.com/DinoTools/dionaea/issues/169
sed -i -e 's|python3.2|python3|g;' \
    m4/az_python.m4 \
    doc/html/index.html \
    modules/python/util/readlogsqltree.py



# ============= Build ==========================================================
%build
autoreconf -vif
%configure --enable-python --with-python=`which python3` --with-glib=glib --with-nl-include=/usr/include/libnl3
make %{?_smp_mflags} CFLAGS="%{optflags} -Wno-error -D_GNU_SOURCE -std=c99"
cd doc
make html
make man
cd ..



# ============= Install ========================================================
%install
%make_install PYTHON_SITELIB=%{python3_sitelib} PYTHON_SITEARCH=%{python3_sitearch}

# *.a *.la files not allowed for fedora
find %{buildroot} '(' -name '*.a' -o -name '*.la' ')' -delete

install -d %{buildroot}%{_mandir}/man1/
install doc/build/man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1.gz
mv doc/build/html/ ./html

mkdir -p %{buildroot}/var/dionaea/roots/tftp




# ============= Clean ==========================================================
%clean
#Cleanup the buildroot for compatibility with EPEL7
rm -rf %{buildroot}



# ============= package files ==================================================
%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/gnuplotsql
%{_bindir}/readlogsqltree
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_mandir}/man1/%{name}.1.gz
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%dir %{_var}/lib/%{name}
%{_var}/lib/%{name}/*



%files -n %{name}-doc
%doc README.md
%doc html



%files -n python%{python3_pkgversion}-%{gitname}
%license LICENSE
%doc README.md
%dir %{python3_sitelib}/%{name}
%dir %{python3_sitearch}/%{name}
%{python3_sitelib}/%{name}/*
%{python3_sitearch}/%{name}/*
%{python3_sitearch}/%{name}-*egg-info


%changelog
* Wed Mar 21 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-0.3.20180313gitd2efb76
- fix openssl dependency for EPEL7 build

* Wed Mar 21 2018 Michal Ambroz <rebus at, seznam.cz> 0.6.0-0.2.20180313gitd2efb76
- bump to commit d2efb768e753a7f1ddca6dbf402548d741f33574
- unbundle pyev and refer to system-installed pyev
- remove the hardcoded default prefix /opt/dionaea
- move from /var/dionaea to /var/lib/dionaea
- fix the doc generation warnings

* Thu Dec 28 2017 Michal Ambroz <rebus at, seznam.cz> 0.6.0-0.1
- initial package

