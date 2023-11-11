Name:           libcdata
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcdata

%global         gituser         libyal
%global         gitname         libcdata
%global         gitdate         20230605
%global         commit          e4fde5bd4007e0a77d0e39a61fd36e4cb933e16c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Version:        %{gitdate}
Release:        1%{?dist}

Summary:        Libyal library for cross-platform C generic data functions

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

# Lower the build requirements for RHEL
Patch1:         https://github.com/libyal/libcdata/pull/7.patch#/libcdata-configure.ac.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel
BuildRequires:  libcthreads-devel

%description
Library for cross-platform C generic data functions.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
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
%license COPYING COPYING.LESSER
%doc AUTHORS NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Fri Oct 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20230605-1
- bump to 20230605

* Tue Jun 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20230108-1
- bump to 20230108

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-2
- add build dependencies

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to libewf release 20160224

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
