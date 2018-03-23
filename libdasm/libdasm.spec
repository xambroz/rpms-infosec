Name:           libdasm
Version:        1.5
Release:        4%{?dist}
Summary:        Simple x86 disassembly library

License:        Public Domain
URL:            https://code.google.com/archive/p/libdasm/
#Source0:       http://libdasm.googlecode.com/files/%{name}-%{version}.tar.gz
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/%{name}/%{name}-%{version}.tar.gz

# Fix up the Makefiles to remove upstream compilation flags, install to destdir:
Patch0:         %{name}-destdir.patch


%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}



BuildRequires:  pkgconfig
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

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
%autosetup -p 1 -n %{name}-%{version}

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
* Sun Mar 04 2018 Michal Ambroz <rebus at, seznam.cz> - 1.5-4
- remove *.a files

* Sat Jul 14 2012 Michal Ambroz <rebus at, seznam.cz> - 1.5-3
- build for Fedora 17
- patch the makefiles to fix issue with soname, destdir

* Fri Jun  5 2009 David Malcolm <dmalcolm@redhat.com> - 1.5-2
- add python-devel to build requirements

* Fri May  8 2009 David Malcolm <dmalcolm@redhat.com> - 1.5-1
- initial packaging

