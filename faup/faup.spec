Name:           faup
Summary:        Library and tool for URL parsing and normalizing to tokens
URL:            https://github.com/stricaud/faup
#               https://github.com/stricaud/faup/releases
License:        WTFPL
Group:          System Environment/Libraries
Version:        1.5

%global         gituser         stricaud
%global         gitname         faup
%global         gitdate         20190701
%global         commit          a5268839130d76ebe2a26e9d7ff497e7d81dc142
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  cmake
BuildRequires:  lua-devel
BuildRequires:  gcc-c++
BuildRequires:  make


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
export CFLAGS="%{optflags}"
[ -d build ] || mkdir build
cd build
%cmake -DLOCALSTATEDIR:PATH=%{_var} -DBUILD_WITH_LDAP=ON ..


%build
export CFLAGS="%{optflags}"
make build

%install
cd build
%make_install

# Remove static libraries
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Remove static libraries
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md LICENSE 
%{_bindir}/faup
%{_mandir}/man1/faup.1*
%{_libdir}/libfaupl.so.*
%{_datadir}/faup


%files devel
%defattr(-,root,root,-)
%{_includedir}/faup/
%{_libdir}/libfaupl.so


%changelog
* Fri Aug 02 2019 Michal Ambroz <rebus at, seznam.cz> - 1.5-1
- initial spec

