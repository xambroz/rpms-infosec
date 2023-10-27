Name:           libcdatetime
Summary:        Libyal library for cross-platform C date and time functions
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libcdatetime

%global         gituser         libyal
%global         gitname         libcdatetime
%global         gitdate         20230606
%global         commit          a65c5494daf193f5a1ff14ffa1c40291069b0829
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Version:        %{gitdate}
Release:        1%{?dist}

Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

# Lower build requirements for rhel
Patch1:         https://github.com/libyal/libcdatetime/pull/1.patch#/%{name}-configure.ac.patch


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  libcstring-devel
BuildRequires:  libcerror-devel

%description
Library for cross-platform C date and time functions.

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
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%files
%license COPYING COPYING.LESSER
%doc AUTHORS NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Tue Jun 27 2023 Michal Ambroz <rebus AT seznam.cz> - 20230115-1
- bump to 20230115

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-1
- bump to 20160425 - related to libewf release 20160224

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150407-1
- Initial build for Fedora
