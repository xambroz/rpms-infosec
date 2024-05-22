Name:           libfguid
Summary:        Libyal library for GUID/UUID data types
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libfguid
Version:        20240415

%global         gituser         libyal
%global         gitname         libfguid
%global         gitdate         %{version}
%global         commit          c79feddbafec7d24df8c661e8c9be1417d4dedf4
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        1%{?dist}

Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-000-libs.patch

# Allow older autotools for EPEL builds
Patch1:         %{name}-001-configure.ac.patch


#
Patch1:         %{name}-configure.ac.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel

%description
Library for GUID/UUID data types.

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
* Mon May 13 2024 Michal Ambroz <rebus AT seznam.cz> - 20240415-1
- bump to 20240415

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160426-1
- bump to 20160426

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
