%global         gituser         libyal
%global         gitname         libcaes
%global         commit          c36c49b2b2f330d2769b8a896c4f2539a757162e
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libcaes
Version:        20160425
Release:        1%{?dist}
Summary:        Libyal library to support cross-platform AES encryption 

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libcaes
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
BuildRequires:  libcthreads-devel

%description
Library to support cross-platform AES encryption.

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
* Fri Jun 24 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to 20160425

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150514-1
- Initial build for Fedora
