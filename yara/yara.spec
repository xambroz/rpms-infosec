Name:           yara
Version:        4.5.2
%global         baserelease 1
Summary:        Pattern matching Swiss knife for malware researchers
URL:            https://VirusTotal.github.io/yara/
VCS:            git:https://github.com/VirusTotal/yara/
#               https://github.com/VirusTotal/yara/releases

# yara package itself is licensed with BSD 3 clause license
# bison grammar parsers in libyara/* are licensed with  GPLv3+ license with exception from FSF alloving usage in larger work
# resulting binary package licensed as BSD
License:        BSD-3-Clause

%global         common_description %{expand:
YARA is a tool aimed at (but not limited to) helping malware researchers to
identify and classify malware samples. With YARA you can create descriptions
of malware families (or whatever you want to describe) based on textual or
binary patterns. Each description, a.k.a rule, consists of a set of strings
and a Boolean expression which determine its logic.}


%global         gituser         VirusTotal
%global         gitname         yara
# Commit of version 4.5.2
%global         gitdate         20240910
%global         commit          688268d83983a0d61bb68ef3d8dfd28102b7d1b4
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  release


# Build from git release version
%if %{with release}
Release:       %autorelease -b %{baserelease}
# Source0:     https://github.com/%%{gituser}/%%{gitname}/archive/v%%{upversion}.tar.gz#/%%{name}-%%{upversion}.tar.gz
Source0:       https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
# Build from git commit baseline
Release:       %autorelease -b %{baserelease} -s %{gitdate}git%{shortcommit}
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif

# Use default sphix theme to generate documentation rather than sphinx_rtd_theme
# to avoid static installation of font files on fedora >= 24
Patch1:         yara-docs-theme.patch


BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  m4
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  sharutils
BuildRequires:  file
BuildRequires:  sed
BuildRequires:  gawk
BuildRequires:  gzip
BuildRequires:  xz
BuildRequires:  pcre
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libtool
BuildRequires:  file-devel
BuildRequires:  jansson-devel >= 2.5
BuildRequires:  protobuf-c-devel
BuildRequires:  protobuf-compiler

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:  openssl11-devel
%else
BuildRequires:  openssl-devel
%endif

# html doc generation
BuildRequires:  /usr/bin/sphinx-build

%description
%{common_description}

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
This package contains documentation for %{name}.
%{common_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%{common_description}

%prep
%if %{with release}
    %autosetup -n %{gitname}-%{version} -p 1 -S git
%else
    %autosetup -n %{gitname}-%{commit} -p 1 -S git
%endif
autoreconf --force --install

%build

# Add missing protobuf definition on RHEL7, and also configure for the libcrypto11/openssl11 from EPEL
%if 0%{?rhel} && 0%{?rhel} == 7
export CFLAGS="%{optflags} -D PROTOBUF_C_FIELD_FLAG_ONEOF=4 $(pkg-config --cflags libcrypto11)"
export LDFLAGS="$LDFLAGS $(pkg-config --libs libcrypto11)"
%endif

# macro %%configure already does use CFLAGS="%%{optflags}" and yara build
# scripts configure/make already honors that CFLAGS
%configure --enable-magic --enable-cuckoo --enable-debug --enable-dotnet \
        --enable-macho --enable-dex --enable-pb-tests \
        --with-crypto \
        --htmldir=%{_datadir}/doc/%{name}/html
%make_build

# build the HTML documentation
pushd docs
make html
popd


%install
%make_install

# Remove static libraries
rm %{buildroot}%{_libdir}/lib%{name}.la
rm %{buildroot}%{_libdir}/lib%{name}.a

# Remove the rebuild-needed tag so it is not installed in doc pkg
rm -f %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo


%if 0%{?rhel} && 0%{?rhel} <= 7
%ldconfig_scriptlets
%endif

%check
# reenable the validation of SHA1 certificates in OPENSSL (RHEL9 disabled that by default)
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes
make check || (
    # print more verbose info in case the test(s) fail
    echo "===== ./test-suite.log"
    [ -f ./test-suite.log ] && cat ./test-suite.log
    # Build in COPR lacking the hwinfo.log
    echo "===== /proc/cpu"
    head -n 35 /proc/cpuinfo
    echo "===== /etc/os-release"
    cat /etc/os-release
    echo "===== uname -a"
    uname -a

%ifarch s390x
    # test-pe and test-dotnet fails for x390x at this point - ignored for rc1
    true
%else
    false
%endif
)

%files
%license COPYING
%doc AUTHORS CONTRIBUTORS README.md
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}c.1*


%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%files doc
%license COPYING
%doc docs/_build/html


%changelog
%autochangelog
