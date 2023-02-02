Name:           python-distorm3
Version:        3.4.4
Release:        1%{?dist}
Summary:        Powerful Disassembler Library For x86/AMD64
License:        GPLv3

%global         srcname         distorm3
%global         gituser         gdabah
%global         gitname         distorm
%global         commit          0dcd35c9927efd69587a880fea2423dde0fb8a96
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 7 )
%global with_python3 1
%endif

%if ( 0%{?fedora} && 0%{?fedora} <= 32 ) || ( 0%{?rhel} && 0%{?rhel} <= 8 )
# distorm3 needed for python2-volatility
%global with_python2 1
%endif

URL:            https://github.com/gdabah/distorm
#Source0:       https://github.com/%%{gituser}/%%{gitname}/archive/%%{commit}/%%{name}-%%{version}-%%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%if 0%{?with_python2}
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python-libs
BuildRequires:  python-setuptools
%endif

%if 0%{?with_python3}
BuildRequires:  python3
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-libs
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif


%description
The diStorm is a lightweight, easy-to-use and fast decomposer library.
The diStorm disassembles instructions in 16, 32 and 64 bit modes.
Supported instruction sets: FPU, MMX, SSE, SSE2, SSE3, SSSE3, SSE4,
3DNow! (w/ extensions), new x86-64 instruction sets, VMX, AMD's SVM and AVX.
The output of new interface of diStorm is a special structure that can describe
any x86 instruction, this structure can be later formatted into text for
display too.


%if 0%{?with_python2}
%package -n python2-%{srcname}
Summary:        Powerful Disassembler Library For x86/AMD64
Group:          Development/Libraries
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
The diStorm is a lightweight, easy-to-use and fast decomposer library.
The diStorm disassembles instructions in 16, 32 and 64 bit modes.
Supported instruction sets: FPU, MMX, SSE, SSE2, SSE3, SSSE3, SSE4,
3DNow! (w/ extensions), new x86-64 instruction sets, VMX, AMD's SVM and AVX.
The output of new interface of diStorm is a special structure that can describe
any x86 instruction, this structure can be later formatted into text for
display too.
%endif



%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Powerful Disassembler Library For x86/AMD64
Group:          Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
The diStorm is a lightweight, easy-to-use and fast decomposer library.
The diStorm disassembles instructions in 16, 32 and 64 bit modes.
Supported instruction sets: FPU, MMX, SSE, SSE2, SSE3, SSSE3, SSE4,
3DNow! (w/ extensions), new x86-64 instruction sets, VMX, AMD's SVM and AVX.
The output of new interface of diStorm is a special structure that can describe
any x86 instruction, this structure can be later formatted into text for
display too.
%endif

%prep
%autosetup -n %{gitname}-%{version}


%build
%if 0%{?with_python2}
%py2_build
%endif

%if 0%{?with_python3}
%py3_build
%endif


%install
%if 0%{?with_python2}
%py2_install
%endif

%if 0%{?with_python3}
%py3_install
%endif



%if 0%{?with_python2}
%files -n python2-%{srcname}
%license COPYING
# For arch-specific packages: sitearch
%{python2_sitearch}/*
%endif

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license COPYING
# For arch-specific packages: sitearch
%{python3_sitearch}/*
%endif


%changelog
* Sat May 16 2020 Michal Ambroz <rebus at, seznam.cz> 3.4.4-1
- bump to version 3.4.4

* Sat Apr 29 2017 Michal Ambroz <rebus at, seznam.cz> 3.3-git20150530.1
- bump to version 3.3.4

* Sun Mar 11 2012 Michal Ambroz <rebus at, seznam.cz> 3.3-git20150530.1
- Initial build for Fedora
