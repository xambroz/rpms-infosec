Name:           xmount
Version:        0.6.0
Release:        1%{?dist}
Summary:        A on-the-fly convert for multiple hard disk image types

Group:          Applications/Multimedia
License:        GPL-3.0-or-later
URL:            https://www.pinguin.lu/index.php
Source0:        http://files.pinguin.lu/projects/%{name}-%{version}.tar.gz
Patch1:         %{name}-ewf.patch

BuildRequires:  fuse-devel
BuildRequires:  libewf-devel
BuildRequires:  afflib-devel

Provides:       bundled(md5-deutsch)

%description
xmount allows you to convert on-the-fly between multiple input
and output hard disk image types. xmount creates a virtual file
system using FUSE (Filesystem in Userspace) that contains a virtual
representation of the input image. The virtual representation can
be in raw DD, VirtualBox's virtual disk file format or in VmWare's
VMDK file format. Input images can be raw DD, EWF (Expert Witness
Compression Format) or AFF (Advanced Forensic Format) files. In
addition, xmount also supports virtual write access to the output
files that is redirected to a cache file. This makes it possible
to boot acquired hard disk images using QEMU, KVM, VirtualBox,
VmWare, or alike.

%prep
%setup -q
%patch1 -p 1
%if 0%{?rhel} != 5
autoreconf
%endif


%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

%files
%doc AUTHORS ChangeLog COPYING NEWS README ROADMAP
%{_mandir}/man*/%{name}*.*
%{_bindir}/%{name}

%changelog
* Tue Aug 19 2014 Michal Ambroz <rebus _AT seznam.cz> - 0.6.0-1
- Update for new upstream version 0.6.0
- enable build with newer ewf library

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-4
- Rebuilt for libewf

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 02 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.0-2
- Clean section removed
- BR updated

* Mon Aug 06 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.0-1
- Added a provide
- Permissions were fixed upstream 
- Updated to new upstream version 0.5.0

* Sat Jun 30 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.4.7-2
- Leave md5 implementation in place

* Fri Apr 13 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.4.7-1
- Updated to new upstream version 0.4.7

* Tue Oct 18 2011 Fabian Affolter <mail@fabian-affolter.ch> - 0.4.6-1
- Updated to new upstream version 0.4.6

* Wed Sep 01 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.4.2-2
- Added patch from #606073
- Fixed permission
- Added needed BRs

* Mon Mar 15 2010 Fabian Affolter <mail@fabian-affolter.ch> - 0.4.2-1
- Initial package for Fedora
