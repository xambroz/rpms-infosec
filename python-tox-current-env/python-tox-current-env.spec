Name:           python-tox-current-env
Version:        0.0.11
Release:        5%{?dist}
Summary:        Tox plugin to run tests in current Python environment

License:        MIT
URL:            https://github.com/fedora-python/tox-current-env
Source0:        %{pypi_source tox-current-env}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

%bcond tests 1

%description
The tox-current-env plugin allows to run tests in current Python environment.


%package -n     python%{python3_pkgversion}-tox-current-env
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-tox-current-env}

%description -n python%{python3_pkgversion}-tox-current-env
The tox-current-env plugin allows to run tests in current Python environment.


%prep
%autosetup -n tox-current-env-%{version}


%generate_buildrequires
# Don't use %%pyproject_buildrequires -t/-e to avoid a build dependency loop
%pyproject_buildrequires %{?with_tests:-x tests}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files tox_current_env


%check
# hooks[34].py are imported in hooks.py based on tox version so we have to
# exclude them here.
%pyproject_check_import -e '*.hooks?'
%if %{with tests}
# deselected tests run tox without the options for this plugin and hence they need internet
%pytest -k "not regular and not noquiet_installed_packages[None]"
%endif


%files -n python%{python3_pkgversion}-tox-current-env -f %{pyproject_files}
%doc README.rst


%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 0.0.11-4
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.0.11-3
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Miro Hrončok <mhroncok@redhat.com> - 0.0.11-1
- Update to 0.0.11 with tox 4.1.2+ support

* Wed Dec 14 2022 Miro Hrončok <mhroncok@redhat.com> - 0.0.10-1
- Update to 0.0.10 with tox 4 support

* Wed Dec 07 2022 Miro Hrončok <mhroncok@redhat.com> - 0.0.8-4
- Run tests during the package build

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.0.8-2
- Rebuilt for Python 3.11

* Wed Mar 02 2022 Miro Hrončok <mhroncok@redhat.com> - 0.0.8-1
- Update to 0.0.8 to support allowlist_externals

* Mon Feb 07 2022 Miro Hrončok <mhroncok@redhat.com> - 0.0.7-1
- Update to 0.0.7 to pin tox < 4

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 05 2021 Miro Hrončok <mhroncok@redhat.com> - 0.0.6-4
- In %%check, test if the module at least imports

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.0.6-2
- Rebuilt for Python 3.10

* Mon Mar 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0.0.6-1
- Update to 0.0.6

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.5-1
- Update to 0.0.5

* Wed Nov 04 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.4-1
- Update to 0.0.4

* Wed Sep 30 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.3-1
- Update to 0.0.3

* Wed Aug 12 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-7
- Fix FTBFS with pyproject-rpm-macros >= 0-23

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-2
- Rebuilt for Python 3.8

* Mon Aug 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-1
- Update to 0.0.2

* Wed Jul 24 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.1-1
- Initial package
