Name:           libsmraw
Version:        20240506
Release:        1%{?dist}
Summary:        Libyal library and tools to access the (split) RAW image format
Group:          System Environment/Libraries
License:        LGPL-3.0-or-later
URL:            https://github.com/libyal/libsmraw
VCS:            https://github.com/libyal/libsmraw
# Releases      https://github.com/libyal/libsmraw/releases


%global         gituser         libyal
%global         gitname         libsmraw
%global         gitdate         20240506
%global         commit          995b9e200ae8c836439f14741253143803fecb0c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         pythonopts      -enable-python2

%if 0%{?fedora}
%global         with_python3    1
%global         pythonopts      -enable-python2 --enable-python3
%endif


Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:         %{name}-libs.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  fuse-devel
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
BuildRequires:  libhmac-devel

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# if with_python3
%endif

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
# with_python3
%endif



%prep
%autosetup -n %{gitname}-%{commit}
#%%patch0 -p 1 -b .libs
./autogen.sh


%build
%if 0%{?with_python3}

# with_python3
%endif
%configure --disable-static --enable-wide-character-type \
	--enable-multi-threading-support --enable-verbose-output \
	%{pythonopts}
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
# with_python3
%endif


%changelog
* Mon Aug 01 2016 Michal Ambroz <rebus AT seznam.cz> - 20160524-1
- bump to 20160524

* Sat Jun 06 2015 Michal Ambroz <rebus AT seznam.cz> - 20150105-1
- Initial build for Fedora
