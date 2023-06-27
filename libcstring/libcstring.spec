%global         gituser         libyal
%global         gitname         libcstring
%global         gitdate         20180218
%global         commit          9a6461ffcdaaa0cda5dd4736b0298de7b1e99aaa
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Previous versions
# %%global      commit          284f0aced7694cb79870757de5082a65947b65af
# %%global      commit          e4d51d13148780502371622f778b2e639f7cbf11


Name:           libcstring
Version:        %{gitdate}
Release:        1%{?dist}
Summary:        Libyal library for cross-platform C string functions

Group:          System Environment/Libraries
License:        Not a valid license string. Pass '--verbose' to get full parser error.
#URL:           https://github.com/libyal/libcstring
URL:            https://github.com/%{gituser}/%{gitname}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz


%description
Library for cross-platform C string functions.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{gitname}-%{commit}
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
* Fri Feb 18 2022 Michal Ambroz <rebus AT seznam.cz> - 20180218-1
- rebuild on bump for libevtx 2017

* Mon Jul 03 2017 Michal Ambroz <rebus AT seznam.cz> - 20160425-3
- rebuild on bump for libevtx 2017

* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160425-2
- bump for libewf 20160425

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150101-1
- Initial build for Fedora
