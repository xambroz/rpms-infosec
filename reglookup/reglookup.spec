Name:           reglookup
Version:        1.0.1
Release:        2%{?dist}
License:        GPLv3
Summary:        Direct analysis of Windows NT-based registry files

%global         common_description %{expand:
The RegLookup project is devoted to direct analysis of Windows NT-based
registry files. RegLookup is released under the GNU GPL, and is implemented
in ANSI C. RegLookup provides command line tools, a C API, and a Python
module for accessing registry data structures. The project has a focus
on providing tools for digital forensic examiners (though is useful for
many purposes), and includes algorithms for retrieving deleted data
structures from registry hives. Browse the project's goals to read up
on the objectives of future releases.
}


URL:            http://projects.sentinelchicken.org/reglookup/
# Mirror        https://github.com/DonnchaC/coldboot-attacks

#               http://projects.sentinelchicken.org/reglookup/download/
Source0:        http://projects.sentinelchicken.org/data/downloads/reglookup-src-1.0.1.tar.gz

Patch0:         reglookup-destdir.patch
Patch1:         reglookup-docbook2man.patch
Patch2:         reglookup-soname.patch

Buildrequires:  gcc
BuildRequires:  libtalloc
BuildRequires:  libtalloc-devel
BuildRequires:  python%{python3_pkgversion}-scons
BuildRequires:  python%{python3_pkgversion}-talloc
BuildRequires:  python%{python3_pkgversion}-talloc-devel
BuildRequires:  docbook2X



%description
%{common_description}

# =================== devel package ================================
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%{common_description}


# =================== python bindings ==============================
%package -n python%{python3_pkgversion}-pyregfi
Summary:        Python3 binding for the regfi library from reglookup
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-pyregfi}

# Runtime dependencies

%description -n python%{python3_pkgversion}-pyregfi
This is a Python3 library that gives access to reglookup regfi library.
%{common_description}


%prep
%autosetup -n %{name}-src-%{version}


%build
%set_build_flags
PREFIX=%{_prefix} scons


%install
PREFIX=%{_prefix} DESTDIR=%{buildroot} MANDIR=%{_mandir} LIBDIR=%{_libdir} scons install

# Fedora doesn't distribute *.a
rm %{buildroot}%{_libdir}/libregfi.a

# Create missing .so link for the devel package
ln -s libregfi.so.%{version} %{buildroot}%{_libdir}/libregfi.so


%files
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-recover
%{_bindir}/%{name}-timeline
%{_mandir}/man1/%{name}*.1*
%{_libdir}/libregfi.so.*

%files devel
%license LICENSE
%{_includedir}/regfi
%{_libdir}/libregfi.so


%files -n python%{python3_pkgversion}-pyregfi
%license LICENSE
%{python3_sitelib}/pyregfi-1.0-py3.11.egg-info
%{python3_sitelib}/pyregfi


%changelog
* Sat Mar 18 2023 Michal Ambroz <rebus at, seznam.cz> - 1.0.1-2
- split devel,python package to comply with Fedora guidelines

* Fri Mar 17 2023 Michal Ambroz <rebus at, seznam.cz> - 1.0.1-1
- initial package

