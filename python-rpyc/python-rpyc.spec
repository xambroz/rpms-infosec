Name:           python-rpyc
Version:        5.3.1
Release:        %autorelease
Summary:        Transparent, Symmetrical Python Library for Distributed-Computing
License:        MIT
URL:            http://rpyc.wikidot.com/
VCS:            https://github.com/tomerfiliba/rpyc/

%global modname rpyc

Source0:        https://github.com/tomerfiliba/rpyc/archive/%{version}/%{modname}-%{version}.tar.gz
BuildArch:      noarch

%global _description\
RPyC, or Remote Python Call, is a transparent and symmetrical python library\
for remote procedure calls, clustering and distributed-computing.\
RPyC makes use of object-proxies, a technique that employs python's dynamic\
nature, to overcome the physical boundaries between processes and computers,\
so that remote objects can be manipulated as if they were local.

%description %_description


%package -n python3-%{modname}
Summary:        %{summary}

BuildRequires:  python%{python3_pkgversion}-devel
Obsoletes:      python2-%{modname} < 4.0.1-4
%{?python_provide:%python_provide python3-%{modname}}

%description -n python3-%{modname} %_description


%generate_buildrequires
%pyproject_buildrequires -t


%prep
%autosetup -n %{modname}-%{version} -p 1

%build
%pyproject_wheel

%install
%pyproject_install

# The binaries should not have .py extension
mv %{buildroot}%{_bindir}/rpyc_classic.py %{buildroot}%{_bindir}/rpyc_classic
mv %{buildroot}%{_bindir}/rpyc_registry.py %{buildroot}%{_bindir}/rpyc_registry

%py3_shebang_fix %{buildroot}%{_bindir}/rpyc_* %{buildroot}%{python3_sitelib}/rpyc*

%pyproject_save_files rpyc


%check
%tox


%files -n python3-%{modname} -f %{pyproject_files}
%{_bindir}/rpyc_*

%changelog
%autochangelog

