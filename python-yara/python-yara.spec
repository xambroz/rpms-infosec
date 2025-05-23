Name:           python-yara
Version:        4.5.3
Summary:        Python binding for the YARA pattern matching tool
License:        Apache-2.0
URL:            https://github.com/VirusTotal/yara-python/
VCS:            https://github.com/VirusTotal/yara-python/
#               https://github.com/VirusTotal/yara-python/tags
#               https://github.com/VirusTotal/yara-python/releases/

# By default build from a release tarball.
# If you want to rebuild from a unversioned commit from git do that with
# rpmbuild --rebuild python-yara.src.dpm --without release
%bcond_without  release

%global         gituser         VirusTotal
%global         gitname         yara-python
%global         gitdate         20250523
%global         commit          5caac1ea81f7e700dc7969abd9706dd0cd1580ec
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


%global         common_description %{expand:
Python binding for the YARA pattern matching tool.
YARA is a tool aimed at (but not limited to) helping malware researchers to
identify and classify malware samples. With YARA you can create descriptions
of malware families (or whatever you want to describe) based on textual or
binary patterns. Each description, a.k.a rule, consists of a set of strings
and a Boolean expression which determine its logic.}

# Build with python2 support for RHEL7
%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%bcond_without     python2
%endif

%if 0%{?with_release}
Release:        %autorelease
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz#/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  pkgconfig(yara)
BuildRequires:  libtool
BuildRequires:  yara-devel >= %{version}
# html doc generation
BuildRequires:  /usr/bin/sphinx-build

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-setuptools


%if 0%{?with_python2}  > 0
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif


%description
%{common_description}


#====================================================================
%package -n python%{python3_pkgversion}-yara
Summary:        Python3 binding for the YARA pattern matching tool
%{?python_provide:%python_provide python%{python3_pkgversion}-yara}



%description -n python%{python3_pkgversion}-yara
%{common_description}

%if 0%{?with_python2}  > 0
%package -n python2-yara
Summary:        Python2 binding for the YARA pattern matching tool
%{?python_provide:%python_provide python2-yara}


%description -n python2-yara
%{common_description}
%endif

#====================================================================
%prep
%if 0%{?with_release}
# Build from git release version
%autosetup -n yara-python-%{version}

%else
# Build from git commit
%autosetup -n yara-python-%{commit}
%endif



#====================================================================
%build
%if 0%{?with_python2}  > 0
%py2_build "--dynamic-linking"
%endif

%py3_build "--dynamic-linking"



#====================================================================
%install
%if 0%{?with_python2}  > 0
%py2_install
%endif

%py3_install


#====================================================================
%check
# testModuleData is always failing for architecture armv7hl
# Remove once Fedora 36 is EOL
%ifarch armv7hl
EXCLUDE='not testModuleData'
%endif

%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
export CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}"
export PATH="%{buildroot}%{_bindir}:$PATH"
export PYTHONPATH="${PYTHONPATH:-%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}}"
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_XDIST_AUTO_NUM_WORKERS=%{_smp_build_ncpus}}
pytest-3 -k "$EXCLUDE" tests.py -v
%else
%pytest -k "$EXCLUDE" tests.py -v
%endif


#====================================================================
%files -n python%{python3_pkgversion}-yara
%license LICENSE
%doc README.rst
%{python3_sitearch}/yara*

%if 0%{?with_python2}  > 0
%files -n python2-yara
%license LICENSE
%doc README.rst
%{python2_sitearch}/yara*
%endif

#====================================================================
%changelog
%autochangelog
