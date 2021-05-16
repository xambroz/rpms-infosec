Name:           faup
Summary:        Library and tool for URL parsing and normalizing to tokens
URL:            https://github.com/stricaud/faup
#               https://github.com/stricaud/faup/releases
License:        WTFPL
Group:          System Environment/Libraries
Version:        1.5
Release:        1%{?dist}


%global         gituser         stricaud
%global         gitname         faup
%global         gitdate         20190701
%global         commit          a5268839130d76ebe2a26e9d7ff497e7d81dc142
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(lua)

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
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
%autosetup


%build
cd build
%cmake ..
%cmake_build


%install
cd build
%cmake_install

# Remove static libraries
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Remove static libraries
find %{buildroot} -name '*.a' -exec rm -f {} ';'


%ldconfig_scriptlets


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


%changelog
* Sun May 16 2021 Michal Ambroz <rebus at, seznam.cz> - 1.5-2
- modernize spec file

* Fri Aug 02 2019 Michal Ambroz <rebus at, seznam.cz> - 1.5-1
- initial spec

