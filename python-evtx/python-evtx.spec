Name:		python-evtx
Version:	0.6.1
License:	APLv2
Release:	2%{?dist}
Summary:	Pure Python parser for new Windows Event Log XML files (.evtx)
URL:		https://github.com/williballenthin/python-evtx/
#		https://github.com/williballenthin/python-evtx/releases


%global         gituser         williballenthin
%global         gitname         python-evtx
%global         commit          86905344699452088e155589ec5900ce74ae3d1c
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  python3
%bcond_without  python2


#URL:		https://pypi.python.org/pypi/python-evtx
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildArch:	noarch

%if 0%{?with_python2}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-hexdump
%endif

%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
Requires:       python3-hexdump
%endif

%description
Pure Python parser for recent Windows Event Log files (those with the file
extension ".evtx"). The module provides programmatic access to the File
and Chunk headers, record templates, and event entries. For example, you
can use python-evtx to review the event logs of Windows 7 systems from a Mac
or Linux workstation. The structure definitions and parsing strategies were
heavily inspired by the work of Andreas Schuster and his Perl implementation
"Parse-Evtx".


%if 0%{?with_python2}
%package -n python2-evtx
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python2-evtx}

%description -n python2-evtx
Pure Python parser for recent Windows Event Log files (those with the file
extension ".evtx"). The module provides programmatic access to the File
and Chunk headers, record templates, and event entries. For example, you
can use python-evtx to review the event logs of Windows 7 systems from a Mac
or Linux workstation. The structure definitions and parsing strategies were
heavily inspired by the work of Andreas Schuster and his Perl implementation
"Parse-Evtx".
%endif


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-evtx
Summary:        Dump binary data to hex format and restore from there
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-evtx}

%description -n python%{python3_pkgversion}-evtx
Pure Python parser for recent Windows Event Log files (those with the file
extension ".evtx"). The module provides programmatic access to the File
and Chunk headers, record templates, and event entries. For example, you
can use python-evtx to review the event logs of Windows 7 systems from a Mac
or Linux workstation. The structure definitions and parsing strategies were
heavily inspired by the work of Andreas Schuster and his Perl implementation
"Parse-Evtx".
%endif


%prep
#setup -q -n %{gitname}-%{commit}
%setup -q -n %{name}-%{version}


%build
%if 0%{?with_python2}
%{__python2} setup.py build
%endif
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%if 0%{?with_python2}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%endif
%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%if 0%{?with_python2}
%files -n python2-evtx
%license LICENSE.TXT
%{python2_sitelib}/Evtx
%{python2_sitelib}/python_evtx*egg-info
%{_bindir}/evtx_*.py
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-evtx
%license LICENSE.TXT
%doc README.md
%{python3_sitelib}/Evtx
%{python3_sitelib}/python_evtx*egg-info
%{_bindir}/evtx_*.py
%endif


%changelog
* Tue Apr 14 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.6.1-2
- build python3

* Wed Oct 04 2017 Michal Ambroz <rebus _AT seznam.cz> - 0.6.1-1
- Initial package for Fedora
