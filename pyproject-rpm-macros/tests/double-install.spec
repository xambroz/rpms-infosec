Name:           double-install
Version:        0
Release:        0%{?dist}
Summary:        Install 2 wheels
License:        BSD and MIT
%global         markupsafe_version 2.0.1
%global         tldr_version 0.4.4
Source1:        https://github.com/pallets/markupsafe/archive/%{markupsafe_version}/MarkupSafe-%{markupsafe_version}.tar.gz
Source2:        %{pypi_source tldr %{tldr_version}}

BuildRequires:  gcc
BuildRequires:  python3-devel

%description
This package tests that we can build and install 2 wheels at once.
One of them is "noarch" and one has an extension module.


%prep
%setup -Tc
tar xf %{SOURCE1}
tar xf %{SOURCE2}


%generate_buildrequires
cd markupsafe-%{markupsafe_version}
%pyproject_buildrequires -R
cd ../tldr-%{tldr_version}
%pyproject_buildrequires -R
cd ..


%build
cd markupsafe-%{markupsafe_version}
%pyproject_wheel
cd ../tldr-%{tldr_version}
%pyproject_wheel
cd ..


%install
# This should install both the wheels:
%pyproject_install
#pyproject_save_files is not possible with 2 dist-infos


%check
# Internal check for the value of %%{pyproject_build_lib}
%if 0%{?rhel} == 9
for dir in . markupsafe-%{markupsafe_version} tldr-%{tldr_version}; do
  (cd $dir && test "%{pyproject_build_lib}" == "$(echo %{_pyproject_builddir}/pip-req-build-*/build/lib.%{python3_platform}-%{python3_version}):$(echo %{_pyproject_builddir}/pip-req-build-*/build/lib)")
done
%else
cd markupsafe-%{markupsafe_version}
%if 0%{?fedora} == 36
test "%{pyproject_build_lib}" == "%{_builddir}/%{buildsubdir}/markupsafe-%{markupsafe_version}/build/lib.%{python3_platform}-%{python3_version}"
%else
test "%{pyproject_build_lib}" == "%{_builddir}/%{buildsubdir}/markupsafe-%{markupsafe_version}/build/lib.%{python3_platform}-cpython-%{python3_version_nodots}"
%endif
cd ../tldr-%{tldr_version}
test "%{pyproject_build_lib}" == "%{_builddir}/%{buildsubdir}/tldr-%{tldr_version}/build/lib"
cd ..
%endif


%files
%{_bindir}/tldr*
%pycached %{python3_sitelib}/tldr.py
%{python3_sitelib}/tldr-%{tldr_version}.dist-info/
%{python3_sitearch}/MarkupSafe-%{markupsafe_version}.dist-info/
%{python3_sitearch}/markupsafe/
