Name:           libcaes
Version:        20240922
Summary:        Libyal library to support cross-platform AES encryption 
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcaes
# Releases      https://github.com/libyal/libcaes/releases

%global         common_description %{expand:
Library to support cross-platform AES encryption.
}

%global         gituser         libyal
%global         gitname         libcaes
%global         gitdate         20240922
%global         commit          3ed36e5ef7ba2b4e2eb3950ea713d5cc9f93e303
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease

Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-000-libs.patch

# Allow older autotools for EPEL builds
Patch1:         %{name}-001-configure.ac.patch

# Testsuite to use python3 instead of unversioned python in scripts
Patch2:         https://github.com/libyal/libcaes/pull/20.patch#/%{name}-002-python3.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  openssl-devel
BuildRequires:  libcerror-devel

%description
%{common_description}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%{common_description}


%package     -n python%{python3_pkgversion}-%{name}
Summary:        Python3 package for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# needed for tests
BuildRequires:  /usr/bin/python

%description -n python%{python3_pkgversion}-%{name}
Python 3 bindings for %{name}
%{common_description}


%prep
%autosetup -p 1 -n %{gitname}-%{commit}
#%%patch0 -p 1 -b .libs
./autogen.sh


%build
%configure --enable-shared --disable-static \
    --with-openssl --enable-openssl-evp-cipher --enable-openssl-evp-md \
    --enable-python
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
make check


%files
%doc AUTHORS NEWS README
%license COPYING COPYING.LESSER
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%files -n python%{python3_pkgversion}-%{name}
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.so

%changelog
%autochangelog
