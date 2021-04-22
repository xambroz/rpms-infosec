%global         gituser         libyal
%global         gitname         libcerror
#%global         commit          99cd8c5cde340ee87c636e67e7599ca873fcc2ca
#20160422 from 20160601
%global         commit          7ab34b933c538e54aca9df8910b2f3b402f67cab
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libcerror
Version:        20160422
Release:        1%{?dist}
Summary:        Libyal library for cross-platform C error functions

Group:          System Environment/Libraries
License:        LGPLv3+
#URL:            https://github.com/libyal/libcerror
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

%description
Library for cross-platform C error functions.

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
%setup -qn %{gitname}-%{commit}
%patch0 -p 1 -b .libs
./autogen.sh


%build
%configure --disable-static --enable-wide-character-type
make %{?_smp_mflags}


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
* Mon Jun 20 2015 Michal Ambroz <rebus AT seznam.cz> - 20160507-1
- bump to 20160507

* Mon Jun 20 2015 Michal Ambroz <rebus AT seznam.cz> - 20160327-1
- bump to 20160327

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150407-1
- Initial build for Fedora
