Name:           python-ipykernel
Version:        6.11.0
Release:        0%{?dist}
Summary:        IPython Kernel for Jupyter
License:        BSD
URL:            https://github.com/ipython/ipykernel
Source0:        https://github.com/ipython/ipykernel/archive/v%{version}/ipykernel-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel

# some of the nested modules import from this, but upstream does not declare the dependency
BuildRequires:  python3-ipyparallel

%description
This package contains data files.
Building this tests that data files are not listed when +auto is not used
with %%pyproject_save_files.
Run %%pyproject_check_import on installed package and exclude unwanted modules
(if they're not excluded, build fails).
- We don't want to pull test dependencies just to check import
- The others fail to find `gi` and `matplotlib` which weren't declared
  in the upstream metadata


%package -n python3-ipykernel
Summary:        %{summary}

%description -n python3-ipykernel
...

%prep
%autosetup -p1 -n ipykernel-%{version}

# Remove the dependency on debugpy.
# See https://github.com/ipython/ipykernel/pull/767
sed -i '/"debugpy/d' pyproject.toml setup.py

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files 'ipykernel*' +auto

%check
%pyproject_check_import  -e '*.test*' -e 'ipykernel.gui*' -e 'ipykernel.pylab.*' -e 'ipykernel.trio*'

%files -n python3-ipykernel -f %{pyproject_files}
%license COPYING.md
%doc README.md

