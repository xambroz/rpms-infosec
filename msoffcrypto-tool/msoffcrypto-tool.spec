Summary:        Python tool for decrypting MS Office files with passwords or other keys
Name:           msoffcrypto-tool
Version:        5.4.2
Release:        %autorelease
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

# python command needed for tests
BuildRequires:  /usr/bin/python
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
rm -f %{buildroot}%{python3_sitelib}/NOTICE.txt
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
%license LICENSE.txt NOTICE.txt



%changelog
%autochangelog