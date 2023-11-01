Name:           python-ldap
Version:        3.3.0
Release:        0%{?dist}
License:        Python
Summary:        An object-oriented API to access LDAP directory servers
Source0:        %{pypi_source}

# OpenLDAP 2.5+ is not yet supported by python-ldap
# https://github.com/python-ldap/python-ldap/issues/432
# Fedora has this patch to make it build, but the tests will fail anyway
Patch0:         https://src.fedoraproject.org/rpms/python-ldap/raw/a237d9b212bd1581e07f4f1a8f54c26a7190843c/f/python-ldap-always-use-ldap-library.patch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

BuildRequires:  cyrus-sasl-devel
BuildRequires:  gcc
BuildRequires:  openldap-clients
BuildRequires:  openldap-devel
BuildRequires:  openldap-servers
BuildRequires:  openssl-devel


%description
This package contains extension modules. Does not contain pyproject.toml.
Has multiple files and directories.
Building this tests:
- the proper files are installed in the proper places
- module glob in %%pyproject_save_files (some modules are included, some not)
- combined manual and generated Buildrequires
- building an extension module via %%pyproject_buildrequires -w


%package -n     python3-ldap
Summary:        %{summary}

%description -n python3-ldap
%{summary}


%prep
%autosetup
# Hack: We remove tests that are broken by OpenLDAP 2.5+
# Don't do this in the regular Fedora package, please
rm Tests/t_ldapobject.py Tests/t_cext.py Tests/t_edit.py Tests/t_ldap_sasl.py Tests/t_ldap_syncrepl.py Tests/t_slapdobject.py Tests/t_bind.py Tests/t_ldap_options.py Tests/t_ldap_schema_subentry.py


%generate_buildrequires
# -w is not required with this package, but we test that we can use it anyway
%pyproject_buildrequires -t -w


%build
#%%pyproject_wheel -- this is done via %%pyproject_buildrequires -w

# Internal check that we can import the built extension modules from %%{pyproject_build_lib}
%{python3} -c 'import _ldap' && exit 1 || true
PYTHONPATH=%{pyproject_build_lib} %{python3} -c 'import _ldap'


%install
%pyproject_install
# We can pass multiple globs
%pyproject_save_files 'ldap*' '*ldap'


%check
%tox

# Internal check if the instalation outputs expected files
test -d %{buildroot}%{python3_sitearch}/__pycache__/
test -d %{buildroot}%{python3_sitearch}/python_ldap-%{version}.dist-info/
test -d %{buildroot}%{python3_sitearch}/ldap/
test -f %{buildroot}%{python3_sitearch}/ldapurl.py
test -f %{buildroot}%{python3_sitearch}/ldif.py
test -d %{buildroot}%{python3_sitearch}/slapdtest/
test -f %{buildroot}%{python3_sitearch}/_ldap.cpython-*.so

# Internal check: Unmatched modules are not supposed to be listed in %%{pyproject_files}
# We'll list them explicitly
grep -F %{python3_sitearch}/ldif.py %{pyproject_files} && exit 1 || true
grep -F %{python3_sitearch}/__pycache__/ldif.cpython-%{python3_version_nodots}.pyc %{pyproject_files} && exit 1 || true
grep -F %{python3_sitearch}/__pycache__/ldif.cpython-%{python3_version_nodots}.opt-1.pyc %{pyproject_files} && exit 1 || true
grep -F %{python3_sitearch}/slapdtest %{pyproject_files} && exit 1 || true

# Internal check: Unmatched modules are not supposed to be listed in %%{_pyproject_modules}
grep -F slapdtest %{_pyproject_modules} && exit 1 || true
grep -F ldif %{_pyproject_modules} && exit 1 || true
# Let's check that at least one module is listed in %%{_pyproject_modules}
grep -F ldapurl %{_pyproject_modules}

# Internal check: Top level __pycache__ is never owned
grep -E '/site-packages/__pycache__$' %{pyproject_files} && exit 1 || true
grep -E '/site-packages/__pycache__/$' %{pyproject_files} && exit 1 || true

# Internal check for the value of %%{pyproject_build_lib} in an archful package
%if 0%{?rhel} == 9
test "%{pyproject_build_lib}" == "$(echo %{_pyproject_builddir}/pip-req-build-*/build/lib.%{python3_platform}-%{python3_version})"
%elif 0%{?fedora} == 36
test "%{pyproject_build_lib}" == "%{_builddir}/%{buildsubdir}/build/lib.%{python3_platform}-%{python3_version}"
%else
test "%{pyproject_build_lib}" == "%{_builddir}/%{buildsubdir}/build/lib.%{python3_platform}-cpython-%{python3_version_nodots}"
%endif


%files -n python3-ldap -f %{pyproject_files}
%license LICENCE
%doc CHANGES README TODO Demo
# Explicitly listed files can be combined with automation
%pycached %{python3_sitearch}/ldif.py
%{python3_sitearch}/slapdtest/
