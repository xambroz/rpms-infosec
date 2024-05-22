Name:           libscca
Version:        20240427
Release:        1%{?dist}
Summary:        Libyal libscca is a library to access the Windows Prefetch File (SCCA) format
URL:            https://github.com/libyal/libscca
VCS:            https://github.com/libyal/libscca
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later

%global         common_description %{expand:
Libyal libscca is a library to access the Windows Prefetch File (SCCA) format.
}


%global         gituser         libyal
%global         gitname         libscca
#20160425
%global         commit          691c2140cc18935e0e2d62baaffe992b39773e9e
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
# Patch build to use the shared system libraries rather than using embedded ones
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
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel
BuildRequires:  libbfio-devel
BuildRequires:  libfcache-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfdatetime-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libfwnt-devel



%description
%{common_description}


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
%{common_description}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{gitname}-%{commit}
./autogen.sh


%build
%configure --disable-static --enable-wide-character-type
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
make check


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Sat May 18 2024 Michal Ambroz <rebus _AT seznam.cz> - 20240427-1
- bump to 20240427

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to 20160425

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150101-1
- Initial build for Fedora
