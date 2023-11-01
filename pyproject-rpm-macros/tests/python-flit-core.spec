Name:           python-flit-core
Version:        3.0.0
Release:        0%{?dist}
Summary:        Distribution-building parts of Flit

License:        BSD
URL:            https://pypi.org/project/flit-core/
Source0:        https://github.com/takluyver/flit/archive/%{version}/flit-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
Test a wheel built from a subdirectory.
Test a build with pyproject.toml backend-path = .
flit-core builds with flit-core.


%package -n python3-flit-core
Summary:        %{summary}

%description -n python3-flit-core
...


%prep
%autosetup -p1 -n flit-%{version}


%generate_buildrequires
cd flit_core
# this runtime-requires pytoml which is no longer available in Fedora
%pyproject_buildrequires -R
cd ..

%build
cd flit_core
%pyproject_wheel
cd ..


%install
%pyproject_install
%pyproject_save_files flit_core


%files -n python3-flit-core -f %{pyproject_files}
