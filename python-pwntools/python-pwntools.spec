Name:           python-pwntools
Version:        4.11.1
Release:        1%{?dist}
Summary:        A CTF framework and exploit development library
URL:            https://github.com/Gallopsled/pwntools/
VCS:            https://github.com/Gallopsled/pwntools/

# ./LICENSE-pwntools.txt - base project of pwntools is licensed as MIT
# ./pwnlib/data/includes/LICENSE.txt
#    - header files from FreeBSD licensed with BSD 2-clause license
#    - header files from dietlibc licensed with GPLv2 or later
# ./pwnlib/data/useragents/LICENSE.txt - script `download-useragents.py licensed with BSD 2-clause license
License:        MIT AND BSD-2-Clause AND GPL-2.0-or-later

%global srcname pwntools

# Source0:      https://github.com/Gallopsled/%%{srcname}/archive/%%{srcname}-%%{version}.tar.gz
Source0:        https://github.com/Gallopsled/%{srcname}/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Waiting on pwntools to support newer sphinx shipped by Fedora.
# BuildRequires:  python3-sphinx

%description
Pwntools is a CTF framework and exploit development library. Written
in Python, it is designed for rapid prototyping and development, and
intended to make exploit writing as simple as possible.

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
Requires:       binutils

%description -n python3-%{srcname}
Pwntools is a CTF framework and exploit development library. Written
in Python, it is designed for rapid prototyping and development, and
intended to make exploit writing as simple as possible.

# Waiting on pwntools to support newer sphinx shipped by Fedora.
# %%package doc
# Summary:        pwntools documentation
#
# %%description doc
# Documentation for pwntools.

%prep
%autosetup -n %{srcname}-%{version} -p1

#wrong permission
chmod -x docs/requirements.txt


%build
%py3_build
# Waiting on pwntools to support newer sphinx shipped by Fedora.
# # Generate html documentation.
# PYTHONPATH=${PWD} sphinx-build-2 docs/source html
# # Remove the sphinx-build leftovers.
# rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

mv %{buildroot}%{_bindir}/checksec %{buildroot}%{_bindir}/checksec-pwntools

# setuptools < 60 installs pwntools-doc to sitelib
# setuptools >= 60 changes the installation location
# remove pwntools-doc from both locations
rm -rf %{buildroot}%{python3_sitelib}/pwntools-doc
rm -rf %{buildroot}%{_prefix}/pwntools-doc

%files -n python3-%{srcname}
%doc CHANGELOG.md CONTRIBUTING.md README.md TESTING.md docs/requirements.txt
%license LICENSE-pwntools.txt
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/pwn/
%{python3_sitelib}/pwnlib/
%{_bindir}/asm
%{_bindir}/checksec-pwntools
%{_bindir}/common
%{_bindir}/constgrep
%{_bindir}/cyclic
%{_bindir}/debug
%{_bindir}/disablenx
%{_bindir}/disasm
%{_bindir}/elfdiff
%{_bindir}/elfpatch
%{_bindir}/errno
%{_bindir}/hex
%{_bindir}/libcdb
%{_bindir}/main
%{_bindir}/phd
%{_bindir}/pwn
%{_bindir}/pwnstrip
%{_bindir}/scramble
%{_bindir}/shellcraft
%{_bindir}/template
%{_bindir}/unhex
%{_bindir}/update
%{_bindir}/version

# Waiting on pwntools to support newer sphinx shipped by Fedora.
# %%files doc
# %%doc html
# %%license LICENSE-pwntools.txt

%changelog
* Mon Nov 20 2023 Michal Ambroz <rebus _AT seznam.czike@flyn.org> - 4.11.1-1
- New upstream version 4.11.1
- change license references to new SPDX format

* Mon Sep 25 2023 W. Michael Petullo <mike@flyn.org> - 4.11.0-2
- Deal with requirements.txt, which moved.

* Mon Sep 25 2023 W. Michael Petullo <mike@flyn.org> - 4.11.0-1
- New upstream version

* Sat Sep 09 2023 W. Michael Petullo <mike@flyn.org> - 4.9.0-5
- Fix BZ #2238038; rename to checksec-pwntools to remove conflict with checksec package

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.9.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Jonathan Wright <jonathan@almalinux.org> - 4.9.0-1
- Update to 4.9.0 rhbz#1902526
- Fix changelog from 4.8.0-4 missing > after email

* Fri Dec 02 2022 W. Michael Petullo <mike@flyn.org> - 4.8.0-4
- Fix BZ #2149766; backport patch that fixes compatibility with Python 3.11

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.8.0-2
- Rebuilt for Python 3.11

* Fri May 13 2022 W. Michael Petullo <mike@flyn.org> - 4.8.0-1
- New upstream version

* Fri Mar 04 2022 Karolina Surmao <ksurma@redhat.com> - 4.7.0-3
- Fix python-pwntools build with setuptools >= 60

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 W. Michael Petullo <mike@flyn.org> - 4.7.0-1
- New upstream version

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.3.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 06 2020 W. Michael Petullo <mike@flyn.org> - 4.3.0-2
- Fix BZ #1892888; something did not like setup.py's 'unicorn>=1.0.2rc1,<1.0.2rc4'

* Fri Nov 06 2020 W. Michael Petullo <mike@flyn.org> - 4.3.0-1
- New upstream version

* Thu Oct 08 2020 W. Michael Petullo <mike@flyn.org> - 4.2.1-1
- New upstream version

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.1.0-2
- Rebuilt for Python 3.9

* Fri May 08 2020 W. Michael Petullo <mike@flyn.org> - 4.1.0-1
- New upstream version

* Thu Dec 19 2019 W. Michael Petullo <mike@flyn.org> - 4.0.0-0.1.b0
- New upstream version
- Migrate to Python 3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 16 2019 W. Michael Petullo <mike@flyn.org> - 3.12.2-1
- New upstream version
- Adjust requires.txt

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 W. Michael Petullo <mike@flyn.org> - 3.12.1-1
- New upstream version
- Drop python2-pypandoc requirement

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 W. Michael Petullo <mike@flyn.org> - 3.12.0-1
- Initial package
