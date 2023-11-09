Name:           readpe
Version:        0.82
%global         baserelease 1
Summary:        Command line toolkit to work with and analyze PE binaries
URL:            https://github.com/mentebinaria/readpe
VCS:            https://github.com/mentebinaria/readpe
#               https://github.com/mentebinaria/readpe/releases

License:        GPL-2.0-or-later

%global         common_description %{expand:
Open source, full-featured, multiplatform command line toolkit to work with
and analyze PE (Portable Executables) binaries.}

%global         gituser         mentebinaria
%global         gitname         readpe
%global         gitdate         20230512
%global         commit          ad4d5a586f022f36b6b925a63ffd667cb729731d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%bcond_without  release

# Build from git release version
%if %{with release}
Release:       %{baserelease}%{?dist}
# Source0:     https://github.com/%%{gituser}/%%{gitname}/archive/v%%{upversion}.tar.gz#/%%{name}-%%{upversion}.tar.gz
Source0:       https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
# Build from git commit baseline
Release:       %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz
%endif


BuildRequires:  gcc

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:  openssl11-devel
%else
BuildRequires:  openssl-devel
%endif

%description
%{common_description}


#%%package        devel
# Summary:        Development files for %%{name}
# Requires:       %%{name}%%{?_isa} = %%{version}-%%{release}


# %%description    devel
# The %%{name}-devel package contains libraries and header files for
# developing applications that use %%{name}.
# %%{common_description}

%prep
%if %{with release}
    %autosetup -n %{gitname}-%{version} -p 1 -S git
%else
    %autosetup -n %{gitname}-%{commit} -p 1 -S git
%endif

%build
%make_build prefix=%{_prefix} libdir=%{_libdir}


%install
%make_install prefix=%{_prefix} libdir=%{_libdir}

rm -f %{buildroot}/usr/lib64/libpe.so

%if 0%{?rhel} && 0%{?rhel} <= 7
%ldconfig_scriptlets
%endif


%check


%files
%license LICENSE LICENSE.OpenSSL
%doc README.md
%{_bindir}/pe*
%{_bindir}/readpe
%{_bindir}/ofs2rva
%{_bindir}/rva2ofs
%{_libdir}/libpe.so.*
%{_libdir}/pev
%{_mandir}/man1/pe*.1.gz
%{_mandir}/man1/readpe*.1.gz
%{_mandir}/man1/ofs2rva*.1.gz
%{_mandir}/man1/rva2ofs*.1.gz
%{_datadir}/pev

#%%files devel
#%%{_includedir}/%%{name}.h
#%%{_includedir}/%%{name}/
#%%{_libdir}/*.so

%changelog
* Thu Nov 09 2023 Michal Ambroz <rebus at, seznam.cz> - 0.83-1
- initial build for Fedora Project
