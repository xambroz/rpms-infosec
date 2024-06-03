Name:           libregf
Version:        20240421
Summary:        Libyal library for cross-platform C error functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libregf
#               https://github.com/libyal/libregf/releases

%global         gituser         libyal
%global         gitname         libregf
%global         gitdate         20240421
%global         commit          51edeb225ffcaf6f9f3b27248eafc67f6d07ba84
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:        1%{?dist}

Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# https://github.com/libyal/libregf/pull/10
# there are older versions of gettext and autoconf, but still builds well
Patch0:         libregf-configure.ac.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel

%description
Library for cross-platform C error functions.

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
* Mon Jun 03 2024 Michal Ambroz <rebus _AT seznam.cz> - 20240421-1
- bump to 20240421

* Mon May 13 2024 Michal Ambroz <rebus AT seznam.cz> - 20240413-1
- bump to 20240413

* Fri Oct 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20231024-2
- lower build requirements for rhel

* Fri Oct 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20231024-1
- bump to 20231024

* Tue Jun 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20220101-1
- bump to 20220101

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160507-1
- bump to 20160507

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160327-1
- bump to 20160327

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150407-1
- Initial build for Fedora
