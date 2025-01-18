Name:           liblnk
Version:        20241015
Summary:        Libyal library for cross-platform C file functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/liblnk
#               https://github.com/libyal/liblnk/releases

%global         gituser         libyal
%global         gitname         liblnk
%global         gitdate         20241015
%global         commit          00e03ad49fd9610d2941388ebab08ff2dc8affde
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %aurorelease
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-000-libs.patch

# Allow older autotools for EPEL builds
Patch1:         %{name}-001-configure.ac.patch



BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
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
BuildRequires:  libfdatetime-devel
BuildRequires:  libfguid-devel
BuildRequires:  libfole-devel
BuildRequires:  libfwps-devel
BuildRequires:  libfwsi-devel


%description
Library for cross-platform C file functions.

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
%autosetup -n %{gitname}-%{commit} -p 1
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
%autochangelog
