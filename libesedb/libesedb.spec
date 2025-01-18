Name:           libesedb
Version:        20240420
Summary:        Library to access the Extensible Storage Engine (ESE) Database File (EDB) format
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libesedb
#               https://github.com/libyal/libesedb/releases

%global         common_description %{expand:
Library and tools to access the Extensible Storage Engine (ESE) Database File
(EDB) format. ESEDB is used in may different applications like Windows Search,
Windows Mail, Exchange, Active Directory, etc.}


%global         gituser         libyal
%global         gitname         libesedb
%global         gitdate         20240420
%global         commit          24ae2ff47365adb5f1dcdce315ac7dd16b972836
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease

# Build with python3 package by default
%bcond_without  python3


# Source0:      https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        %{url}/releases/download/%{version}/%{gitname}-experimental-%{version}.tar.gz

# Patch build to use the shared system libraries rather than using embedded ones
# Patch0:         %%{name}-libs.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# if with_python3
%endif

Provides: bundled(libbfio)      = 20180910
Provides: bundled(libcdata)     = 20181228
Provides: bundled(libcerror)    = 20181117
Provides: bundled(libcfile)     = 20180102
Provides: bundled(libclocale)   = 20180721
Provides: bundled(libcnotify)   = 20180102
Provides: bundled(libcpath)     = 20181228
Provides: bundled(libcsplit)    = 20180103
Provides: bundled(libcthreads)  = 20180724
Provides: bundled(libfcache)    = 20181011
Provides: bundled(libfdata)     = 20181216
Provides: bundled(libfdatetime) = 20180910
Provides: bundled(libfguid)     = 20180724
Provides: bundled(libfmapi)     = 20180714
Provides: bundled(libfvalue)    = 20180817
Provides: bundled(libfwnt)      = 20181227
Provides: bundled(libmapidb)    = 20170304
Provides: bundled(libuna)       = 20181006

%description
%{common_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%{common_description}


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-pyesedb
Summary:        Python3 binding for the library reading of esedb format
%{?python_provide:%python_provide python%{python3_pkgversion}-pyesedb}

%description -n python%{python3_pkgversion}-pyesedb
Python3 binding for the librarye reading of esedb format
%{common_description}
%endif


%prep
%autosetup -n %{gitname}-%{version}
#./autogen.sh
autoreconf --force --install
aclocal


%build
%configure --disable-static \
%if 0%{?with_python3}
           --enable-python3 \
%endif
           --enable-wide-character-type \
           --enable-multi-threading-support

%make_build


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
make check


%files
%doc COPYING AUTHORS
%{_libdir}/*.so.*
%{_bindir}/esedbexport
%{_bindir}/esedbinfo
%{_mandir}/man1/esedbinfo.1.*
%{_mandir}/man3/libesedb.3.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libesedb.pc

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-pyesedb
%{python3_sitearch}/pyesedb*
%endif


%changelog
%autochangelog
