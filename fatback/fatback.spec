Name:           fatback
Version:        1.3
Release:        1%{?dist}
Summary:        A tool for recovering files from FAT file systems

Group:          Applications/System
License:        GPL+
URL:            https://sourceforge.net/projects/fatback/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  flex
BuildRequires:  flex-static

Requires(post):  info
Requires(preun): info

%description
Fatback is a forensic tool for undeleting files from Microsoft FAT file
systems. Fatback is different from other undelete tools in that it does
the following:
- Can undelete files automatically
- Supports Long File Names
- Supports FAT12, FAT16, and FAT32
- Powerful interactive mode
- Recursively undeletes deleted directories
- Recovers lost cluster chains
- Works with single partitions or whole disks

%prep
%setup -q
# Fix permissions of files
chmod -x AUTHORS COPYING NEWS README
chmod -x *.c *.h *.l *.y

%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -rf %{buildroot}%{_infodir}/dir

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%doc AUTHORS COPYING NEWS README
%{_mandir}/man?/*.*
%{_infodir}/%{name}-manual.info.gz
%{_bindir}/%{name}

%changelog
* Sun Mar 27 2011 Fabian Affolter <fabian@bernewireless.net> - 1.3-1
- Initial package for Fedora
