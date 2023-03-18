Name:           reglookup
Version:        1.0.1
Release:        1%{?dist}
License:        GPLv3
Summary:        Direct analysis of Windows NT-based registry files

URL:            http://projects.sentinelchicken.org/reglookup/
# Mirror        https://github.com/DonnchaC/coldboot-attacks

#               http://projects.sentinelchicken.org/reglookup/download/
Source0:        http://projects.sentinelchicken.org/data/downloads/reglookup-src-1.0.1.tar.gz

Patch0:         reglookup-destdir.patch
Patch1:         reglookup-docbook2man.patch

Buildrequires:  gcc
BuildRequires:  python3-scons
BuildRequires:  libtalloc
BuildRequires:  libtalloc-devel
BuildRequires:  python3-talloc
BuildRequires:  python3-talloc-devel
BuildRequires:  docbook2X



%description
The RegLookup project is devoted to direct analysis of Windows NT-based
registry files. RegLookup is released under the GNU GPL, and is implemented
in ANSI C. RegLookup provides command line tools, a C API, and a Python
module for accessing registry data structures. The project has a focus
on providing tools for digital forensic examiners (though is useful for
many purposes), and includes algorithms for retrieving deleted data
structures from registry hives. Browse the project's goals to read up
on the objectives of future releases.

%prep
%autosetup -n %{name}-src-%{version}


%build
%set_build_flags
PREFIX=%{_prefix} scons


%install
PREFIX=%{_prefix} DESTDIR=%{buildroot} MANDIR=%{_mandir} LIBDIR=%{_libdir} scons install

# Fedora doesn't distribute *.a
rm %{buildroot}%{_libdir}/libregfi.a



%files
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-recover
%{_bindir}/%{name}-timeline
%{_mandir}/man1/%{name}*.1*
%{_includedir}/regfi
%{_libdir}/libregfi.so
%{python3_sitelib}/pyregfi-1.0-py3.11.egg-info
%{python3_sitelib}/pyregfi


%changelog
* Fri Mar 17 2023 Michal Ambroz <rebus at, seznam.cz> - 1.0.1-1
- initial package

