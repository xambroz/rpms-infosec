%global         gituser         libyal
%global         gitname         libsmdev
#20150105
%global         commit          a747d84ac719669f10da783fd704adc8f2dadf6e
#20160524
%global         commit          d0e71d9e5e8a1a3fff07cc945f65fb7c1b50d4d4
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libsmdev
Version:        20160524
Release:        1%{?dist}
Summary:        Libyal library to access to storage media devices

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libsmdev
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
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcsystem-devel

%description
Library to access to storage media devices

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


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%check
make check


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%{_bindir}/smdevinfo
%{_mandir}/man1/smdevinfo.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160524-1
- bump to 20160524

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-1
- Initial build for Fedora
