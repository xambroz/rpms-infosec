%define with_doc 1
%define debug_package %{nil}
%define VMFS_VERSION 5

Name:               vmfs-tools
Version:            0.2.5
Release:            3%{?dist}
Summary:            Tools to access VMFS filesystems
Source:             http://glandium.org/projects/vmfs-tools/vmfs-tools-%{version}.tar.gz
Patch1:             vmfs-tools-uuid.patch
URL:                http://glandium.org/projects/vmfs-tools/
Group:              System/Filesystems
License:            GPL-2.0+
BuildRoot:          %{_tmppath}/build-%{name}-%{version}
%if 0%{?centos} == 5
BuildRequires:      uuid-devel 
BuildRequires:      docbook-style-xsl
%else
BuildRequires:      libuuid-devel 
%if 0%{?centos} == 8
BuildRequires:      docbook-style-xsl
%else
BuildRequires:      docbook5-style-xsl
%endif
%endif
BuildRequires:      fuse-devel
%if %with_doc
BuildRequires:      asciidoc
BuildRequires:      libxslt
%endif #with_doc
BuildRequires:      gcc make glibc-devel pkgconfig
BuildRequires:      autoconf automake libtool

%description
Originally loosely based on the vmfs code from fluidOps, this set of tools has
since evolved to handle more features from VMFS, such as extents, and allows to
access VMFS through the standard Linux VFS with the help of the FUSE framework.

While it is still work in progress and is not destined for production use yet,
it can be of some help for some people.

%package -n libvmfs-devel
Summary:            Library to access VMFS filesystems
Group:              Development/Libraries/C and C++

%description -n libvmfs-devel
Originally loosely based on the vmfs code from fluidOps, this set of tools has
since evolved to handle more features from VMFS, such as extents, and allows to
access VMFS through the standard Linux VFS with the help of the FUSE framework.

While it is still work in progress and is not destined for production use yet,
it can be of some help for some people.

%prep
%setup -q
%if 0%{?centos} != 5
%patch1 -p1
%endif

%build
%configure
%__make %{?_smp_flags}

%install
%makeinstall

pushd %{buildroot}%{_sbindir}
for f in *

do
        ln "$f" $(echo $f | sed s/vmfs/vmfs%{VMFS_VERSION}/)
done
popd

pushd %{buildroot}%{_mandir}/man8
for f in *
do
        ln "$f" $(echo $f | sed s/vmfs/vmfs%{VMFS_VERSION}/)
done
popd


%__chmod 0644 "%{buildroot}%{_mandir}/man8"/*.8

%__install -d "%{buildroot}%{_includedir}/libvmfs"
%__install -m0644 libvmfs/*.h "%{buildroot}%{_includedir}/libvmfs/"
%__install -D -m0644 libvmfs/libvmfs.a "%{buildroot}%{_libdir}/libvmfs.a"
pushd %{buildroot}%{_includedir}/
ln -s libvmfs libvmfs%{VMFS_VERSION}
popd
pushd %{buildroot}%{_libdir}
ln libvmfs.a libvmfs%{VMFS_VERSION}.a

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE TODO
%{_sbindir}/debugvmfs*
%{_sbindir}/fsck.vmfs*
%{_sbindir}/vmfs*-fuse
%{_sbindir}/vmfs*-lvm
%if %with_doc
%doc %{_mandir}/man8/debugvmfs*.8*
%doc %{_mandir}/man8/fsck.vmfs*.8*
%doc %{_mandir}/man8/vmfs*-fuse.8*
%doc %{_mandir}/man8/vmfs*-lvm.8*
%endif #with_doc

%files -n libvmfs-devel
%defattr(-,root,root)
%{_includedir}/libvmfs*
%{_libdir}/libvmfs*.a

%changelog
* Tue Jun 11 2019 Lawrence R. Rogers <lrr@cert.org> 0.2.5-3
* Release 0.2.5-3
	Made links so that the tools, documentation, header files, and libraries have an alias of vmfs5.

- Remove redundant tags/sections from specfile
* Sat May 26 2012 jengelh@inai.de
- Remove redundant tags/sections from specfile
* Mon May  7 2012 jeffm@suse.com
- Build fixes for libuuid-devel
* Wed Mar 23 2011 pascal.bleser@opensuse.org
- initial version (0.2.1)
