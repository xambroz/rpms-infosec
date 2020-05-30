Name:           wmi
Summary:        WMI client for Linux

Version:        1.3.14
Release:        9%{?dist}
Group:          System Environment/Libraries
License:        GPL
Source:         http://www.openvas.org/download/wmi/%{name}-%{version}.tar.bz2
Patch1:         http://www.openvas.org/download/wmi/openvas-wmi-%{version}.patch
Patch2:         http://www.openvas.org/download/wmi/openvas-wmi-%{version}.patch2
Patch3:         http://www.openvas.org/download/wmi/openvas-wmi-%{version}.patch3v2
Patch4:         http://www.openvas.org/download/wmi/openvas-wmi-%{version}.patch4
Patch5:         http://www.openvas.org/download/wmi/openvas-wmi-%{version}.patch5
Patch6:         openvas-wmi-gnutls.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: autoconf
BuildRequires: gcc
BuildRequires: make
BuildRequires: git
BuildRequires: gtk+-devel
BuildRequires: gtk3-devel
BuildRequires: GConf2-devel
BuildRequires: libblkid-devel
BuildRequires: compat-openssl10-devel
BuildRequires: gnutls-devel


%description
WMI client and libraries.

%prep
%autosetup -S git

#fix Can’t use ‘defined(@array)’ at ./pidl/pidl line 583.
sed -i -e '583d' Samba/source/pidl/pidl

# create the pkgconfig
%{__cat} <<EOF > wmiclient.pc

prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_prefix}/lib
includedir=%{_prefix}/include

Name: wmiclient
Description: wmiclient library for OpenVAS
 Version: 1.3.14
 Requires:
Cflags: -I%{_includedir} -I%{_includedir}/openvas
Libs: -L%{_prefix}/lib
EOF


%build

cd Samba/source
./autogen.sh
#./configure --with-setproctitle --with-pthread --with-python=/usr/bin/python2 --enable-gnutls
./configure --enable-debug
make proto all "CPP=gcc -E -ffreestanding"
make libraries "CPP=gcc -E -ffreestanding"

# Cleanup linking
pushd wmi
  ln -sf libwmiclient.so.1 libwmiclient.so
popd

%install
make "DESTDIR=${RPM_BUILD_ROOT}/%{_prefix}/" install

mkdir -p  $RPM_BUILD_ROOT/%{_prefix}/lib/
mkdir -p  $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig
%{__install} -m 0644 wmiclient.pc $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/wmiclient.pc
%{__install} -m 0755 Samba/source/wmi/libwmiclient.so.1 $RPM_BUILD_ROOT/%{_prefix}/lib/libwmiclient.so.1
%{__install} -m 0755 Samba/source/wmi/libwmiclient.so $RPM_BUILD_ROOT/%{_prefix}/lib/libwmiclient.so

# Fix duplicities
rm -f $RPM_BUILD_ROOT/%{_prefix}/lib/python/libasync_wmi_lib.so.0
ln -s %{_prefix}/lib/python/libasync_wmi_lib.so.0.0.1 $RPM_BUILD_ROOT/%{_prefix}/lib/python/libasync_wmi_lib.so.0
rm -f $RPM_BUILD_ROOT/%{_prefix}/lib/libwmiclient.so
ln -s %{_prefix}/lib/libwmiclient.so.1 $RPM_BUILD_ROOT/%{_prefix}/lib/libwmiclient.so


%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/winexe
%{_bindir}/wmic
%{_prefix}/lib/python/libasync_wmi_lib.so.*
%{_prefix}/lib/python/pysamba/*
%{_prefix}/lib/pkgconfig/wmiclient.pc
%{_prefix}/lib/libwmiclient.so*


%changelog
* Sun May 20 2020 Michal Ambroz <rebus _AT seznam.cz> 1.3.14-9
- rebuild for fedora 32

* Wed Sep 19 2018 Michal Ambroz <rebus _AT seznam.cz> 1.3.14-8
- rebuild for fedora 28

* Wed Sep 02 2015 John Prause <jprause@redhat.com> 1.3.13-6
- Fix issue with macro

* Tue Sep 01 2015 John Prause <jprause@redhat.com> 1.3.13-5
- Fix issue with Release param

* Tue Sep 01 2015 John Prause <jprause@redhat.com> 1.3.13-4
- Fix issue lib and bin paths

* Thu Aug 27 2015 John Prause <jprause@redhat.com> 1.3.13-3
- Fix issue with spec which caused prior build failure

* Wed Aug 26 2015 John Prause <jprause@redhat.com> 1.3.13-2
- Update to rhel7

* Mon Mar 16 2015 Joe VLcek <jvlcek@redhat.com> 1.3.13-1
- Initial build
