Name:           python-volatility3
Summary:        The volatile memory extraction framework
Version:        1.0.1
%global         baserelease     1


URL:            https://github.com/volatilityfoundation/volatility3
#               http://www.volatilityfoundation.org/
#               https://github.com/volatilityfoundation/volatility3/releases/

# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/OHECHDPLDJ7LLFUZXQMBBAXEXYTQMXOR/
# https://www.volatilityfoundation.org/license/vsl-v1.0
License:        vslv1

%global         gituser         volatilityfoundation
# this is hosted on github as...
%global         gitname         volatility3
%global         pyname          volatility3
%global         commit          8ecc7df9eb6b83ad1c82a9ad3b9790bffb568681
%global         gitdate         20210201
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


# %%global      pre .beta.1
# %%global      pypre b1
%global         upstream_version %{version}%{?pre:-%{pre}}
%global         py_version %{version}%{?pypre:%{pypre}}


# Build source is versioned github release=1 or unversioned git commit=0
%global         build_release    1

%if 0%{?build_release}  > 0
Release:        %{baserelease}%{?pre:%{pre}}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{upstream_version}/%{gitname}-%{upstream_version}.tar.gz
%else
Release:        %{baserelease}%{?pre:%{pre}}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
#Build_release
%endif


BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  /usr/bin/dos2unix

%global _description %{expand:
Volatility is the world’s most widely used framework for extracting digital
artifacts from volatile memory (RAM) samples. The extraction techniques are
performed completely independent of the system being investigated but offer
visibility into the runtime state of the system. The framework is intended
to introduce people to the techniques and complexities associated with
extracting digital artifacts from volatile memory samples and provide a
platform for further work into this exciting area of research.

In 2019, the Volatility Foundation released a complete rewrite of the
framework, Volatility 3. The project was intended to address many of the
technical and performance challenges associated with the original
code base that became apparent over the previous 10 years. Another benefit
of the rewrite is that Volatility 3 could be released under a custom
license that was more aligned with the goals of the Volatility community,
the Volatility Software License (VSL).}

%description %_description

%package -n     python%{python3_pkgversion}-%{gitname}
Summary:        %{summary}
Provides:       %{gitname} = %{version}-%{release}

Provides:       python%{python3_pkgversion}-%{pyname} = %{version}-%{release}

# I want to be able to install side by side with python2-volatility so the following fedora stub is disabled
# Provides:       %%{pyname} = %%{version}-%%{release}
# %%{?python_provide:%%python_provide python%%{python3_pkgversion}-%%{gitname}}
# %%{?python_provide:%%python_provide python%%{python3_pkgversion}-%%{pyname}}
# %%if 0%%{?fedora} > 31
# Obsoletes:      python2-volatility < 3
# %%endif

# from extras_require
%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} > 7 )
Recommends:     python%{python3_pkgversion}dist(jsonschema)
Recommends:     python%{python3_pkgversion}dist(yara-python)
Recommends:     python%{python3_pkgversion}dist(capstone)
%else
Requires:     python%{python3_pkgversion}dist(jsonschema)
Requires:     python%{python3_pkgversion}dist(yara-python)
Requires:     python%{python3_pkgversion}dist(capstone)
%endif

%description -n python%{python3_pkgversion}-%{gitname} %_description


%prep
%autosetup -n %{gitname}-%{upstream_version}



%build
%py3_build



%install
%py3_install
# highlevel importable module only used to develop volatility itself
# rm -r %{buildroot}%{python3_sitelib}/development

mv %{buildroot}%{_bindir}/vol{,3}
mv %{buildroot}%{_bindir}/volshell{,3}
ln -s vol3 %{buildroot}%{_bindir}/volatility3
ln -s volshell3 %{buildroot}%{_bindir}/volshell

# Replace pytho2-volatility on fc32+
%if 0%{?fedora} >= 32
ln -s vol3 %{buildroot}%{_bindir}/vol
ln -s volatility3 %{buildroot}%{_bindir}/volatility
%endif



%files -n python%{python3_pkgversion}-%{gitname}
%license LICENSE.txt
%doc README.md
%{_bindir}/vol3
%{_bindir}/volatility3
%{_bindir}/volshell3
%{_bindir}/volshell
%if 0%{?fedora} >= 32
%{_bindir}/vol
%{_bindir}/volatility
%endif
%{python3_sitelib}/%{pyname}/
%{python3_sitelib}/%{pyname}-%{py_version}-py%{python3_version}.egg-info/



%changelog
* Tue Mar 23 2021 Michal Ambroz <rebus AT_ seznam.cz> - 1.0.1-1
- bump to new upstream version 1.0.1

* Wed Oct 30 2019 Michal Ambroz <rebus AT_ seznam.cz> - 1.0.0-0.2.beta.1
- change summary, license name

* Wed Oct 30 2019 Michal Ambroz <rebus AT_ seznam.cz> - 1.0.0-0.1.beta.1
- switch to the generic leading 0. scheme for releases
- expected final release 2020-08
- always rename to ~3 to allow users to run side by side volatility2
  as migration of other plugins and utilities might take longer
- use %{python3_pkgversion} to make package compatible with EPEL

* Fri Oct 25 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0~beta.1-1
- Initial package

