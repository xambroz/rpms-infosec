Name:           libewf
Version:        20251106
Release:        %autorelease
Summary:        Libyal library for the Expert Witness Compression Format (EWF)

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libewf
# was URL:      http://sourceforge.net/projects/libewf/
# Releases      https://github.com/libyal/libewf/releases

%global         gituser         libyal
%global         gitname         libewf
%global         gitdate         20251106
%global         commit          87a4ea137581cdac474376dfe7db1eb8ee1df2d8
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


%bcond_with     python2
%bcond_without  python3


#Source0:       http://libewf.googlecode.com/files/libewf-%%{version}.tar.gz
#Source0:       https://53efc0a7187d0baa489ee347026b8278fe4020f6.googledrive.com/host/0B3fBvzttpiiSMTdoaVExWWNsRjg/%%{name}-%%{version}.tar.gz
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

#./libewf/.libs/libewf.so: undefined reference to `libcstring_narrow_string_compare'
#https://github.com/libyal/libewf/issues/51
Patch1:         %{name}-libcstring.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  fuse-devel
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
#Needed for mount.ewf(.py) support
BuildRequires:  libcerror-devel
BuildRequires:  libcthreads-devel
BuildRequires:  libcdata-devel
BuildRequires:  libcdatetime-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel
BuildRequires:  libbfio-devel
BuildRequires:  libfcache-devel
BuildRequires:  libfguid-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libhmac-devel
BuildRequires:  libcaes-devel
BuildRequires:  libodraw-devel
BuildRequires:  libsmdev-devel
BuildRequires:  libsmraw-devel

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# if with_python3
%endif


%description
Libewf is a library for support of the Expert Witness Compression Format (EWF),
it support both the SMART format (EWF-S01) and the EnCase format (EWF-E01). 
Libewf allows you to read and write media information within the EWF files.


%package -n     ewftools
Summary:        Utilities for the Expert Witness Compression Format (EWF)
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-tools = %{version}-%{release}
Obsoletes:      %{name}-tools <= %{version}-%{release}
#Requires:       disktype
Requires:       fuse-python3 >= 0.2

%description -n ewftools
Several tools for reading and writing EWF files.
It contains tools to acquire, verify and export EWF files.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with python2}
%package python2
Summary:        Python2 extension that gives access to %{name} library
Group:          Development/Libraries
%{?python_provide:%python_provide python2-%{name}}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description python2
This is a Python module that gives access to %{name} library
from Python scripts.
%endif



%if %{with python3}
%package python3
Summary:        Python3 extension that gives access to %{name} library
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

Requires:       %{name}%{?_isa} = %{version}-%{release}


%description python3
This is a Python3 module that gives access to %{name} library
from Python scripts.
# with_python3
%endif




%prep
%autosetup -n %{gitname}-%{commit}
#exit 1
#%%patch0 -p 1 -b .libs
#%%patch1 -p 1 -b .libcstrings
./autogen.sh


%build
%configure \
%if %{with python2}
  --enable-python2 \
%endif
%if %{with python3}
  --enable-python3
%endif
  --disable-static --enable-wide-character-type \
  --enable-multi-threading-support --enable-verbose-output


# Remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
make check


%files
%doc AUTHORS COPYING NEWS
%{_libdir}/*.so.*

%files -n ewftools
%{_bindir}/ewf*
%{_mandir}/man1/*.gz

%files devel
%{_includedir}/libewf.h
%{_includedir}/libewf/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libewf.pc
%{_mandir}/man3/%{name}.3*

%if %{with python2}
%files python2
%{python2_sitearch}/pyewf*
%{python2_sitearch}/pyewf.so
%endif

%if %{with python3}
%files python3
%{python3_sitearch}/pyewf*
%{python3_sitearch}/pyewf.so
%endif


%changelog
%{?%autochangelog: %autochangelog }
