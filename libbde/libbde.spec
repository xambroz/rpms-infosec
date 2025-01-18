Name:           libbde
Version:        20240502
Release:        %autorelease
Summary:        Library to access the BitLocker Drive Encryption (BDE) format
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libbde
# Releases      https://github.com/libyal/libbde/releases

%global         gituser         libyal
%global         gitname         libbde
%global         gitdate         20240502
%global         commit          a7bf86d0907b84dfb551fdd3f6f548bd687fdcac
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  openssl-devel
BuildRequires:  libcerror-devel
BuildRequires:  libcthreads-devel
BuildRequires:  libcdata-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel
BuildRequires:  libbfio-devel
BuildRequires:  libfcache-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfdatetime-devel
BuildRequires:  libfguid-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libhmac-devel
BuildRequires:  libcaes-devel


%description
Library to access the BitLocker Drive Encryption (BDE) format


%package        devel
Summary:        Header files and libraries for developing applications for libbde
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     python3-libbde
Summary:        Python 3 bindings for libbde
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release} python3
BuildRequires:  python3-devel

%description -n python3-libbde
Python 3 bindings for libbde


%prep
%autosetup -n %{gitname}-%{commit}
./autogen.sh


%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --disable-static --enable-wide-character-type --enable-python3
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
make check


%files
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%files -n python3-libbde
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so




%changelog
%autochangelog
