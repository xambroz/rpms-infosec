Name:           libemu
Version:        0.2.0
Summary:        The x86 shell-code detection and emulation
Group:          Applications/System

# libemu package licensed with GPLv2+
# libdasm.c libdasm.h licensed as public domain do whatever - being bundled with libemu since at least 2006 effectively GPLv2+
License:        GPLv2+
URL:            https://github.com/DinoTools/libemu/
# Other information sources:
#    Original nepenthes site - is gone, but available from web archive
#               http://libemu.mwcollect.org -> https://web.archive.org/web/20090122230505/http://libemu.mwcollect.org
#               https://sourceforge.net/projects/nepenthes/files/libemu%20development/
#               http://downloads.sourceforge.net/project/nepenthes/libemu%20development/libemu/libemu-0.2.0.tar.gz
#    Original dionaea site - is gone, but available from web archive
#               http://libemu.carnivore.it/ -> https://web.archive.org/web/20150812195102/http://libemu.carnivore.it/
#    Debian libemu package
#               https://packages.debian.org/search?searchon=sourcenames&keywords=libemu
#               https://packages.debian.org/sid/libemu-dev
#    Git repositories/forks
#               https://github.com/DinoTools/libemu/
#               https://github.com/tpltnt/libemu
#               https://github.com/buffer/libemu
#               https://github.com/buffer/pylibemu
#               https://github.com/buffer/phoneyc
#               https://github.com/dzzie/SCDBG
#        Win32 Libemu shim for using Unicorn Engine as a backend
#               https://github.com/fireeye/unicorn-libemu-shim
#               https://github.com/gento/libemu
#    Paul Baecher
#               https://baecher.github.io/
#    Markus Koetter
#		https://www2.honeynet.org/2009/06/05/iteolih-is-this-worth-your-time/
#		https://www.honeynet.org/node/485
#    Articles
#               http://resources.infosecinstitute.com/shellcode-detection-emulation-libemu/
#               https://www.aldeid.com/wiki/Dionaea/Installation

# Version in Debian - 09bbeb583be41b96b9e8a5876a18ac698a77abfa
# http://http.debian.net/debian/pool/main/libe/libemu/libemu_0.2.0+git20120122.orig.tar.gz
#global         gitdate         20120122
#global         commit          09bbeb583be41b96b9e8a5876a18ac698a77abfa

%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 7 )
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif


%global         gituser         DinoTools
%global         gitname         libemu
# Current version
%global         gitdate         20130410
%global         commit          ab48695b7113db692982a1839e3d6eb9e73e90a9
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Build source is tarball release=1 or git commit=0
%global         build_release    0

%if 0%{?build_release}  > 0
# Build from the targball release
Release:        5%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

%else
# Build from the git commit snapshot
Release:        0.5.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release


# Patches 1-5 taken from the Debian package - author David Martínez Moreno <ender@debian.org>
# and is licensed under the GPL version 2 or later

# Remove the hardcoded rpath from python binding
# https://github.com/DinoTools/libemu/issues/3
# https://github.com/DinoTools/libemu/pull/2
Patch1:         libemu-01_no_rpath_python.patch

# Allow installing to DESTDIR for the python binding
# https://github.com/DinoTools/libemu/issues/5
# https://github.com/DinoTools/libemu/pull/4
Patch2:         libemu-02_python_install_dir.patch


# Remove hardcoded rpath from configure.ac
# https://github.com/DinoTools/libemu/issues/6
# https://github.com/DinoTools/libemu/pull/7
Patch3:         libemu-03_remove_rpath_and_fix_ldflags.patch


# Comment out unused typedefs
# https://github.com/DinoTools/libemu/issues/8
# https://github.com/DinoTools/libemu/pull/9
Patch5:         libemu-05_unused_local_typedefs.patch

# Debian patches not relevant for Fedora -
# - recognizing GNU as OS not needed for Fedora build
# Patch4:       libemu-04_recognize_gnu.patch

# Fix warnings during the autreconf
# https://github.com/DinoTools/libemu/issues/10
# https://github.com/DinoTools/libemu/pull/11
Patch6:         libemu-06_autoreconf.patch

# Fix memory leak in emu_memory_free
# https://github.com/buffer/libemu/commit/9256d8dc460b15a1c05d19b2fd277939602145e1.patch
Patch7:         libemu-07_emu_memory_free.patch

# Add configure option for pkgconfigdir
# https://github.com/buffer/libemu/commit/48466d2d0d641c8b2067a366600cd2b6a52ef01b
Patch8:         libemu-08_pkgconfigdir.patch

# fix potential name collision of PAGE_SIZE in emu_memory.c by renaming to EMU_PAGE_SIZE
# https://github.com/DinoTools/libemu/issues/14
# https://github.com/DinoTools/libemu/pull/15
Patch9:         libemu-09_pagesize.patch

# fix single byte buffers causing floating point exception
# https://github.com/bwall/libemu/commit/d424e097b2a08fd0b837756192bc257344782009.patch
# https://github.com/buffer/libemu/pull/1
Patch10:        libemu-10_singlebyte.patch

# removed tautological condition
# https://github.com/tpltnt/libemu/commits/master
# https://github.com/tpltnt/libemu/commit/910f39fa0d9a18fc07ba2541c3757cc616d0ffeb.patch
Patch11:        libemu-11_tautology.patch

# fix potential null pointer dereferences
# https://github.com/DinoTools/libemu/issues/20
# https://github.com/DinoTools/libemu/pull/19
# From:
# https://github.com/tpltnt/libemu/commits/master
# https://github.com/tpltnt/libemu/commit/6c1a774e6d342912d646935432b426b4da6d3c93.patch
# https://github.com/tpltnt/libemu/commit/c3fb84dc99b01805c7f01d52527339dd58ceabbe.patch
# https://github.com/tpltnt/libemu/commit/5d88320054b642c6388a6af05cf397895b82e2d5.patch
# https://github.com/tpltnt/libemu/commit/b8c35bf2c3704fb8acc0501abc33be0a4d146c1c.patch
# https://github.com/tpltnt/libemu/commit/d41a3737ab62e9aaaabb791f8959c7cbd9d77a7a.patch
# https://github.com/tpltnt/libemu/commit/23117b2b9cff6346feb944611c05cc723820a3ba.patch
# https://github.com/tpltnt/libemu/commit/0267a6f003b5e08069d8e266826865f42f939025.patch
# https://github.com/tpltnt/libemu/commit/d15e16cee40898dd035537a47b5e97c404387b83.patch
# https://github.com/tpltnt/libemu/commit/56ff307ea36b938a11151bb22432b1ab561d71ea.patch
# https://github.com/tpltnt/libemu/commit/bdb14b443ff1b5294ecbc1ab7ba9b430b7ab2d50.patch
Patch12:        libemu-12_nullpointer.patch



BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

# libemu contains modified version of libdasm 1.4
# libdasm licensed as public domain do whatever
Provides:       bundled(libdasm) = 1.4


%description
The libemu is a small library written in C offering basic x86 emulation and
shell-code detection using GetPC heuristics. Intended use is within network
intrusion/prevention detection and honeypots.



%package        devel
# ======================= devel package ==============================
Summary:        Development files for the libemu x86 emulator
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%package        -n python2-libemu
# ======================= python2-libemu =============================
Summary:        Python2 binding to the libemu x86 emulator
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}


%description    -n python2-libemu
Python2 binding to the libemu x86 emulator.


%if 0%{?with_python3}
%package        -n python3-libemu
# ======================= python3-libemu =============================
Summary:        Python3 binding to the libemu x86 emulator
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description    -n python3-libemu
Python3 binding to the libemu x86 emulator.

%endif #with_python3



%prep
# ======================= prep =======================================
%if 0%{?build_release} > 0
# Build from tarball release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif



%build
# ======================= build ======================================
autoreconf -v -i
%configure --enable-python-bindings

#Build also for python3
cp -r bindings/python bindings/python3

make %{?_smp_mflags}

# Just to be sure rebuild with the Fedora hardening options
pushd bindings/python
%py2_build
popd

%if 0%{?with_python3}
# Ignore the python3 build at this point
pushd bindings/python3
%py3_build || touch python3_build_failed
popd
%endif #with_python3

%install
# ======================= install ====================================
%make_install pkgconfigdir=%{_libdir}/pkgconfig

# just to be on the safe side
pushd bindings/python
%py2_install
popd

%if 0%{?with_python3}
# Ignore the python3 build at this point
pushd bindings/python3
mkdir -p %{buildroot}/%{python3_sitearch}
%py3_install || touch %{buildroot}/%{python3_sitearch}/python3_install_failed
[ -f python3_build_failed ] && touch %{buildroot}/%{python3_sitearch}/python3_build_failed
popd
%endif

# No static building allowed for Fedora
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'



%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig

%files
# ======================= files ======================================
%doc AUTHORS CHANGES README
%{_bindir}/sctest
%{_bindir}/scprofiler
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*


%files -n python2-libemu
%{python2_sitearch}/*

%if 0%{?with_python3}
%files -n python3-libemu
%{python3_sitearch}/*
%endif #with_python3

%changelog
* Fri Mar 23 2018 Michal Ambroz <rebus at, seznam.cz> - 0.2.0-0.5.20130410gitab48695
- added missing dependency to python3-devel
- use the python%{python3_pkgversion}-devel/setuptools to enable EPEL7 build


* Thu Mar 22 2018 Michal Ambroz <rebus at, seznam.cz> - 0.2.0-0.4.20130410gitab48695
- spec clean-up
- prepare for the python3 support
- include patches from buffer github repository

* Sun Mar 04 2018 Michal Ambroz <rebus at, seznam.cz> - 0.2.0-0.1.20130410gitab48695
- build for Fedora 27

