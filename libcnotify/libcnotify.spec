Name:           libcnotify
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcnotify
Summary:        Libyal library for cross-platform C generic data functions

%global         gituser         libyal
%global         gitname         libcnotify
%global         gitdate         20230610
%global         commit          92cd859fd5b7b0f75e40206fdd188b63c3fb946c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Version:        %{gitdate}
Release:        1%{?dist}

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

Patch1:         https://patch-diff.githubusercontent.com/raw/libyal/libcnotify/pull/4.patch#/%{name}-configure.ac.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel

%description
Library for cross-platform C generic data functions.

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
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%files
%license COPYING COPYING.LESSER
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Fri Oct 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20230610-1
- bump to 20230610

* Wed Jun 28 2023 Michal Ambroz <rebus AT seznam.cz> - 20220108-1
- bump to 20220108

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160422-1
- bump to 20160422 - related to libewf release 20160424

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
