Name:           libuna
Summary:        Libyal library to support Unicode and ASCII (byte string) conversions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libuna

# Bootstrap round dependency to libcfile
%bcond_with     bootstrap

%global         gituser         libyal
%global         gitname         libuna
%global         gitdate         20220611
%global         commit          0bec9356d6c9fd2684defa2807752e39c5d34014
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Version:        %{gitdate}
Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:         %{name}-libs.patch
%if %{with bootstrap}
Patch1:         %{name}-bootstrap.patch
%endif

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel
BuildRequires:  libcdatetime-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
%if %{without bootstrap}
BuildRequires:  libcfile-devel
%endif

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
%autosetup -n %{gitname}-%{commit}
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
* Wed Jun 28 2023 Michal Ambroz <rebus AT seznam.cz> - 20220611-1
- bump to 20220611

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160705-1
- bump to 20160705

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160501-1
- bump to 20160501

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
