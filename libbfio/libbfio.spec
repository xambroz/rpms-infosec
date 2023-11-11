%global         gituser         libyal
%global         gitname         libbfio
#20150102
#%global        commit          00a9e6e0644147d4ad44466ac9e2d58a8c6a8476
#20160528
%global         commit          26abccb427951b4da00f99fd46774863582b53e5
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libbfio
Version:        20160528
Release:        1%{?dist}
Summary:        Library to provide basic file input/output abstraction

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libbfio
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
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel

%description
Library to provide basic file input/output abstraction.

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
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160528-1
- bump to 20160528

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150102-1
- Initial build for Fedora
