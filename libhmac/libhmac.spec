Name:           libhmac
Version:        20240417
Summary:        Libyal library to support various Hash-based Message Authentication Codes (HMAC)
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libhmac
URL:            https://github.com/%{gituser}/%{gitname}

%global         gituser         libyal
%global         gitname         libhmac
%global         gitdate         20240417
%global         commit          7ce99ac975e27be8e19eea9accf5ffce0304fe8a
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  python3


Release:        1%{?dist}
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-000-libs.patch

# Allow older autotools for EPEL builds
Patch1:         %{name}-001-configure.ac.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-libs
%endif


%description
Library to support various Hash-based Message Authentication Codes (HMAC).

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with python3}
%package        -n python%{python3_pkgversion}-%{name}
Summary:        Python3 binding for %{name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

# Runtime dependencies
# Requires:       python%%{python3_pkgversion}-???

%description -n python%{python3_pkgversion}-%{name}
This is a Python3 library that gives access to dionaea honeypot functionality.
%endif



%prep
%autosetup -n %{gitname}-%{commit}
#%%patch0 -p 1 -b .libs
./autogen.sh


%build
%configure \
%if %{with python3}
 --enable-python \
%endif
--enable-wide-character-type \
--disable-static


%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
%if %{with python3}
export PYTHON=python3
%endif
make check


%files
%doc AUTHORS NEWS README
%license COPYING
%{_libdir}/*.so.*
%{_bindir}/hmacsum
%{_mandir}/man1/hmacsum.1.gz


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*


%if %{with python3}
%files -n python%{python3_pkgversion}-%{gitname}
%license COPYING
%{python3_sitearch}/pyhmac.so
%endif


%changelog
* Sat May 18 2024 Michal Ambroz <rebus AT seznam.cz> - 20240417-1
- bump to 20240417

* Fri Feb 18 2022 Michal Ambroz <rebus AT seznam.cz> - 20200104-1
- bump to 20200104

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160802-1
- bump to 20160802 - WINCRYPT

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160731-1
- bump to 20160731

* Tue Jul 07 2015 Michal Ambroz <rebus AT seznam.cz> - 20150703-1
- bump to release 20150703

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
