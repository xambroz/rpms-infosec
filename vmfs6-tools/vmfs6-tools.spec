%define with_doc 1
%define debug_package %{nil}
%define VMFS_VERSION 6

Name:               vmfs%{VMFS_VERSION}-tools
Version:            0.0.0.844.1195
Release:            1%{?dist}
Summary:            Tools to access VMFS filesystems
Source:             http://glandium.org/projects/vmfs-tools/vmfs%{VMFS_VERSION}-tools-%{version}.tar.gz
URL:                http://glandium.org/projects/vmfs-tools/
Group:              System/Filesystems
License:            GPL-2.0+
BuildRoot:          %{_tmppath}/build-%{name}-%{version}
BuildRequires:      libuuid-devel 
%if 0%{?centos} == 8
BuildRequires:      docbook-style-xsl
%else
BuildRequires:      docbook5-style-xsl
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

%package -n libvmfs%{VMFS_VERSION}-devel
Summary:            Library to access VMFS filesystems
Group:              Development/Libraries/C and C++

%description -n libvmfs%{VMFS_VERSION}-devel
Originally loosely based on the vmfs code from fluidOps, this set of tools has
since evolved to handle more features from VMFS, such as extents, and allows to
access VMFS through the standard Linux VFS with the help of the FUSE framework.

While it is still work in progress and is not destined for production use yet,
it can be of some help for some people.

%prep
%autosetup -p1

%build
%configure
%__make %{?_smp_flags}

%install
%make_install

pushd %{buildroot}%{_sbindir}
for f in *
do
	mv "$f" $(echo $f | sed s/vmfs/vmfs%{VMFS_VERSION}/)
done
popd

pushd %{buildroot}%{_mandir}/man8
for f in *
do
	nf=$(echo ${f%.*} | sed s/vmfs/vmfs%{VMFS_VERSION}/)
	sed --in-place -e s/${f%.*}/$nf/g -e "s/VMFS file system/VMFS %{VMFS_VERSION} file system/" -e "s/vmfs\\\\-fuse/vmfs%{VMFS_VERSION}\\\\-fuse/" -e s/vmfs-tools/vmfs%{VMFS_VERSION}-tools/ -e s/debugvmfs/debugvmfs%{VMFS_VERSION}/ $f
	mv "$f" $(echo $f | sed s/vmfs/vmfs%{VMFS_VERSION}/)
done
popd

%__chmod 0644 "%{buildroot}%{_mandir}/man8"/*.8

%__install -d "%{buildroot}%{_includedir}/libvmfs%{VMFS_VERSION}"
%__install -m0644 libvmfs/*.h "%{buildroot}%{_includedir}/libvmfs%{VMFS_VERSION}/"
%__install -D -m0644 libvmfs/libvmfs.a "%{buildroot}%{_libdir}/libvmfs%{VMFS_VERSION}.a"

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE TODO
%{_sbindir}/debugvmfs%{VMFS_VERSION}
%{_sbindir}/fsck.vmfs%{VMFS_VERSION}
%{_sbindir}/vmfs%{VMFS_VERSION}-fuse
%{_sbindir}/vmfs%{VMFS_VERSION}-lvm
%if %with_doc
%doc %{_mandir}/man8/debugvmfs%{VMFS_VERSION}.8*
%doc %{_mandir}/man8/fsck.vmfs%{VMFS_VERSION}.8*
%doc %{_mandir}/man8/vmfs%{VMFS_VERSION}-fuse.8*
%doc %{_mandir}/man8/vmfs%{VMFS_VERSION}-lvm.8*
%endif #with_doc

%files -n libvmfs%{VMFS_VERSION}-devel
%defattr(-,root,root)
%{_includedir}/libvmfs%{VMFS_VERSION}
%{_libdir}/libvmfs%{VMFS_VERSION}.a

%changelog
* Tue Jan 29 2019 Lawrence R. Rogers <lrr@cert.org> 0.0.0.844.1195-1
* Release 0.0.0.844.1195-1
	This version supports VMFS 6 Datastores
