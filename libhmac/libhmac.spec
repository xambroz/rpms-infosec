%global         gituser         libyal
%global         gitname         libhmac
%global         gitdate         20200104
%global         commit          5ca9bd3b4ec99c998b629600115e51a4d8bc0082

# Previous builds
#20160802
#%%global       commit          91b621fd9df85a0d20cb83a283ffc4e0171e6305
#20160731
#%%global       commit          a9762ac45955a37b9e9f6bd7d14c11ffadd9d9d8
#20150703
#%%global       commit          a95f04ccab1c8c23def380e19814855a7a6a05d0

%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libhmac
Version:        %{gitdate}
Release:        1%{?dist}
Summary:        Libyal library to support various Hash-based Message Authentication Codes (HMAC)

Group:          System Environment/Libraries
License:        LGPLv3+
#URL:           https://github.com/libyal/libhmac
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
BuildRequires:  libcstring-devel
BuildRequires:  libcerror-devel
BuildRequires:  libclocale-devel
BuildRequires:  libcnotify-devel
BuildRequires:  libcsplit-devel
BuildRequires:  libuna-devel
BuildRequires:  libcfile-devel
BuildRequires:  libcpath-devel
BuildRequires:  libcsystem-devel

%description
Library to support various Hash-based Message Authentication Codes (HMAC).

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
%setup -qn %{gitname}-%{commit}
%patch0 -p 1 -b .libs
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
%{_bindir}/hmacsum
%{_mandir}/man1/hmacsum.1.gz

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%changelog
* Fri Feb 18 2022 Michal Ambroz <rebus AT seznam.cz> - 20200104-1
- bump to 20200104

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160802-1
- bump to 20160802 - WINCRYPT

* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160731-1
- bump to 20160731

* Tue Jul 07 2015 Michal Ambroz <rebus AT seznam.cz> - 20150703-1
- bump to release 20150703

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150104-1
- Initial build for Fedora
