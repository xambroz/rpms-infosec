Name:           libcpath
Version:        20240414
Release:        1%{?dist}
Summary:        Libyal library for cross-platform C path functions

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcpath
VCS:            https://github.com/libyal/libcpath

%global         gituser         libyal
%global         gitname         libcpath
#20240414
%global         commit          fcc7645b094e904cfb57ce5eb9e7515ad12b420f
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
BuildRequires:  libcstring-devel
BuildRequires:  libcerror-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel

%description
Library for cross-platform C path functions.

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
* Sat Apr 20 2024 Michal Ambroz <rebus AT seznam.cz> - 20240414-1
- bump to 20240414

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to 20160425

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150101-1
- Initial build for Fedora
