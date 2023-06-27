Name:           python-floss
Version:        2.0.0
%global         baserelease     1
Summary:        FLARE Obfuscated String Solver
License:        Apache-2.0
URL:            https://github.com/mandiant/flare-floss

# By default build from a release tarball.
# If you want to rebuild from a unversioned commit from git do that with
# rpmbuild --rebuild python-floss.src.dpm --without release
%bcond_without  release

%global         commit          dd9bea80bd65be9b820e94773f4dcc846d28d527
%global         gitdate         20220621
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


%global         common_description %{expand:
The FLARE Obfuscated String Solver (FLOSS, formerly FireEye Labs Obfuscated String Solver)
uses advanced static analysis techniques to automatically deobfuscate strings from malware
binaries. You can use it just like strings.exe to enhance basic static analysis of unknown
binaries.}

# Build with python2 support for RHEL7
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
%bcond_without     python2
%endif

%if 0%{?with_release}
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/mandiant/flare-floss/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/mandiant/flare-floss/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif


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
%package -n python%{python3_pkgversion}-floss
Summary:        Python3 version of FLARE Obfuscated String Solver
%{?python_provide:%python_provide python%{python3_pkgversion}-floss}



%description -n python%{python3_pkgversion}-floss
%{common_description}

%if 0%{?with_python2}  > 0
%package -n python2-floss
Summary:        Python2 version of FLARE Obfuscated String Solver
%{?python_provide:%python_provide python2-floss}


%description -n python2-floss
%{common_description}
%endif

#====================================================================
%prep
%if 0%{?with_release}
# Build from git release version
%autosetup -n flare-floss-%{version}

%else
# Build from git commit
%autosetup -n flare-floss-%{commit}
%endif



#====================================================================
%build
%if 0%{?with_python2}  > 0
%py2_build
%endif

%py3_build



#====================================================================
%install
%if 0%{?with_python2}  > 0
%py2_install
%endif

%py3_install


#====================================================================
%check
%pytest tests.py -v

#====================================================================
%files -n python%{python3_pkgversion}-floss
%license LICENSE
%doc README.rst
%{python3_sitearch}/floss*

%if 0%{?with_python2}  > 0
%files -n python2-floss
%license LICENSE
%doc README.rst
%{python2_sitearch}/floss*
%endif

#====================================================================
%changelog
* Thu Jun 23 2022 Michal Ambroz <rebus at, seznam.cz> - 2.0.0-1
- initial package
