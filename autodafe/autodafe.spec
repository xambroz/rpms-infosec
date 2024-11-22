Summary:  Fuzzing framework
Name: autodafe
Version: 0.1
Release: 5%{?dist}
License: GPLv2+
Group: Development/Tools
URL: http://autodafe.sourceforge.net/ 
Source: http://downloads.sourceforge.net/autodafe/autodafe-%{version}.tar.gz
Patch1: autodafe.patch
Patch2: autodafe-0.1-cflags.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libxml2-devel >= 2.6.13
BuildRequires: gdb >= 6.2
BuildRequires: gcc >= 3.3.4
BuildRequires: perl >= 3.3.4
BuildRequires: bison
BuildRequires: flex

%description
Autodafé is a fuzzing framework able to uncover buffer overflows 
by using the fuzzing by weighting attacks with markers technique. 

%package doc
Summary:  Documentation of autodafe
Group:    Documentation
BuildArch:noarch

%description doc
This package contains tutorial to Autodafe

%prep
%setup -q
%patch1 -p1 -b .old
%patch2 -p1 -b .cflags
for i in README TUTORIAL; do iconv -f iso-8859-1 -t utf-8 < $i > $i.NEW && mv -f $i.NEW $i; done
cd docs; tar cfz tutorials.tgz tutorials

%build
%configure
make # do not use it in broken Makefile %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make prefix=$RPM_BUILD_ROOT/usr -C src/adbg install
make prefix=$RPM_BUILD_ROOT/usr -C src/adc install
make prefix=$RPM_BUILD_ROOT/usr -C src/autodafe install
make prefix=$RPM_BUILD_ROOT/usr -C src/pdml2ad install
( cd ./etc/generator; ./generator.sh . )
mv ./etc/generator/autodafe $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING AUTHORS FAQ TODO TUTORIAL BUGS
%dir %{_usr}/share/autodafe
%{_usr}/share/autodafe/*
%{_bindir}/adbg
%{_bindir}/adc
%{_bindir}/autodafe
%{_bindir}/pdml2ad

%files doc
%doc docs/tutorials.tgz

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Jan F. Chadima <jchadima@redhat.com> - 0.1-3
- support cflags from build environment

* Thu Jun 18 2009 Jan F. Chadima <jchadima@redhat.com> - 0.1-2
- reapired version

* Thu Jun 18 2009 Jan F. Chadima <jchadima@redhat.com> - 0.1-1
- initial version
