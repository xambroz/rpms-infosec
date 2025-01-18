Name:           python-colorclass
Version:        2.2.2
Release:        %autorelease
Summary:        Yet another ANSI color text library for Python

%global srcname colorclass

License:        MIT
URL:            https://pypi.python.org/pypi/colorclass
VCS:            git:https://github.com/matthewdeanmartin/colorclass
# was           https://github.com/Robpol86/colorclass
Source0:        https://files.pythonhosted.org/packages/source/c/%{srcname}/%{srcname}-%{version}.tar.gz
# Source1:      https://github.com/Robpol86/colorclass/blob/master/LICENSE


BuildArch:      noarch

%description
Colorful worry-free console applications for Linux, Mac OS X, and Windows.
Yet another ANSI color text library for Python. Provides "auto colors" for
dark/light terminals. Works on Linux, OS X, and Windows.

%package -n python3-%{srcname}
Summary:        Yet another ANSI color text library for Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Colorful worry-free console applications for Linux, Mac OS X, and Windows.
Yet another ANSI color text library for Python. Provides "auto colors" for
dark/light terminals. Works on Linux, OS X, and Windows.

%prep
%autosetup -n %{srcname}-%{version} -p1
# cp %%{SOURCE1} .
rm -rf colorclass.egg-info

%build
%py3_build

%install
%py3_install

%check
# %%{python3} -m unittest
%py3_check_import colorclass

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/colorclass*

%changelog
%autochangelog
