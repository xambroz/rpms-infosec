%global         gituser         libyal
%global         gitname         libmapidb
#20150105
#%global        commit          4db7d4fed43b960f5fa60b47987cdc4d8e59df40
#20160508
%global         commit          0ce0464f45bddb81effaa845abd639dbfbd1264d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libmapidb
Version:        20160508
Release:        1%{?dist}
Summary:        Libyal library for cross-platform C generic data functions

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libmapidb
URL:            https://github.com/%{gituser}/%{gitname}
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

%description
Library for accessing the Exchange MAPI database format.

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
%patch0 -p 1 -b .libs
./autogen.sh


%build
%configure --disable-static --enable-wide-character-type
%make_build


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


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
* Wed Aug 03 2016 Michal Ambroz <rebus AT seznam.cz> - 20160508-1
- bump to 20160508

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-1
- Initial build for Fedora
