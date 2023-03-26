Name:           python-evtx
Version:        0.7.4
License:        APLv2
Release:        2%{?dist}
Summary:        Pure Python parser for new Windows Event Log XML files (.evtx)
URL:            https://github.com/williballenthin/python-evtx/
# URL:          https://pypi.python.org/pypi/python-evtx
#               https://github.com/williballenthin/python-evtx/releases


%global         gituser         williballenthin
%global         gitname         python-evtx
%global         commit          86905344699452088e155589ec5900ce74ae3d1c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  python3
%bcond_with     python2


Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         python-evtx-deps-versions.patch

BuildArch:        noarch

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-hexdump
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-cov
Requires:       python%{python3_pkgversion}-hexdump
%endif

%global common_description %{expand:
Pure Python parser for recent Windows Event Log files (those with the file
extension ".evtx"). The module provides programmatic access to the File
and Chunk headers, record templates, and event entries. For example, you
can use python-evtx to review the event logs of Windows 7 systems from a Mac
or Linux workstation. The structure definitions and parsing strategies were
heavily inspired by the work of Andreas Schuster and his Perl implementation
"Parse-Evtx".
}

%description
%common_description



%if %{with python2}
%package -n python2-evtx
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python2-evtx}

%description -n python2-evtx
%common_description

%endif


%if %{with python3}
%package -n python%{python3_pkgversion}-evtx
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-evtx}

%description -n python%{python3_pkgversion}-evtx
%common_description

%endif


%prep
#setup -q -n %{gitname}-%{commit}
%autosetup -n %{name}-%{version}


%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%pyproject_wheel
%endif

%install
%if %{with python2}
%py2_install
pushd %{buildroot}%{_bindir}
for I in *.py ; do
    BASENAME=$(basename "$I" .py)
    mv "$I" "${BASENAME}-%{python2_version}"
    ln -s "${BASENAME}-%{python2_version}" "${BASENAME}-2"

done
popd
%endif

%if %{with python3}
%pyproject_install

# Doesn't work
# pyproject_save_files Evtx python_evtx

pushd %{buildroot}%{_bindir}
for I in *.py ; do
    BASENAME=$(basename "$I" .py)
    mv "$I" "${BASENAME}-%{python3_version}"
    ln -s "${BASENAME}-%{python3_version}" "${BASENAME}-3"
done
popd
%endif


# Default link
pushd %{buildroot}%{_bindir}

%if (0%{?fedora} && 0%{?fedora} <= 30 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
    #Link to python2 as default on fedora up to 30 and rhel up to 7
    for I in *-2 ; do
        BASENAME=$(basename "$I" "-2" )
        ln -s "${I}" "${BASENAME}.py"
    done
%else
    #Link to python3 as default on fedora 31+ and rhel8+ and everything else
    for I in *-3 ; do
        BASENAME=$(basename "$I" "-3" )
        ln -s "${I}" "${BASENAME}.py"
    done
%endif
popd



%if %{with python2}
%files -n python2-evtx
%license LICENSE.TXT
%{python2_sitelib}/Evtx
%{python2_sitelib}/python_evtx*egg-info
%{_bindir}/evtx_*-2
%{_bindir}/evtx_*-%{python2_version}
%if (0%{?fedora} && 0%{?fedora} <= 30 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
%{_bindir}/evtx_*.py
%endif
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-evtx
%license LICENSE.TXT
%doc README.md
%{python3_sitelib}/Evtx
%{python3_sitelib}/python_evtx-*.dist-info
%{_bindir}/evtx_*-3
%{_bindir}/evtx_*-%{python3_version}
%if (0%{?fedora} && 0%{?fedora} >= 31 ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
%{_bindir}/evtx_*.py
%endif
%endif


%changelog
* Sun Mar 26 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.7.4-2
- modernize spec

* Wed Apr 14 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.7.4-1
- bump to 0.7.4

* Wed Apr 14 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.6.1-2
- build python3

* Wed Oct 04 2017 Michal Ambroz <rebus _AT seznam.cz> - 0.6.1-1
- Initial package for Fedora
