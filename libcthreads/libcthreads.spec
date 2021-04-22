%global         gituser         libyal
%global         gitname         libcthreads
#%global        commit          f73a55f845007fa43c9c608c617e74c2082578a
#release 20160402
#%global        commit          b0cb6461776168f76ad35104d551d51adf152514
#20160602
%global         commit          f73a55f845007fa43c9c608c617e74c2082578a9
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libcthreads
Version:        20160426
Release:        1%{?dist}
Summary:        Libyal library for cross-platform C threads functions

Group:          System Environment/Libraries
License:        LGPLv3+
#URL:           https://github.com/libyal/libcthreads
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

%description
Library for cross-platform C threads functions.

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
make %{?_smp_mflags}


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
* Mon Jun 20 2016 Michal Ambroz <rebus AT seznam.cz> - 20160402-1
- bump to 20160402

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150407-1
- Initial build for Fedora
