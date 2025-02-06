Name:           afpfs-ng
Version:        0.8.1
Release:        %autorelease
Summary:        Apple Filing Protocol client


# by default build with the fuse module
# rpmbuild --rebuild afpfs-ng.src.rpm --without fuse
%bcond_without     fuse


License:        GPL-2.0-or-later
URL:            http://alexthepuffin.googlepages.com/home
Source0:        http://downloads.sourceforge.net/afpfs-ng/%{name}-%{version}.tar.bz2
Patch0:         afpfs-ng-0.8.1-overflows.patch
Patch1:         afpfs-ng-0.8.1-pointer.patch
# Sent by e-mail to Alex deVries <alexthepuffin@gmail.com>
Patch2:         afpfs-ng-0.8.1-formatsec.patch
Patch3:         afpfs-ng-0.8.1-longoptions.patch
Patch4:         afpfs-ng-0.8.1-c99.patch
Patch5:         afpfs-ng-0.8.1-pointer2.patch
Patch6:         afpfs-ng-0.8.1-tests.patch

%{?with_fuse:BuildRequires: fuse-devel}
BuildRequires: gcc
BuildRequires: libgcrypt-devel gmp-devel readline-devel
BuildRequires: make
BuildRequires: libtool
BuildRequires: autoconf


%description
A command line client to access files exported from Mac OS system via
Apple Filing Protocol.
%{?with_fuse:The FUSE filesystem module for AFP is in fuse-afp package}


%if 0%{?with_fuse}
%package -n fuse-afp
Summary:        FUSE driver for AFP filesystem

%description -n fuse-afp
A FUSE file system server to access files exported from Mac OS system
via AppleTalk or TCP using Apple Filing Protocol.
The command line client for AFP is in fuse-afp package
%endif


%package devel
Summary:        Development files for afpfs-ng
Requires:       %{name} = %{version}

%description devel
Library for dynamic linking and header files of afpfs-ng.

%prep
%autosetup -p 1
libtoolize
autoreconf

%build
# make would rebuild the autoconf infrastructure due to the following:
# Prerequisite `configure.ac' is newer than target `Makefile.in'.
# Prerequisite `aclocal.m4' is newer than target `Makefile.in'.
# Prerequisite `configure.ac' is newer than target `aclocal.m4'.
touch --reference aclocal.m4 configure.ac Makefile.in

export CFLAGS="${RPM_OPT_FLAGS} -fcommon -D NeedFunctionPrototypes"
%configure %{?!with_fuse:--disable-fuse} --disable-static
make %{?_smp_mflags}


%install
%make_install
install -d %{buildroot}%{_includedir}/afpfs-ng
cp -p include/* %{buildroot}%{_includedir}/afpfs-ng
# libtool .la file works different in different versions of libtool, should not be packaged
[ -f %{buildroot}%{_libdir}/libafpclient.la ] && rm -f %{buildroot}%{_libdir}/libafpclient.la

%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%ldconfig_scriptlets
%endif


%files
%license COPYING
%{_bindir}/afpcmd
%{_bindir}/afpgetstatus
%{_mandir}/man1/afpcmd.1*
%{_mandir}/man1/afpgetstatus.1*
%{_libdir}/libafpclient.so.*
%doc AUTHORS ChangeLog docs/README docs/performance docs/FEATURES.txt docs/REPORTING-BUGS.txt


%if 0%{?with_fuse}
%files -n fuse-afp
%license COPYING
%{_bindir}/afp_client
%{_bindir}/afpfs
%{_bindir}/afpfsd
%{_bindir}/mount_afp
%{_mandir}/man1/afp_client.1*
%{_mandir}/man1/afpfsd.1*
%{_mandir}/man1/mount_afp.1*
%doc AUTHORS ChangeLog
%endif


%files devel
%{_includedir}/afpfs-ng
%{_libdir}/*.so

%changelog
%autochangelog
