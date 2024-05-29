Name:           libcdata
Version:        20240414
Summary:        Libyal library for cross-platform C generic data functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcdata
#               https://github.com/libyal/libcdata/releases

%global         gituser         libyal
%global         gitname         libcdata
%global         gitdate         20240414
%global         commit          ed66801e97c516c405486508d280fda3e8114e9d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        1%{?dist}

Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
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
* Mon May 13 2024 Michal Ambroz <rebus AT seznam.cz> - 20240414-1
- bump to 20240414

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
