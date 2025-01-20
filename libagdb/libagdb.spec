Name:           libagdb
Version:        20240624
Release:        %autorelease
Summary:        Libyal library and tools to access the Windows SuperFetch database format
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libagdb
VCS:            git:https://github.com/libyal/libagdb
#               https://github.com/libyal/libagdb/releases

%global         gituser         libyal
%global         gitname         libagdb
%global         gitdate         %{version}
%global         commit          43389aefc12e2cad99a899ad4e8a5598d4f09081
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         common_description %{expand:
libagdb is a library to access the SuperFetch database format.
Note that this project currently only focuses on the analysis of the format.}


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-000-libs.patch

# there are older versions of gettext and autoconf, but still builds well
Patch1:         libagdb-001-configure.ac.patch

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
BuildRequires:  libfwnt-devel


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
%configure --disable-static --enable-wide-character-type
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
%{?%autochangelog: %autochangelog }
