Name:           libsmraw
Version:        20240506
Release:        %autorelease
Summary:        Libyal library and tools to access the (split) RAW image format
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libsmraw
VCS:            https://github.com/libyal/libsmraw
# Releases      https://github.com/libyal/libsmraw/releases


%global         gituser         libyal
%global         gitname         libsmraw
%global         gitdate         20240506
%global         commit          995b9e200ae8c836439f14741253143803fecb0c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  python3


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
BuildRequires:  fuse-devel
BuildRequires:  libcerror-devel
BuildRequires:  libcthreads-devel
BuildRequires:  libcdata-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel
BuildRequires:  libbfio-devel
BuildRequires:  libfcache-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libhmac-devel


%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-libs
%endif

%description
Library and tools to access the (split) RAW image format.

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
Summary:        Python3 extension that gives access to %{name} library
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%{?python_provide:%python_provide python%{python3_pkgversion}-pysmraw}
# compatibility with the upstream package
Provides:       %{name}-python3

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}
This is a Python3 module that gives access to %{name} library
from Python scripts.
# with_python3
%endif



%prep
%autosetup -n %{gitname}-%{commit}
./autogen.sh


%build
%if %{with python3}
export PYTHON=python3
%endif

%configure \
%if %{with python3}
        --enable-python \
%endif
        --disable-static --enable-wide-character-type \
	--enable-multi-threading-support --enable-verbose-output

%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
%if %{with python3}
export PYTHON=python3
%endif

make check || tests/test-suite.log


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%{_bindir}/smrawmount
%{_bindir}/smrawverify
%{_mandir}/man1/smrawmount.1*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%if %{with python3}
%files -n python%{python3_pkgversion}-%{gitname}
%license COPYING
%{python3_sitearch}/pysmraw*
%endif


%changelog
%{?%autochangelog: %autochangelog }
