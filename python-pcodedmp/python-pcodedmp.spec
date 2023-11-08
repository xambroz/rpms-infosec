%global srcname pcodedmp

# Bootstrap may be needed to break circular dependencies between
# python-pcodedmp and python-oletools
%bcond_with     bootstrap

# No python-pypandoc packages in EPEL 8 (yet?)
%if 0%{?fedora} || 0%{?rhel} == 7
%bcond_without  pypandoc
%else
%bcond_with     pypandoc
%endif

Summary:        VBA p-code disassembler
Name:           python-%{srcname}
Version:        1.2.6
Release:        17%{?dist}
License:        GPLv3+
URL:            https://github.com/bontchev/pcodedmp
Source0:        %{pypi_source}
Patch0:         python-pcodedmp-1.2.6-python27.patch
BuildArch:      noarch

%global _description %{expand:
Macros written in VBA (Visual Basic for Applications; the macro programming
language used in Microsoft Office) exist in three different executable forms,
each of which can be what is actually executed at run time, depending on the
circumstances: Source code, p-code and execodes.

Since most of the time it is the p-code that determines what exactly a macro
would do (even if neither source code, nor execodes are present), pcodedmp is
a Python library and command line tool to display it.}

%description %_description

%package -n %{srcname}
Summary:        %{summary}
Requires:       python%{python3_pkgversion}-%{srcname} = %{version}-%{release}

%description -n %{srcname} %_description

%if 0%{?rhel} && 0%{?rhel} < 8
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with pypandoc}
BuildRequires:  python2-pypandoc
%endif
%if %{without bootstrap}
BuildRequires:  python2-oletools >= 0.54
Requires:       python2-oletools >= 0.54
%endif
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %_description
%endif

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with pypandoc}
BuildRequires:  python%{python3_pkgversion}-pypandoc
%endif
%if %{without bootstrap}
BuildRequires:  python%{python3_pkgversion}-lxml
BuildRequires:  python%{python3_pkgversion}-oletools >= 0.54
Requires:       python%{python3_pkgversion}-oletools >= 0.54
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname} %_description

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-setuptools
%if %{with pypandoc}
BuildRequires:  python%{python3_other_pkgversion}-pypandoc
%endif
%if %{without bootstrap}
BuildRequires:  python%{python3_other_pkgversion}-lxml
BuildRequires:  python%{python3_other_pkgversion}-oletools >= 0.54
Requires:       python%{python3_other_pkgversion}-oletools >= 0.54
%endif
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{srcname}}

%description -n python%{python3_other_pkgversion}-%{srcname} %_description
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%if 0%{?rhel} && 0%{?rhel} < 8
%py2_build
%endif
%py3_build
%{?with_python3_other:%py3_other_build}

%install
%if 0%{?rhel} && 0%{?rhel} < 8
%py2_install
%endif
%py3_install
%{?with_python3_other:%py3_other_install}

%if %{without bootstrap}
%check
%{__python3} setup.py test
%{?with_python3_other:%{__python3_other} setup.py test}
%endif

%files -n %{srcname}
%{_bindir}/%{srcname}

%if 0%{?rhel} && 0%{?rhel} < 8
%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}-*.egg-info
%endif

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/
%endif

%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Python Maint <python-maint@redhat.com> - 1.2.6-16
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.6-15
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.6-12
- Rebuilt for pyparsing-3.0.9

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 1.2.6-11
- Rebuilt for Python 3.11

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 1.2.6-10
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.6-7
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.6-6
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Robert Scheck <robert@fedoraproject.org> 1.2.6-3
- Require python-setuptools during build-time explicitly

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-2
- Rebuilt for Python 3.9

* Mon May 04 2020 Robert Scheck <robert@fedoraproject.org> 1.2.6-1
- Upgrade to 1.2.6 (#1832610)
- Initial spec file for Fedora and Red Hat Enterprise Linux
