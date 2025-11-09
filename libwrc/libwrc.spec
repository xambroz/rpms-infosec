Name:           libwrc
Version:        20240610
Release:        %autorelease
Summary:        Libyal library and tools to access the Windows SuperFetch database format
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libwrc
VCS:            git:https://github.com/libyal/libwrc
#               https://github.com/libyal/libwrc/releases

%global         gituser         libyal
%global         gitname         libwrc
%global         gitdate         %{version}
%global         commit          b4b358785237344d9dbad8b338cc3d7d1ac74a12
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         common_description %{expand:
libwrc is a library to access the SuperFetch database format.
Note that this project currently only focuses on the analysis of the format.}


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-000-libs.patch

# there are older versions of gettext and autoconf, but still builds well
Patch1:         libwrc-001-configure.ac.patch

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
BuildRequires:  libfcache-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfdatetime-devel
BuildRequires:  libfdatetime-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libfwnt-devel
BuildRequires:  libfguid-devel
BuildRequires:  libexe-devel




%description    %{common_description}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel    %{common_description}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{gitname}-%{commit}
./autogen.sh


%build
%configure --disable-static --enable-wide-character-type --enable-python
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%check
make check


%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/*.so.*
%{_bindir}/agdbinfo
%{_mandir}/man1/agdbinfo.1*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
%autochangelog

