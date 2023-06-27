Name:           keystone
Version:        0.9.2
Release:        1%{?dist}
Summary:        A lightweight multi-platform, multi-architecture assembler framework

%global         gituser         keystone-engine
%global         gitname         keystone
# 0.9.2 release
%global         commit          dc7932ef2b2c4a793836caec6ecab485005139d6
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

License:        GPL-2.0-only
URL:            http://www.keystone-engine.org/
VCS:            https://github.com/keystone-engine/keystone/
#               https://github.com/keystone-engine/keystone/releases
# Source0:      https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Test suite binary samples to be used for disassembly
# Source1:

# Fedora 29 makes python executable separate from python2 and python3. This patch makes
# it possible to specify PYTHON2 and PYTHON3 binary to be explicit that by "python" we mean "python2"
# Patch0:         keystone-python.patch

# Upstream patch which fixes libkeystone.pc.
# See: https://github.com/aquynh/keystone/issues/1339
# Patch1:         0001-Fix-include-path-in-pkg-config-for-Makefile-too-1339.patch

%global         common_desc %{expand:
Keystone is a lightweight multi-platform, multi-architecture assembler framework.
Highlight features:
- Multi-architecture, with support for Arm, Arm64 (AArch64/Armv8), Ethereum Virtual Machine, Hexagon, Mips, PowerPC, Sparc, SystemZ, & X86 (include 16/32/64bit).
- Clean/simple/lightweight/intuitive architecture-neutral API.
- Implemented in C/C++ languages, with bindings for Java, Masm, Visual Basic, C#, PowerShell, Perl, Python, NodeJS, Ruby, Go, Rust, Haskell & OCaml available.
- Native support for Windows & *nix (with Mac OSX, Linux, *BSD & Solaris confirmed).
- Thread-safe by design.
- Open source.
Keystone is based on LLVM, but it goes much further with a lot more to offer.
}

# Build with python3 package by default
%bcond_without  python3

# Build without python2 package for newer releases f32+ and rhel8+
%if (0%{?fedora} && 0%{?fedora} >= 32 ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
%bcond_with     python2
%else
%bcond_without  python2
%endif


%global srcname distribute

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  git

%ifarch %{java_arches}
BuildRequires:  jna
BuildRequires:  java-devel
%endif

%if %{with python2}
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%global _hardened_build 1


%description
%{common_desc}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{common_desc}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%if %{with python2}
%package        -n python2-keystone
%{?python_provide:%python_provide python2-keystone}
# Remove before F30
Provides:       %{name}-python = %{version}-%{release}
Provides:       %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python < %{version}-%{release}
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    -n python2-keystone
%{common_desc}
The python2-keystone package contains python bindings for %{name}.
# with_python2
%endif



%if %{with python3}
%package	-n python%{python3_pkgversion}-keystone
%{?python_provide:%python_provide python%{python3_pkgversion}-keystone}
Provides:       %{name}-python%{python3_pkgversion} = %{version}-%{release}
Provides:       %{name}-python%{python3_pkgversion}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python%{python3_pkgversion} < %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Python3 bindings for %{name}


%description    -n python%{python3_pkgversion}-keystone
%{common_desc}
The python%{python3_pkgversion}-keystone package contains python3 bindings for %{name}.
#with python3
%endif


%ifarch %{java_arches}
%package        java
Summary:        Java bindings for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    java
%{common_desc}
The %{name}-java package contains java bindings for %{name}.
%endif


%prep
# autosetup -n %%{gitname}-%%{commit} -S git
%autosetup -n %{gitname}-%{version} -S git



%build
mkdir build
cd build
export CFLAGS="%{optflags}"
../make-share.sh debug

# Fix pkgconfig file
sed -i 's;%{buildroot};;' keystone.pc
grep -v archive keystone.pc > keystone.pc.tmp
mv keystone.pc.tmp keystone.pc


# build python bindings
cd ..
pushd bindings/python

%if %{with python2}
%py2_build
%endif

%if %{with python3}
%py3_build
%endif
popd

%ifarch %{java_arches}
# build java bindings needs some python
pushd bindings/java
%if %{with python3}
%make_build PYTHON2=%{__python3} PYTHON3=%{__python3} CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
%else
%make_build PYTHON2=%{__python2} PYTHON3=%{__python2} CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
%endif
popd
%endif



%install
DESTDIR=%{buildroot} PREFIX="%{_prefix}" LIBDIRARCH=%{_lib} \
INCDIR="%{_includedir}" make install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# install python bindings
pushd bindings/python
%if %{with python2}
%py2_install
%endif

%if %{with python3}
%py3_install
%endif
popd

%ifarch %{java_arches}
# install java bindings
install -D -p -m 0644 bindings/java/%{name}.jar  %{buildroot}/%{_javadir}/%{name}.jar
%endif


%check
ln -s libkeystone.so.4 libkeystone.so
make check LD_LIBRARY_PATH="`pwd`"


%ldconfig_scriptlets



%files
%license LICENSE.TXT LICENSE_LLVM.TXT
%doc CREDITS.TXT ChangeLog README.md SPONSORS.TXT
%{_libdir}/*.so.*
%{_bindir}/cstool



%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*



%if %{with python2}
%files -n python2-keystone
%{python2_sitelib}/*egg-info
%{python2_sitelib}/%{name}
%endif



%if %{with python3}
%files -n python%{python3_pkgversion}-keystone
%{python3_sitelib}/*egg-info
%{python3_sitelib}/%{name}
%endif


%ifarch %{java_arches}
%files java
%{_javadir}/
%endif

%changelog
* Fri Jan 06 2023 Michal Ambroz <rebus AT_ seznam.cz> - 0.9.2-1
- initial keystone package


