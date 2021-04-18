%global radare2_ver 5.1.1

%global ghidra_commit          44bacf3a13c52def99866ad2c9044044af393390
%global ghidra_shortcommit     %(c=%{ghidra_commit}; echo ${c:0:7})
%global ghidra_checkout_date   20210209
%global ghidra_snapshot        %{ghidra_checkout_date}git%{ghidra_shortcommit}

Name:       r2ghidra
Version:    5.1.0
Release:    1%{?dist}
Summary:    Integration of the Ghidra decompiler for radare2

License:    LGPLv3+
URL:        https://github.com/radareorg/r2ghidra
Source0:    https://github.com/radareorg/r2ghidra/archive/v%{version}/r2ghidra-%{version}.tar.gz
Source1:    https://github.com/radareorg/ghidra/archive/%{ghidra_commit}/ghidra-%{ghidra_snapshot}.tar.gz


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pugixml-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  radare2-devel >= %{radare2_ver}
BuildRequires:  r2cutter-devel

Requires: radare2


%description
r2ghidra is an integration of the Ghidra decompiler for radare2. It
is solely based on the decompiler part of Ghidra, which is written
entirely in C++, so Ghidra itself is not required at all and the plugin
can be built self-contained.


%package r2cutter
Summary:        r2ghidra plugin for r2cutter
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       r2cutter

%description r2cutter
Plugin to use r2ghidra from Cutter UI.


%prep
%autosetup -b0
%autosetup -N -b1

cd ghidra/
rmdir ghidra
ln -s ../../ghidra-%{ghidra_commit} ghidra


%build
mkdir build
cd build
%cmake \
        -DRADARE2_INSTALL_PLUGDIR=%{_datadir}/%{name} \
        -DCUTTER_INSTALL_PLUGDIR=%{_libdir}/r2cutter/plugins \
        -DCUTTER_SOURCE_DIR=%{_includedir}/r2cutter \
        -DBUILD_CUTTER_PLUGIN=ON \
        -DUSE_SYSTEM_PUGIXML=ON \
        ..
%cmake_build


%install
cd build
%cmake_install

mkdir -p %{buildroot}%{_libdir}/radare2/%{radare2_ver}
mv \
        %{buildroot}%{_datadir}/%{name}/core_ghidra.so \
        %{buildroot}%{_libdir}/radare2/%{radare2_ver}/


%files
%{_libdir}/radare2/%{radare2_ver}/core_ghidra.so
%{_datadir}/%{name}/r2ghidra_sleigh


%files r2cutter
%{_libdir}/r2cutter/plugins/libr2ghidra_cutter.so


%changelog
* Tue Mar 23 2021 Michal Ambroz <rebus _AT seznam.cz> - 5.1.0-1
- Update to 5.1.0

* Sat Nov 28 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.1-1
- Update to 4.5.1

* Fri Aug 07 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.0-1
- Update to 4.5.0

* Sat Apr 18 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.4.0-1
- Initial packaging
