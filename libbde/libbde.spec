%global         gituser         libyal
%global         gitname         libbde
%global         gitdate         20220121
%global         commit          ac7bb8586041b69e56e3dbbcbeb0ccb19917c88e
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libbde
Version:        %{gitdate}
Release:        1%{?dist}
Summary:        Library to support cross-platform AES encryption 

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            https://github.com/libyal/libbde
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
BuildRequires:  libbfio-devel
BuildRequires:  libfcache-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfdatetime-devel
BuildRequires:  libfguid-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libhmac-devel
BuildRequires:  libcaes-devel

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
%setup -qn %{gitname}-%{commit}
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
* Fri Feb 18 2022 Michal Ambroz <rebus AT seznam.cz> - 20220121-1
- bump to 20220121

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160418-1
- Initial build for Fedora
