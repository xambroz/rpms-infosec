Name:           libuna
Version:        20251108
Summary:        Libyal library to support Unicode and ASCII (byte string) conversions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libuna
#               https://github.com/libyal/libuna/releases

%global         common_description %{expand:
Library to support Unicode and ASCII (byte string) conversions.
}


# Bootstrap round dependency to libcfile
%bcond_with     bootstrap

%global         gituser         libyal
%global         gitname         libuna
%global         gitdate         20251108
%global         commit          85e9a613e78bcc5a61fa5c79e676fd280fcd840a
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# dynamically loaded libraries
Patch0:         %{name}-000-libs.patch

# Allow older autotools for EPEL builds
Patch1:         %{name}-001-configure.ac.patch

# ======= Only used with Bootstrap
# Allow bootstrapping to break the circular dependency
Patch100:         %{name}-100-bootstrap.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel
BuildRequires:  libcdatetime-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
%if %{without bootstrap}
BuildRequires:  libcfile-devel
%endif

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

%if %{without bootstrap}
%package        tools
Summary:        Unatools from the libuna package
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Unatools from the libuna package.
%{common_description}
%endif


%prep
%setup -q -n %{gitname}-%{commit}
# autopatch missing -m -M options in RHEL7
%autopatch -M 99

%if %{with bootstrap}
%autopatch -m 100
%endif
./autogen.sh


%build
%configure --disable-static --enable-wide-character-type
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm %{buildroot}%{_mandir}/man1/unaexport.1*


%ldconfig_scriptlets


%check
make check


%files
%license COPYING COPYING.LESSER
%doc AUTHORS NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%if %{without bootstrap}
%files tools
%{_bindir}/unabase
%{_bindir}/unaexport
%endif


%changelog
%{?%autochangelog: %autochangelog }
