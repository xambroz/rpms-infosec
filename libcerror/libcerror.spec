Name:           libcerror
Version:        20241013
Release:        %autorelease
Summary:        Libyal library for cross-platform C error functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcerror
VCS:            git:https://github.com/libyal/libcerror
#               https://github.com/libyal/libcerror/releases

%global         gituser         libyal
%global         gitname         libcerror
%global         gitdate         %{version}
%global         commit          0f0d145fe63f2769ceac76d5425a0bb10d5e304f
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         common_description %{expand:
Library for cross-platform C error functions.}


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# https://github.com/libyal/libcerror/pull/10
# there are older versions of gettext and autoconf, but still builds well
Patch1:         libcerror-001-configure.ac.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel

%description %{common_description}

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

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
%{?%autochangelog: %autochangelog }
