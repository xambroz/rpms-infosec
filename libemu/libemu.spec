%global         gituser         DinoTools
%global         gitname         libemu
%global         commit          ab48695b7113db692982a1839e3d6eb9e73e90a9
%global         commitdate      20130410
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           libemu
Version:        0.2.0
Release:        3.%{commitdate}git%{shortcommit}%{?dist}
Summary:        x86 shellcode detection and emulation

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/DinoTools/libemu/
#		http://libemu.carnivore.it/
#		http://libemu.mwcollect.org
#               https://www.aldeid.com/wiki/Dionaea/Installation
#               https://packages.debian.org/stretch/libemu-dev
# Source0:        http://http.debian.net/debian/pool/main/libe/libemu/libemu_0.2.0+git20120122.orig.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# Patches taken from the Debian package - author David Martínez Moreno <ender@debian.org>
# and is licensed under the GPL version 2 or later
Patch1:         %{name}-01_no_rpath_python.patch
Patch2:		%{name}-02_python_install_dir.patch
Patch3:		%{name}-03_remove_rpath_and_fix_ldflags.patch

# Debian patches not relevant for Fedora
# Patch4:		%{name}-04_recognize_gnu.patch

Patch5:		%{name}-05_unused_local_typedefs.patch

# Fix warnings during the autreconf
Patch6:		%{name}-autoreconf.patch


BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description
The libemu is a small library written in C offering basic x86 emulation and
shellcode detection using GetPC heuristics. Intended use is within network
intrusion/prevention detections and honeypots.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



# We use the upstream name for the Python module:
%package        -n libemu-python2
Summary:        Python interface to the libemu x86 emulator.
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    -n libemu-python2
Python interface to the libemu x86 emulator.


%prep
%setup -q -n %{name}-%{commit}

%patch1 -p 1 -b .rpath_python
%patch2 -p 1 -b .python_install_dir
%patch3 -p 1 -b .rpath
%patch5 -p 1 -b .typedefs
%patch6 -p 1 -b .autoreconf


%build
autoreconf -v -i
%configure --enable-python-bindings
make %{?_smp_mflags}


%install
%make_install pkgconfigdir=%{_libdir}/pkgconfig

# No static building
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS CHANGES README
%{_bindir}/sctest
%{_bindir}/scprofiler
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*


%files -n libemu-python2
%{python_sitearch}/*

%changelog
* Sun Mar 04 2018 Michal Ambroz <rebus at, seznam.cz> - 0.2.0-1
- build for Fedora 27

