# ===== Deprecated =====

Name:           libcsystem
Version:        20160425
Release:        1%{?dist}
Summary:        Libyal library for cross-platform C system functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcsystem
# Releases      https://github.com/libyal/libcsystem/releases

%global         gituser         libyal
%global         gitname         libcsystem
%global         gitdate         %{version}
%global         commit          c37249de9a16e4988042f96a93868d97e34568bd
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libuna-devel

%description
Library for cross-platform C system functions.

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
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to 20160425

* Tue Jul 7 2015 Michal Ambroz <rebus AT seznam.cz> - 20150629-1
- patch level tagged as release 20150629

* Tue Jun 30 2015 Michal Ambroz <rebus AT seznam.cz> - 20150101-2
- update to patch level 749d980f5f706d04897d2ae08b77594933a5f7f1 to fix build of libodraw

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150101-1
- Initial build for Fedora
