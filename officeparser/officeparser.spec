Name:           officeparser
Release:        9%{?dist}
Summary:        Parse the format of OLE compound documents used by MS Office applications
License:        MIT
URL:            https://github.com/unixfreak0037/officeparser
VCS:            https://github.com/unixfreak0037/officeparser


%global         gituser         unixfreak0037
%global         gitname         officeparser
%global         gitdate         20230821
%global         commit          fce88741d3f78d5588bb214b824c2d51232287a5
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Version:        0.%{gitdate}


Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# Patch from Lumir Balhar to introduce the python3 compatibility wit the office parser
# https://github.com/unixfreak0037/officeparser/pull/19
Patch1:         https://patch-diff.githubusercontent.com/raw/unixfreak0037/officeparser/pull/19.patch#/officeparser-01_python3_compatibiity.patch

# Patch also xrange to range to bring compatibility with python3
Patch2:         officeparser-02_python3_xrange.patch

# add --help as default action to avoid the empty list error without parameters
# to fix error when no arguments are supplied
Patch3:         officeparser-03_default_help.patch

# Separate functions for the conversion of the python2 binary string / python3 binarray to ascii/hexdump
# This fixes issue with --print-header and --print-directory
Patch4:         officeparser-04_string_conversion.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools


%description
Python script officeparser.py that parses the format of OLE compound documents
used by Microsoft Office applications. Some useful features of this script
include: macro extraction, embedded file extraction, format analysis.


%prep
%autosetup -p 1 -n %{gitname}-%{commit}

# Change implicit "env python" to explicit versioned python shebang
# https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
sed 's|^#!/usr/bin/env python|#!%{__python3}|' officeparser.py > officeparser.py.new
touch -r officeparser.py officeparser.py.new &&
mv officeparser.py.new officeparser.py


%build
# its just a script, nothing to build


%install
install -D officeparser.py %{buildroot}%{_bindir}/officeparser.py


%files
%doc README.md
%license LICENSE
%{_bindir}/officeparser.py


%changelog
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180820-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Michal Ambroz <rebus AT_ seznam.cz> - 0.20180820-1


* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140818-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 02 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.20140818-4
- in each software there is at least 1 error. Times 4 if it is spec file :(

* Wed Jul 01 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.20140818-3
- add build dependency to python2-devel

* Wed Jul 01 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.20140818-2
- updates based on package review

* Wed Jun 10 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.20140818-1
- initial package for Fedora
