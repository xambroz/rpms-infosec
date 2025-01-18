Name:           libclocale
Version:        20240414
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libclocale
#               https://github.com/libyal/libclocale/releases

%global         gituser         libyal
%global         gitname         libclocale
%global         gitdate         20240414
%global         commit          45b989bec6c5578b762f5b13dbce03aa2e999426
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease
Summary:        Libyal library for cross-platform C locale functions

Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

Patch1:         https://github.com/libyal/libclocale/pull/7.patch#/%{name}-configure.ac.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel

%description
Library for cross-platform C locale functions.

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
%autochangelog
