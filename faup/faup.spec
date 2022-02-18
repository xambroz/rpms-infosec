Name:           faup
Summary:        Library and tool for URL parsing and normalizing to tokens
URL:            https://github.com/stricaud/faup
#               https://github.com/stricaud/faup/releases
License:        WTFPL
Group:          System Environment/Libraries
Version:        1.6
%global         rel             1



%global         gituser         stricaud
%global         gitname         faup
%global         gitdate         20210621
%global         commit          8e81b170d205485de587c2f4bca54e5dcdf678a4
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# by default it builds from the git snapshot version of faup
# to build from release use rpmbuild --with=releasetag
%bcond_with     releasetag

%if %{with releasetag}
Release:        %{rel}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        0.%{rel}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.zip
%endif



BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(lua)

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  cmake
BuildRequires:  cmake-rpm-macros
%else
BuildRequires:  cmake3
%endif



%description
Faup stands for Finally An Url Parser and is a library and command line tool to parse URLs and normalize fields with two constraints:
Work with real-life urls (resilient to badly formated ones)
Be fast: no allocation for string parsing and read characters only once


%package devel
Summary:        Development files for faup library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development libraries and headers for use with %{name}.


%prep
%if %{with releasetag}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}
%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif


%build
cd build
%cmake3 ..
%cmake3_build


%install
cd build
%cmake3_install

# Remove static libraries
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Remove static libraries
find %{buildroot} -name '*.a' -exec rm -f {} ';'


%if 0%{?rhel} && 0%{?rhel} <= 7
%ldconfig_scriptlets
%endif


%files
%license LICENSE
%doc README.md
%{_bindir}/faup
%{_mandir}/man1/faup.1*
%{_libdir}/libfaupl.so.*
%{_datadir}/faup


%files devel
%{_includedir}/faup/
%{_libdir}/libfaupl.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Feb 18 2022 Michal Ambroz <rebus at, seznam.cz> - 1.6-0.1
- bump to current git snapshot

* Sun May 16 2021 Michal Ambroz <rebus at, seznam.cz> - 1.5-2
- modernize spec file

* Fri Aug 02 2019 Michal Ambroz <rebus at, seznam.cz> - 1.5-1
- initial spec

