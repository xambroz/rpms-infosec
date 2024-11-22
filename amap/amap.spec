Name:           amap
Version:        5.4
Release:        1%{?dist}
Summary:        Network tool for application protocol detection
Group:          Applications/System
License:        AMAP License
#License        AMAP non-commercial rules added to GPLv2
URL:            http://freeworld.thc.org/thc-amap/
Source0:        http://freeworld.thc.org/releases/%{name}-%{version}.tar.gz
Patch0:         %{name}-destdir.patch
Patch1:         %{name}-path.patch
Patch2:         %{name}-ldflags.patch
Patch3:         %{name}-new-homepage.patch
Patch4:         %{name}-system-pcre.patch
Patch5:         %{name}-optflags.patch
Patch6:         %{name}-lnamap6.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel

%description
THC Amap is a next-generation tool for assisting network penetration testing.
It performs fast and reliable application protocol detection, independent
on the TCP/UDP port they are being bound to.

%prep
%setup -q
%patch0 -p1 -b .0destdir
%patch1 -p1 -b .1path
%patch2 -p1 -b .2ldflags
#%patch3 -p1 -b .3homepage
%patch4 -p1 -b .4pcre
%patch5 -p1 -b .5optflags
%patch6 -p1 -b .6lnamap6

%build
#%%configure
./configure --prefix=%{_prefix} --libdir=%{_libdir}
OPT="$RPM_OPT_FLAGS" make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO LICENCE.AMAP LICENSE.GNU
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}

%changelog
* Fri May 23 2014 Michal Ambroz <rebus at, seznam.cz> 5.4-1
- bump to version 5.4

* Wed Nov 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.2-6
- Rebuilt

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 26 2010 Michal Ambroz <rebus at, seznam.cz> 5.2-4
- more flexible pcre cflags to build also on RHEL4

* Sun Mar 20 2010 Michal Ambroz <rebus at, seznam.cz> 5.2-3
- License changed to AMAP license to avoid confusion
- patch makefile to link to amap6 instead of copy


* Fri Jan 08 2010 Michal Ambroz <rebus at, seznam.cz> 5.2-2
- patched makefile & spec to honour RPM_OPT_FLAGS
- included verbatim copy of licenses
- RPM_OPT_FLAGS fixed build of debug package as well
- removed explicit dependency on openssl and pcre

* Tue Jan 05 2010 Michal Ambroz <rebus at, seznam.cz> 5.2-1
- Initial SPEC for Fedora 12 using SPEC and patches from PLD
- Original SPEC by luzik qboosh zbyniu baggins glen


