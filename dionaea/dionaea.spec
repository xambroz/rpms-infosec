Name:           dionaea
Version:        0.6.0
Summary:        Low interaction honeypot.
Group:          Applications/System
# Exception - it is permitted to link modified binary files in the src/ directory against
# the openssl libraries without breaking the license of dionaea
License:        GPLv2 with exceptions
URL:            https://dionaea.readthedocs.io/
#    Current source:
#		https://github.com/DinoTools/dionaea
#    Original site (dissappeared in 2013, but still available from archives):
#               https://dionaea.carnivore.it
#    Another forks:
#               https://github.com/rep/dionaea
#               https://gitlab.labs.nic.cz/honeynet/dionaea/
#               https://github.com/devwerks/dionaea
#               https://github.com/RootingPuntoEs/DionaeaFR/
#    Installation:
#		https://www.aldeid.com/wiki/Dionaea/Installation

# Specification of the used GIT commit
%global         gituser         DinoTools
%global         gitname         dionaea
%global         commit          793accd84432a77309fa8b81e1f5e9b5bd9ee7a3
%global         gitdate         20161114
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})



# Build source is github release=1 or git commit=0
%global         build_release    0

%if 0%{?build_release}  > 0
Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.1.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release


Patch0:         %{name}-warnerror.patch

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
BuildRequires:  compat-openssl10-devel
BuildRequires:  readline-devel
BuildRequires:  libpcap-devel
BuildRequires:  libsq3-devel
BuildRequires:  sqlite

# Optional dependencies
BuildRequires:  loudmouth-devel
BuildRequires:  libnetfilter_queue-devel
BuildRequires:  libnl3-devel

# Missing dependencies


BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-Cython


# Documentation generation
BuildRequires:  python3-sphinx



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


#Fix paths - remove the hardcoded prefix /opt/dionaea
sed -i -e "s|/opt/dionaea[/]*|/|g;" \
    modules/python/util/readlogsqltree.py \
    modules/python/util/logsql2postgres.py \
    modules/python/util/gnuplotsql.py \
    modules/python/util/updateccs.py \
    src/dionaea.c \
    vagrant/build.sh


# replace in documentation the prefix/destdir /opt/dionaea with variable ${DESTDIR}
sed -i -e "s|/opt/dionaea/var/dionaea|${DESTDIR}/var/lib/dionaea|g;" \
    doc/html/index.html \
    doc/source/old/run.rst \
    doc/source/old/configuration.rst \
    doc/source/old/utils.rst \
    modules/python/util/readlogsqltree.py


# move /var/dionaea to /var/lib/dionaea according to LFS
sed -i -e "s|/var/dionaea|/var/lib/dionaea|g;" \
    modules/python/util/readlogsqltree.py \
    modules/python/util/gnuplotsql.py

# move /var/dionaea to /var/lib/dionaea according to LFS
sed -i -e 's|\$(localstatedir)/dionaea/|\$(localstatedir)/lib/dionaea/|g;' \
    Makefile.am

# move /var/dionaea to /var/lib/dionaea according to LFS
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
sed -i -e 's|python3.2|python3|g;' \
    m4/az_python.m4 \
    doc/html/index.html \
    doc/source/old/development.rst \
    modules/python/util/readlogsqltree.py



# ============= Build ==========================================================
%build
autoreconf -vif
%configure --enable-python --with-python=`which python3` --with-glib=glib --with-nl-include=/usr/include/libnl3
make %{?_smp_mflags} CFLAGS="%{optflags} -Wno-error -D_GNU_SOURCE"
cd doc
make html
make man
cd ..



# ============= Install ========================================================
%install
%make_install PYTHON_SITELIB=%{python3_sitelib} PYTHON_SITEARCH=%{python3_sitearch}

# *.a *.la files not allowed for fedora
find %{buildroot} -name '*.a' -o -name '*.la' -delete

install -d %{buildroot}%{_mandir}/man1/
install doc/build/man/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1.gz
mv doc/build/html/ ./html



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
* Thu Dec 28 2017 Michal Ambroz <rebus at, seznam.cz> 0.6.0-1
- initial package

