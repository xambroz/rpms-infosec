Name:		python-pyringe
Summary:	Python tool to analyze NTFS MFT
Group:		Applications/Forensics Tools
Version:	1.0.2
License:	CPL-1.0

Release:	0.1%{?dist}
URL:		https://github.com/google/pyringe
VCS:		https://github.com/google/pyringe

%global         gituser         google
%global         gitname         pyringe
%global         gitdate         20140510
%global         commit          76dff5d1ac29cd5e7bf32677654a83291a15ad8a
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{gitname}-%{version}-%{shortcommit}.tar.gz

%if 0%{?centos}0%{?amzn} == 70
%define python3_pkgversion 36
%endif

BuildArch:      noarch
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

%global         common_description %{expand:
pyringe.py is designed to fully parse the MFT file from an NTFS filesystem
and present the results as accurately as possible in multiple formats.
}

%description %common_description


%package -n     python3-pyringe
Summary:        %{summary}
%{?python_provide:%python_provide python3-pyringe}
# for convenience update the older CERT package
Provides: pyringe = %{version}-%{release}
Obsoletes: pyringe <= 3.0.1

%description -n python3-pyringe %common_description

%prep
%autosetup -n %{gitname}-%{commit} -p 1

%build
%py3_build


%install
%py3_install
ln -s %{gitname}.py %{buildroot}%{_prefix}/bin/%{gitname}


%files -n python3-pyringe
%doc CHANGES.txt README.txt
%license LICENSE.txt
%{_bindir}/%{gitname}
%{_bindir}/%{gitname}.py
%{python3_sitelib}/pyringe
%{python3_sitelib}/*egg-info

%changelog
* Sat Apr 20 2024 Michal Ambroz <rebus _AT seznam.cz> - 1.0.1-0.1
