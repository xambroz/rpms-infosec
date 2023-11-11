Name:           libcfile
Summary:        Libyal library for cross-platform C file functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcfile

%global         gituser         libyal
%global         gitname         libcfile
%global         gitdate         20230608
%global         commit          fab8185019d05762f807b4128c80fc4a7d3f62c7
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Version:        %{gitdate}
Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcstring-devel
BuildRequires:  libcerror-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libclocale-devel
BuildRequires:  libuna-devel

%description
Library for cross-platform C file functions.

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
* Fri Oct 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20230608-1
- bump to 20230608

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160423-1
- bump to 20160423

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150101-1
- Initial build for Fedora
