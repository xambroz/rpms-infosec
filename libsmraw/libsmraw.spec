%global         gituser         libyal
%global         gitname         libsmraw
#20150105
%global         commit          a54ab68e1d63a7bc3c91b400311fd9c9e4089e94
#20160524
%global         commit          a9c8140455abcd7a77a1f4b7fb6e13d42ac49491
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         pythonopts      -enable-python2

%if 0%{?fedora}
%global         with_python3    1
%global         pythonopts      -enable-python2 --enable-python3
%endif


Name:           libsmraw
Version:        20160524
Release:        1%{?dist}
Summary:        Libyal library and tools to access the (split) RAW image format

Group:          System Environment/Libraries
License:        LGPLv3+
#URL:           https://github.com/libyal/libsmraw
URL:            https://github.com/%{gituser}/%{gitname}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  fuse-devel
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
BuildRequires:  libfcache-devel
BuildRequires:  libfdata-devel
BuildRequires:  libfvalue-devel
BuildRequires:  libcsystem-devel
BuildRequires:  libhmac-devel

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%description
Library and tools to access the (split) RAW image format.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%package python2
Summary:        Python2 extension that gives access to %{name} library
Group:          Development/Libraries
%{?python_provide:%python_provide python2-%{name}}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description python2
This is a Python module that gives access to %{name} library
from Python scripts.



%if 0%{?with_python3}
%package python3
Summary:        Python3 extension that gives access to %{name} library
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

Requires:       %{name}%{?_isa} = %{version}-%{release}


%description python3
This is a Python3 module that gives access to %{name} library
from Python scripts.
%endif # with_python3



%prep
%setup -qn %{gitname}-%{commit}
%patch0 -p 1 -b .libs
./autogen.sh


%build
%if 0%{?with_python3}

%endif # with_python3
%configure --disable-static --enable-wide-character-type \
	--enable-multi-threading-support --enable-verbose-output \
	%{pythonopts}
%make_build


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%{_bindir}/smrawmount
%{_bindir}/smrawverify
%{_mandir}/man1/smrawmount.1*

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%files python2
%{python2_sitearch}/pysmraw*

%if 0%{?with_python3}
%files python3
%{python3_sitearch}/pysmraw*
%endif # with_python3


%changelog
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160524-1
- bump to 20160524

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-1
- Initial build for Fedora
