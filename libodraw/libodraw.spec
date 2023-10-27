%global         gituser         libyal
%global         gitname         libodraw
#20150629
%global         commit          4dfb027dc608dc871bdf3a66c63193c24b189243
#20160522
%global         commit          e2750dd19836b7f1a603e55d1f64eb087401f87a
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libodraw
Version:        20160522
Release:        1%{?dist}
Summary:        Libyal library to access to optical disc (split) RAW image files (bin/cue, iso/cue)

Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
#URL:           https://github.com/libyal/libodraw
URL:            https://github.com/%{gituser}/%{gitname}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Patch build to use the shared system libraries rather than using embedded ones
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  byacc
BuildRequires:  flex
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
BuildRequires:  libcsystem-devel
BuildRequires:  libhmac-devel

%description
Library to access to optical disc (split) RAW image files (bin/cue, iso/cue).

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
#%%patch0 -p 1 -b .libs
./autogen.sh


%build
%configure --disable-static --enable-wide-character-type
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%check
make check


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%{_bindir}/odrawinfo
%{_bindir}/odrawverify
%{_mandir}/man1/odrawinfo.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160522-1
- bump to 20160522

* Tue Jul 7 2015 Michal Ambroz <rebus AT seznam.cz> - 20150629-1
- 4dfb027dc608dc871bdf3a66c63193c24b189243 tagged as release 20150629

* Tue Jun 30 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-3
- fix for build - hmac - 4dfb027dc608dc871bdf3a66c63193c24b189243

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-2
- fix for byacc

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-1
- Initial build for Fedora

