%global         gituser         libyal
%global         gitname         libfvalue
#20150322
#%global        commit          a5b2497f680b4d656f80be82fc82abce1b2e0352
#20160718
%global         commit          8b5638c730ac9f203fa14420a33e83273aa318e5
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libfvalue
Version:        20160718
Release:        1%{?dist}
Summary:        Libyal library for generic file value functions

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libfvalue
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
BuildRequires:  libcdata-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libuna-devel
BuildRequires:  libfdatetime-devel
BuildRequires:  libfguid-devel
BuildRequires:  libfwnt-devel

%description
Library for generic file value functions.

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
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160718-1
- bump to 20160718

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150322-1
- Initial build for Fedora
