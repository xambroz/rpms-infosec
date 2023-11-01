Name:           python-virtualenv
Version:        20.19.0
Release:        0%{?dist}
Summary:        Tool to create isolated Python environments

License:        MIT
URL:            http://pypi.python.org/pypi/virtualenv
Source:         %{pypi_source virtualenv}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-flaky
BuildRequires:  python3-pytest

%description
This specfile was added as a regression test to
https://src.fedoraproject.org/rpms/pyproject-rpm-macros/pull-request/363

It uses hatchling without %%pyproject_buildrequires -w.


%package -n     python3-virtualenv
Summary:        %{summary}

%description -n python3-virtualenv
...


%prep
%autosetup -p1 -n virtualenv-%{version}
# Relax the upper bounds of some dependencies to their known available versions in EL 9
sed -i -e 's/distlib<1,>=0.3.6/distlib<1,>=0.3.2/' \
       -e 's/filelock<4,>=3.4.1/filelock<4,>=3.3.1/' \
       -e 's/platformdirs<4,>=2.4/platformdirs<4,>=2.3/' \
       -e 's/hatchling>=1.12.2/hatchling>=0.25/' \
       -e 's/hatch-vcs>=0.3/hatch-vcs>=0.2.1/' \
    pyproject.toml
# Hacky backport of https://src.fedoraproject.org/rpms/python-virtualenv/c/87b1f95664
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 10
sed -i 's/_nonwrappers/_hookimpls/' tests/conftest.py
%endif


%generate_buildrequires
%pyproject_buildrequires -w


%build
# %%pyproject_buildrequires -w makes this redundant
# %%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files virtualenv
%{?el9:
# old version of setuptools_scm produces files incompatible with
# assumptions in virtualenv code, we append the expected attributes:
echo '__version__, __version_tuple__ = version, version_tuple' >> %{buildroot}%{python3_sitelib}/virtualenv/version.py
}


%check
# test_main fails when .dist-info is not deleted at the end of %%pyproject_buildrequires
PIP_CERT=/etc/pki/tls/certs/ca-bundle.crt \
%pytest -v -k test_main


%files -n python3-virtualenv -f %{pyproject_files}
%doc README.md
%{_bindir}/virtualenv
