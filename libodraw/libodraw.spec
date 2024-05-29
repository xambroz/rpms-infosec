Name:           libodraw
Version:        20240505
Release:        1%{?dist}
Summary:        Libyal library to access to optical disc (split) RAW image files (bin/cue, iso/cue)
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libodraw
# Releases      https://github.com/libyal/libodraw/releases

%global         gituser         libyal
%global         gitname         libodraw
%global         gitdate         20240505
%global         commit          9460a81cb2d7ce7b9a221cab8f97885d001801fb
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


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
BuildRequires:  byacc
BuildRequires:  flex
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

%ldconfig_scriptlets


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
* Sat May 18 2024 Michal Ambroz <rebus _AT seznam.cz> - 20240505-1
- bump to 20240505

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

