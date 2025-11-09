Name:           libexe
Version:        20240630
Release:        %autorelease
Summary:        Libyal library for cross-platform C error functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libexe
VCS:            https://github.com/libyal/libexe
#               https://github.com/libyal/libexe/releases


%global         gituser         libyal
%global         gitname         libexe
%global         gitdate         20240630
%global         commit          54e083ae780131d8bd0eaad58de7141d49a5e25a
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  python3

Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# https://github.com/libyal/libexe/pull/10
# Allow older autotools for EPEL builds
Patch0:        libexe-000-libs.patch

# there are older versions of gettext and autoconf, but still builds well
Patch1:         libexe-001-configure.ac.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel

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
BuildRequires:  libfdatetime-devel

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-libs
%endif


%description
Library for cross-platform C error functions.

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
%{?python_provide:%python_provide python%{python3_pkgversion}-pyexe}
# compatibility with the upstream package
Provides:       %{name}-python3

# Runtime dependencies
# Requires:       python%%{python3_pkgversion}-???

%description -n python%{python3_pkgversion}-%{name}
This is a Python3 library that gives access to functionality of %{name} library.
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
        --disable-static \
        --enable-wide-character-type

%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
%if %{with python3}
export PYTHON=python3
%endif

make check || cat tests/test-suite.log


%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/*.so.*
%{_bindir}/exeinfo
%{_mandir}/man1/exeinfo.1*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%if %{with python3}
%files -n python%{python3_pkgversion}-%{gitname}
%license COPYING
%{python3_sitearch}/pyexe.so
%endif

%changelog
%{?%autochangelog: %autochangelog }
