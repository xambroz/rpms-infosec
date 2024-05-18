Name:           libcsplit
Version:        20240414
Summary:        Libyal library for cross-platform C split string functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcsplit

%global         gituser         libyal
%global         gitname         libcsplit
%global         gitdate         %{version}
%global         commit          b4baf41a06421aaf725b11ebed8c040ad34e8761
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:        1%{?dist}
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch
Patch1:         https://github.com/libyal/libcsplit/pull/3.patch#/%{name}-configure.ac.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel

%description
Library for cross-platform C cplit string functions.

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
* Sat May 18 2024 Michal Ambroz <rebus AT seznam.cz> - 20240414-1
- bump to 20240414

* Sat Oct 28 2023 Michal Ambroz <rebus AT seznam.cz> - 20230612-1
- bump to 20230612

* Wed Jun 28 2023 Michal Ambroz <rebus AT seznam.cz> - 20220109-1
- bump to 20220109

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to 20160425

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
