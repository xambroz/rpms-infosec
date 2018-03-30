Name:           libdasm
Version:        1.5
Summary:        Simple x86 disassembly library

# Original author Jarkko Turkulainen <jt () klake org> put the code into public domain
# http://www.klake.org/~jt/misc/libdasm-1.4.tar.gz -> https://web.archive.org/web/20060718012748/http://www.klake.org/~jt/misc/libdasm-1.4.tar.gz
# http://www.klake.org/~jt/misc/libdasm-1.5.tar.gz -> https://web.archive.org/web/20120119123445/http://www.klake.org/~jt/misc/libdasm-1.5.tar.gz
# https://labsblog.f-secure.com/author/turkja/
# http://en.gravatar.com/turkja
# There was another fork on https://code.google.com/archive/p/libdasm/ by Ange Albertini
# Current code being maintained on github by Joshua Pereyda
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
Patch0:         %{name}-destdir.patch


%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif


# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}


%global         gituser         jtpereyda
%global         gitname         libdasm
# Current version
%global         gitdate         20180328
%global         commit          c315f8d9107566efc8ffde74270ed9031db65c28
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# Build source is tarball release=1 or git commit=0
%global         build_release    0

%if 0%{?build_release}  > 0
# Build from the targball release
Release:        6%{?dist}
#Source0:       http://libdasm.googlecode.com/files/%{name}-%{version}.tar.gz
#Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/%{name}/%{name}-%{version}.tar.gz

%else
# Build from the git commit snapshot
# Release is not starting with 0 as usual, because the next release will be 1.6
Release:        6.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release



BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

# ldconfig is provided by glibc
Requires(post): ldconfig
Requires(postun): ldconfig



%description
libdasm is a C-library that tries to provide simple and convenient
way to disassemble Intel x86 raw op-code bytes (machine code).
It can parse and print out op-codes in AT&T and Intel syntax.

The op-codes are based on IA-32 Intel Architecture Software Developer's
Manual Volume 2: Instruction Set Reference, order number 243667,
year 2004.  Non-Intel instructions are not supported at the moment (also,
non-Intel but Intel-compatible CPU extensions, like AMD 3DNow! are
not supported).


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


# We use here the upstream name for the python module - pydasm
%package        -n python2-pydasm
Summary:        Python module for disassembling x86 machine code
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}
%{?python_provide:%python_provide python2-pydasm}


%description    -n python2-pydasm
pydasm is a python module for disassembling x86 machine code.
It is a wrapper for libdasm.


%prep
# ======================= prep =======================================
%if 0%{?build_release} > 0
# Build from tarball release version
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif

#Use explicitly versioned python2 shabang
sed -i -e 's|#!/usr/bin/env.*|#!/usr/bin/python2|;' pydasm/das.py

# Remove prebuilt Win32 DLLs from the tarball:
rm -rf bin


%build
make %{?_smp_mflags} CFLAGS="%{optflags} -fPIC" PREFIX=/usr LIBDIR=%{_libdir} BINDIR=%{_bindir}


%install
make install DESTDIR=%{buildroot} PREFIX=/usr LIBDIR=%{_libdir} BINDIR=%{_bindir}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc HISTORY.txt LIB.txt README.txt TODO.txt
%{_libdir}/*.so.*
%{_bindir}/das

%files devel
%{_includedir}/*
%{_libdir}/*.so

%files -n python2-pydasm
%{python_sitearch}/*
%{_bindir}/das.py

%changelog
* Sun Mar 25 2018 Michal Ambroz <rebus at, seznam.cz> - 1.5-5.20151201gitc1afd03
- switch to github snapshot

* Sun Mar 04 2018 Michal Ambroz <rebus at, seznam.cz> - 1.5-4
- remove *.a files

* Sat Jul 14 2012 Michal Ambroz <rebus at, seznam.cz> - 1.5-3
- build for Fedora 17
- patch the makefiles to fix issue with soname, destdir

* Fri Jun  5 2009 David Malcolm <dmalcolm@redhat.com> - 1.5-2
- add python-devel to build requirements

* Fri May  8 2009 David Malcolm <dmalcolm@redhat.com> - 1.5-1
- initial packaging

