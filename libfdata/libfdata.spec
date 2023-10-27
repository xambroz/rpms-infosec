%global         gituser         libyal
%global         gitname         libfdata
#20150412
#%global        commit          1d2e7f0edff9d676ccc3e96d40926d83d63af1e5
#20160427
%global         commit          8c27dc70272dec0c28d47fea8603c4f4aacdada7
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libfdata
Version:        20160427
Release:        1%{?dist}
Summary:        Libyal library to provide generic file data functions

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libfdata
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
BuildRequires:  libfcache-devel

%description
Library to provide generic file data functions.

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

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160427-1
- bump to 20160427

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150412-1
- Initial build for Fedora
