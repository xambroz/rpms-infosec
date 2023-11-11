Name:       r2ghidra
Version:    5.8.8
Release:    1%{?dist}
Summary:    Integration of the Ghidra decompiler for radare2

%global radare2_ver 5.8.8

%bcond_with iaito

%global ghidra_commit          078cef887b8c78fd0801c313c6a268e0846a2b19
%global ghidra_shortcommit     %(c=%{ghidra_commit}; echo ${c:0:7})
%global ghidra_checkout_date   20231024
%global ghidra_snapshot        %{ghidra_checkout_date}git%{ghidra_shortcommit}

%global pugixml_commit          6909df2478f7eb092e8e5b5cda097616b2595cc6
%global pugixml_shortcommit     %(c=%{pugixml_commit}; echo ${c:0:7})
%global pugixml_checkout_date   20231022
%global pugixml_snapshot        %{pugixml_checkout_date}git%{pugixml_shortcommit}



License:    LGPL-3.0-or-later
URL:        https://github.com/radareorg/r2ghidra
# Source0:    https://github.com/radareorg/r2ghidra/archive/v%%{version}/r2ghidra-%%{version}.tar.gz
Source0:    https://github.com/radareorg/r2ghidra/archive/refs/tags/%{version}.tar.gz#/r2ghidra-%{version}.tar.gz
Source1:    https://github.com/radareorg/ghidra-native/archive/%{ghidra_commit}/ghidra-native-%{ghidra_snapshot}.tar.gz
Source2:    https://github.com/zeux/pugixml/archive/%{pugixml_commit}/pugixml-%{pugixml_snapshot}.tar.gz


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pugixml-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  radare2-devel >= %{radare2_ver}

%if %{with iaito}
# iaito is now not having devel subpackage
BuildRequires:  iaito-devel
%endif

Requires: radare2

Provides:       bundled(pugixml) = 1.14


%description
r2ghidra is an integration of the Ghidra decompiler for radare2. It
is solely based on the decompiler part of Ghidra, which is written
entirely in C++, so Ghidra itself is not required at all and the plugin
can be built self-contained.


%if %{with iaito}
%package iaito
Summary:        r2ghidra plugin for iaito
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       r2cutter

%description r2cutter
Plugin to use r2ghidra from Cutter UI.

%endif

%prep
%autosetup -b0
%autosetup -N -b1
%autosetup -N -b2

ln -s ../ghidra-native-%{ghidra_commit} ghidra-native

rmdir third-party/pugixml
ln -s ../../pugixml-%{pugixml_commit} third-party/pugixml


%build
%configure
%make_build


%install
%make_install

mkdir -p %{buildroot}%{_libdir}/radare2/%{radare2_ver}
mv \
        %{buildroot}%{_datadir}/%{name}/core_ghidra.so \
        %{buildroot}%{_libdir}/radare2/%{radare2_ver}/


%files
%{_libdir}/radare2/%{radare2_ver}/core_ghidra.so
%{_datadir}/%{name}/r2ghidra_sleigh

%if %{with iaito}
%files iaito
%{_libdir}/r2cutter/plugins/libr2ghidra_iaito.so
%endif

%changelog
* Mon Nov 06 2023 Michal Ambroz <rebus _AT seznam.cz> - 5.8.8-1
- Update to 5.8.8

* Tue Mar 23 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.1.0-1
- Update to 5.1.0

* Sat Nov 28 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.1-1
- Update to 4.5.1

* Fri Aug 07 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.0-1
- Update to 4.5.0

* Sat Apr 18 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.4.0-1
- Initial packaging
