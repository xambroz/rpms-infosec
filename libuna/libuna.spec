%global         gituser         libyal
%global         gitname         libuna
#20150101
#%global        commit          b9129d8786bf86d67c945df5ebc370a3455e07ca
#20150927
#%global        commit          3efc9ac2d4c73ffbb0da1d66308b8a41c328bc9a
#20160501 - from 20160502
#%global        commit          b818506074ed974dc09ac3101bb75d20dfa0a06a
#20160705
%global         commit          2db49f6cd8a225c038e7a51dc4c686f9dbf1fca6
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libuna
Version:        20160705
Release:        1%{?dist}
Summary:        Libyal library to support Unicode and ASCII (byte string) conversions

Group:          System Environment/Libraries
License:        LGPLv3+
#URL:           https://github.com/libyal/libuna
URL:            https://github.com/%{gituser}/%{gitname}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcstring-devel
BuildRequires:  libcerror-devel

%description
Library to support Unicode and ASCII (byte string) conversions.

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
%make_build


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm %{buildroot}%{_mandir}/man1/unaexport.1*

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
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160705-1
- bump to 20160705

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160501-1
- bump to 20160501

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
