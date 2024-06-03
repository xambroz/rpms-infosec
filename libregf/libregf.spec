Name:           libregf
Version:        20240421
Release:        1%{?dist}
Summary:        Libyal library to access the Windows NT Registry File
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libregf
VCS:            https://github.com/libyal/libregf
# Releases      https://github.com/libyal/libregf/releases


%global         gituser         libyal
%global         gitname         libregf
%global         gitdate         20240421
%global         commit          51edeb225ffcaf6f9f3b27248eafc67f6d07ba84
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
BuildRequires:  libcerror-devel
BuildRequires:  libcthreads-devel
BuildRequires:  libcdata-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-libs
%endif


%description
Library and tools to access the Windows NT Registry File (REGF) format

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
%{?python_provide:%python_provide python%{python3_pkgversion}-pyregf}
# compatibility with the upstream package
Provides:        %{name}-python3 = %{version}-%{release}

# Runtime dependencies
# Requires:       python%%{python3_pkgversion}-???

%description -n python%{python3_pkgversion}-%{name}
This is a Python3 library that gives access to %{name}dionaea honeypot functionality.
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
%doc AUTHORS NEWS README
%license COPYING
%{_libdir}/*.so.*
%{_bindir}/smdevinfo
%{_mandir}/man1/smdevinfo.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*


%if %{with python3}
%files -n python%{python3_pkgversion}-%{gitname}
%license COPYING
%{python3_sitearch}/pyregf.so
%endif



%changelog
* Mon Jun 03 2024 Michal Ambroz <rebus _AT seznam.cz> - 20240421-1
- bump to 20240421
