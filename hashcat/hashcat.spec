Name:           hashcat
Version:        5.1.0
# Show as the RPM release number (keep same number line for tarball and git builds)
%global         baserelease     7

Summary:        Advanced password recovery utility

License: MIT and Public Domain
URL: https://hashcat.net/hashcat/
#    https://github.com/hashcat/hashcat/releases

# Specification of the used GIT commit
%global         gituser         hashcat
%global         gitname         hashcat
# Most recent, opencl strictly requires mesa and pocl is not installed
%global         commit          398e06878d6e36460bcd00283d847c723a162be3
%global         gitdate         20200220
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# By default build from official release
# leave option here to build from git snapshot instead
%bcond_without     snapshot

%if 0%{?with_snapshot}
#               not using 0. on the beginning of release as this git snapshot is past the 0.7.0 release
Release:        %{baserelease}.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%else
Release:        %{baserelease}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

# Patch is not needed:
# - debug/optimization options fixed by setting DEBUG=3
# - doc gets deleted in %%install part
# - bash completion installed explicitly in %%instal 
#Patch0:        0001-Fedora-build-patches.patch


BuildRequires:  bash-completion
BuildRequires:  opencl-headers
BuildRequires:  xxhash-devel
BuildRequires:  xz-devel
BuildRequires:  gcc

Requires:       bash-completion
%if 0%{?fedora}
Recommends:     mesa-libOpenCL%{?_isa}
Recommends:     %{name}-doc = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       bundled(zlib) = 1.2.11
# The version 1.1 from zlib/contrib from year cca 2010
Provides:       bundled(minizip) = 1.1

# Upstream does not support Big Endian architectures.
ExcludeArch:    ppc64 s390x

%description
Hashcat is the world's fastest and most advanced password recovery
utility, supporting five unique modes of attack for over 200
highly-optimized hashing algorithms. hashcat currently supports
CPUs, GPUs, and other hardware accelerators on Linux, Windows,
and Mac OS, and has facilities to help enable distributed password
cracking.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%package doc
Summary:        Documentation files for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description doc
%{summary}.

%prep
%if 0%{?with_snapshot}
# Build from git snapshot
%autosetup -p 1 -n %{gitname}-%{commit}
%else
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}
%endif

rm -rf deps/{OpenCL-Headers,xxHash}
sed -e 's/\.\/hashcat/hashcat/' -i *.sh
chmod -x *.sh

%build
%set_build_flags
echo "CFLAGS='$CFLAGS'"
# Not using the system zlib, because that one is not build with all the contribs.
# Hashcat is actually using minizip from zlib/contrib ... unmaintained since cca 2006
# TODO: migrate to new minizip package
%make_build PREFIX=%{_prefix} LIBRARY_FOLDER=%{_libdir} SHARED=1 DEBUG=3 USE_SYSTEM_ZLIB=0 USE_SYSTEM_OPENCL=1 USE_SYSTEM_XXHASH=1

%install
%make_install PREFIX=%{_prefix} LIBRARY_FOLDER=%{_libdir} SHARED=1 DEBUG=3 USE_SYSTEM_ZLIB=0 USE_SYSTEM_OPENCL=1 USE_SYSTEM_XXHASH=1
ln -s lib%{name}.so.%{version} "%{buildroot}%{_libdir}/lib%{name}.so"

# Take doc files directly from source
rm -rf %{buildroot}/usr/share/doc/hashcat

BASHCOMP_FOLDER=%{buildroot}%{_datadir}/bash-completion/completions
install -m 755 -d "$BASHCOMP_FOLDER"
install -m 644 extra/tab_completion/hashcat.sh "$BASHCOMP_FOLDER"/hashcat



%files
%license docs/license.txt
%doc README.md
%{_datadir}/bash-completion/completions/%{name}
%{_libdir}/lib%{name}.so.%{version}
%{_datadir}/%{name}
%{_bindir}/%{name}

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so

%files doc
%doc docs/{changes,contact,credits,limits,performance,readme,rules,status_codes,team,user_manuals}.txt
%doc charsets/ layouts/ masks/ rules/
%doc example.dict example*.sh

%changelog
* Fri Feb 21 2020 Michal Ambroz <rebus AT_ seznam.cz> - 5.1.0-7.20200220git398e068
- cond build from release or git snapshot
- get rid of the Makefile patch to simplify package upgrades
- snapshot version allows cracking of the KRB tickets type 18 - kerberoasting with AES

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 24 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-4
- Switched to regular build instead of debug.

* Mon Feb 18 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-3
- Fixed problem with dependencies on EPEL7.

* Thu Feb 07 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-2
- Moved documentation to a separate package.

* Wed Feb 06 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-1
- Initial SPEC release.
