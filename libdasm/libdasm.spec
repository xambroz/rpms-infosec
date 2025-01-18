Name:           libdasm
Version:        1.6
Summary:        Simple x86 disassembly library
%global         baserelease     19
%if 0%{?rhel}
# Group needed for EPEL
Group:          Applications/System
%endif


%global         common_description %{expand:
libdasm is a C-library that tries to provide simple and convenient
way to disassemble Intel x86 raw op-code bytes (machine code).
It can parse and print out op-codes in AT&T and Intel syntax.

The op-codes are based on IA-32 Intel Architecture Software Developers
Manual Volume 2: Instruction Set Reference, order number 243667,
year 2004.  Non-Intel instructions are not supported at the moment (also,
non-Intel but Intel-compatible CPU extensions, like AMD 3DNow! are
not supported).}


# Do not build with python3 by default for now
# Module can be compiled but it doesn't load properly to python3
%bcond_with  python3

%if ( 0%{?fedora} && 0%{?fedora} <= 31 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
# enable python2 for older releases
%bcond_without  python2
%else
# disable python2 for newer Fedora releases
%bcond_with     python2
%endif


# TODO - add ruby subpackage

# Current code being maintained on github by Joshua Pereyda
# version 1.6 was released with the BSD license
# Original author Jarkko Turkulainen <jt () klake org> put the code into public domain
# http://www.klake.org/~jt/misc/libdasm-1.4.tar.gz -> https://web.archive.org/web/20060718012748/http://www.klake.org/~jt/misc/libdasm-1.4.tar.gz
# http://www.klake.org/~jt/misc/libdasm-1.5.tar.gz -> https://web.archive.org/web/20120119123445/http://www.klake.org/~jt/misc/libdasm-1.5.tar.gz
# https://labsblog.f-secure.com/author/turkja/
# http://en.gravatar.com/turkja
# There was another fork on https://code.google.com/archive/p/libdasm/ by Ange Albertini
License:        BSD
URL:            https://github.com/jtpereyda/libdasm


# Other resources:
#               https://github.com/jtpereyda/libdasm
#               https://code.google.com/archive/p/libdasm/
#               https://github.com/axcheron/libdasm
#               https://github.com/axcheron/pydasm
#               https://github.com/nkzxw/libdasm
#               https://github.com/whb224117/libdasm
#               https://github.com/Starwarsfan2099/PyDasm-3.5
#               https://github.com/gdbinit/pydbg64/tree/master/libdasm-beta
#               https://github.com/gunmetalbackupgooglecode/libdasm

# Fix up the Makefiles to remove upstream compilation flags, install to destdir
# https://github.com/jtpereyda/libdasm/issues/6
# https://github.com/jtpereyda/libdasm/pull/5
# Patch0:       libdasm-00_destdir.patch

# Do not ask for unneeded write access in "das"
# https://github.com/jtpereyda/libdasm/pull/9
# https://github.com/jtpereyda/libdasm/commit/3af940dc771132e3cafe275bb6eeaba2b55937cc.patch
Patch1:         libdasm-01_readonly.patch

# Build the oython only explicitly
Patch2:         libdasm-02_explicit_python.patch

# Make das.py example compatible with both pytho2 and python3
Patch3:         libdasm-03_das_futurize.patch

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif


# we don't want to provide private python extension libs
# TODO: this causes warning "Deprecated external dependency generator is used!"
%{?filter_setup:
%filter_provides_in %{python2_sitearch}/.*\.so$
%filter_setup
}


%global         gituser         jtpereyda
%global         gitname         libdasm
# Current version
%global         gitdate         20180330
%global         commit          b9233ccf35dce894ac0188e5830fa4346873a1f6
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Build source is tarball release=1 or git commit=0
# to build from git snapshot try rpmbuild libdasm-*.src.rpm --without releasetag
%bcond_without  releasetag

%if %{with releasetag}
# Build from the targball release
Release:        %aurorelease
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%else
# Build from the git commit snapshot
# Release is not starting with 0 as usual, because the next release will be 1.6
Release:        %aurorelease
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif



BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel


%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%description
%{common_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%{common_description}


%if %{with python2}
# We use here the upstream name for the python module - pydasm
%package        -n python2-pydasm
Summary:        Python2 module for disassembling x86 machine code
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}
%{?python_provide:%python_provide python2-pydasm}


%description    -n python2-pydasm
The python2 pydasm module for disassembling x86 machine code.
It is a python wrapper for libdasm.
%{common_description}

%endif



%if %{with python3}
%package        -n python%{python3_pkgversion}-pydasm
Summary:        Python module for disassembling x86 machine code
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-pydasm}


%description    -n python%{python3_pkgversion}-pydasm
The python%{python3_pkgversion} pydasm module for disassembling x86 machine code.
It is a python wrapper for libdasm.
%{common_description}

%endif




%prep
# ======================= prep =======================================
%if %{with releasetag}
# Build from tarball release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif


# Remove prebuilt Win32 DLLs from the tarball:
rm -rf bin

# Build explicitly for python2
sed -i -e 's|python |python2 |g;' pydasm/Makefile

# Do not build the python subpackage by default but build explicitly
sed -i -e 's|make -C pydasm|# make -C pydasm|' Makefile



%build
%set_build_flags
%make_build CFLAGS="$CFLAGS -fPIC" PREFIX=/usr LIBDIR=%{_libdir} BINDIR=%{_bindir}

%if %{with python2}
pushd pydasm
%py2_build
popd
%endif


%if %{with python3}
pushd pydasm
%py3_build
popd
%endif



%install
%make_install DESTDIR=%{buildroot} PREFIX=/usr LIBDIR=%{_libdir} BINDIR=%{_bindir}

#remove the das.py example installed by default
rm -f "%{buildroot}%{_bindir}/das.py"

%if %{with python2}
# do the python2 install explicitly
#Use explicitly versioned python2 shabang
sed -i -e 's|^#!/usr/bin/.*|#!/usr/bin/python2|;' pydasm/das.py
pushd pydasm
%py2_install
install -m 755 -p -D das.py "%{buildroot}%{_bindir}/das-%{python2_version}"
pushd %{buildroot}%{_bindir}
ln -s "das-%{python2_version}" "das-2"
popd
popd
%endif


%if %{with python3}
# do the python3 install explicitly
#Use explicitly versioned python3 shabang
sed -i -e 's|^#!/usr/bin/.*|#!/usr/bin/python3|;' pydasm/das.py
pushd pydasm
%py3_install
install -m 755 -p -D das.py "%{buildroot}%{_bindir}/das-%{python3_version}"
pushd %{buildroot}%{_bindir}
ln -s "das-%{python3_version}" "das-3"
popd
popd
%endif


pushd %{buildroot}%{_bindir}
%if %{with python3}
    # Link to python3 as default on fedora 31+ and rhel8+ and everything else
    ln -s "das-3" "das.py"
%else
%if %{with python2}
    # Link to python2 as default on fedora up to 30 and rhel up to 7 if python3 package not enabled
    ln -s "das-2" "das.py"
%endif
%endif
popd

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%doc HISTORY.txt LIB.txt README.txt TODO.txt
%{_libdir}/*.so.*
%{_bindir}/das

%files devel
%{_includedir}/*
%{_libdir}/*.so

%if %{with python2}
%files -n python2-pydasm
%{python2_sitearch}/*
%{_bindir}/das-%{python2_version}
%{_bindir}/das-2
%if ! %{with python3}
%{_bindir}/das.py
%endif
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-pydasm
%{python3_sitearch}/pydasm*
%{_bindir}/das-%{python3_version}
%{_bindir}/das-3
%{_bindir}/das.py
%endif


%changelog
%autochangelog
