#
# spec file for package procmon
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           procmon
Version:        1.0.1
Release:        4.3
Summary:        Trace the syscall activity on the system
License:        MIT
Group:          System/Monitoring
URL:            https://github.com/microsoft/ProcMon-for-Linux/
Source0:        https://github.com/Sysinternals/ProcMon-for-Linux/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# PATCH-FIX-OPENSUSE procmon-use_system_libs.patch
Patch0:         procmon-use_system_libs.patch
# PATCH-FIX-UPSTREAM procmon-no_return_in_nonvoid.patch -- aloisio@gmx.com
Patch1:         procmon-no_return_in_nonvoid.patch
# PATCH-FIX-OPENSUSE procmon-add_missing_include.patch -- aloisio@gmx.com
Patch2:         procmon-add_missing_include.patch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  (pkgconfig(catch2) with pkgconfig(catch2) < 3)
BuildRequires:  pkgconfig(libbcc)
BuildRequires:  pkgconfig(libedit)
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
Requires:       kernel-devel
# on account of BPF.h
ExcludeArch:    %arm %ix86

%description
Process Monitor (Procmon) is a Linux reimagining of the classic Procmon
tool from the Sysinternals suite of tools for Windows. Procmon provides
a convenient and efficient way for Linux developers to trace the syscall
activity on the system.

%prep
%setup -q -n ProcMon-for-Linux-%{version}
%autopatch -p1

%build
%cmake
%cmake_build

%install
%cmake_install
install -Dm0644 procmon.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check
%ctest

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Tue Aug 15 2023 Michal Ambroz <rebus _@ seznam.cz>
- man page in Fedora ends with .gz

* Tue Mar 28 2023 Luigi Baldoni <aloisio@gmx.com>
- Refresh procmon-add_missing_include.patch

* Mon Oct 31 2022 Dominique Leuenberger <dimstar@opensuse.org>
- Limit to catch < 3: not compatible yet to Catch 3.

* Mon Jun  6 2022 Luigi Baldoni <aloisio@gmx.com>
- Add procmon-add_missing_include.patch to fix Factory build

* Thu May  6 2021 Luigi Baldoni <aloisio@gmx.com>
- Update to stable version 1.0.1
  * Small bug fixes
- Remove _service file
- Refresh procmon-use_system_libs.patch

* Sun Dec 27 2020 Luigi Baldoni <aloisio@gmx.com>
- Add procmon-no_return_in_nonvoid.patch
* Thu Dec 24 2020 Luigi Baldoni <aloisio@gmx.com>
- Update to version 1.0+git20201031.d65e7b2:
  * building against 0.15 (#54)
  * Spelling (#45)
  * Avoid telemetry data copy in ITelemetry (#50)
  * CancellableMessageQueue: push(value) using move same as push(vector)
  * Update required cmake version (#23)
  * fixed potential heap corruption and updated minimum specs for OS (#16)
  * patch for f1 segv (#9)
  * fixing cmake for rename of license file
  * documentation cleanup and polish
  * Initial commit of preview from AZDO

* Tue Jul 21 2020 andy great <andythe_great@pm.me>
- Initial package release.
