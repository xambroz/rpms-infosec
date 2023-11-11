Name:           libcthreads
Summary:        Libyal library for cross-platform C threads functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcthreads

%global         gituser         libyal
%global         gitname         libcthreads
%global         gitdate         20231025
%global         commit          a4276aec3255c4902ecb71a72cd852d00cce7df8
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Version:        %{gitdate}
Release:        1%{?dist}

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
# Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

# Lower requirements for rhel
Patch1:         %{name}-configure.ac.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcerror-devel

%description
Library for cross-platform C threads functions.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
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
* Fri Oct 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20231025-1
- bump to 20231025

* Tue Jun 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20220102-1
- bump to 20220102

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160402-1
- bump to 20160402

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150407-1
- Initial build for Fedora
