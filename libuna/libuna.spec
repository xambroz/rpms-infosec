Name:           libuna
Version:        20240414
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
%global         gitdate         20240414
%global         commit          ee21db63eed2820396cff0a7442e408c028535f2
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        1%{?dist}
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
# %%autopatch -M 99
%patch0 -p 1
%patch1 -p 1

%if %{with bootstrap}
# %%autopatch -m 100
%patch100 -p 1
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
* Mon May 13 2024 Michal Ambroz <rebus AT seznam.cz> - 20240414-1
- bump to 20240414

* Mon Oct 30 2023 Michal Ambroz <rebus AT seznam.cz> - 20230710-1
- bump to 20230710

* Wed Jun 28 2023 Michal Ambroz <rebus AT seznam.cz> - 20220611-1
- bump to 20220611

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160705-1
- bump to 20160705

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160501-1
- bump to 20160501

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
