Name:           libfdatetime
Version:        20240415
Summary:        Libyal library for date and time data types
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libfdatetime
#               https://github.com/libyal/libfdatetime/releases

%global         gituser         libyal
%global         gitname         libfdatetime
%global         gitdate         20240415
%global         commit          133ca426176073d54f4e5eb1f7f61a39e0050fe2
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:        1%{?dist}

Group:          System Environment/Libraries
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

%description
Library for date and time data types.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{gitname}-%{commit}
#%%patch0 -p 1 -b .libs
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
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160426-1
- bump to 20160426

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150507-1
- Initial build for Fedora
