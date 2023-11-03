Summary:        Python tool for decrypting MS Office files with passwords or other keys
Name:           msoffcrypto-tool
Version:        5.1.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/nolze/msoffcrypto-tool
VCS:            https://github.com/nolze/msoffcrypto-tool
#               https://github.com/nolze/msoffcrypto-tool/tags
Source:         https://github.com/nolze/msoffcrypto-tool/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%global         common_description %{expand:
The msoffcrypto-tool (formerly ms-offcrypto-tool) is a Python tool and
library for decrypting encrypted Microsoft Office files with password,
intermediate key, or private key which generated its escrow key.
}

%global modulename msoffcrypto

BuildRequires:  python%{python3_pkgversion}-devel
%if 0%{?rhel} && 0%{?rhel} < 9
BuildRequires:  pyproject-rpm-macros
%endif

# Tests
BuildRequires:  python%{python3_pkgversion}-pytest
# BuildRequires:  python%%{python3_pkgversion}-setuptools

Requires:       python%{python3_pkgversion}-%{modulename}

%description %{common_description}


%package -n python%{python3_pkgversion}-%{modulename}
Summary:        Python library for decrypting MS Office files with passwords or other keys
Requires:       python%{python3_pkgversion}-cryptography >= 2.3
Requires:       python%{python3_pkgversion}-olefile >= 0.45
%{?python_provide:%python_provide python%{python3_pkgversion}-%{modulename}}

%description -n python%{python3_pkgversion}-%{modulename} %{common_description}


%generate_buildrequires
%pyproject_buildrequires


%prep
%autosetup


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{modulename}


%check
%if 0%{?rhel} && 0%{?rhel} < 8
pytest-3 -sv
%else
%pytest -sv
%endif


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}


%files -n python%{python3_pkgversion}-%{modulename} -f %{pyproject_files}
%license LICENSE.txt


%changelog
* Thu Nov 02 2023 Michal Ambroz <rebus _AT seznam.cz> 5.1.1-1
- Upgrade to 5.1.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 5.0.0-3
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Michal Ambroz <rebus _AT seznam.cz> 5.0.0-1
- Upgrade to 5.0.0
- migrate the spec to poetry / pyproject-rpm-macros

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 4.11.0-7
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Miro Hrončok <mhroncok@redhat.com> - 4.11.0-5
- Switch the test runner in %%check from deprecated nose to pytest
- Drop undesired and unused build dependency on coverage

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.11.0-3
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Robert Scheck <robert@fedoraproject.org> 4.11.0-1
- Upgrade to 4.11.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.10.1-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 10 2019 Robert Scheck <robert@fedoraproject.org> 4.10.1-1
- Upgrade to 4.10.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.10.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.10.0-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Robert Scheck <robert@fedoraproject.org> 4.10.0-1
- Upgrade to 4.10.0
- Initial spec file for Fedora and Red Hat Enterprise Linux
