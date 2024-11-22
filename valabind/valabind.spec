%global         gituser         radare
%global         gitname         valabind
%global         commit          cd4051f6a7f63b297f3950c11a30f468351cbd69
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           valabind
Version:        0.9.2
Release:        2%{?dist}
Summary:        Transform vala or vapi files into swig, C++, NodeJS-ffi, or GIR
Group:          Applications/Engineering
License:        GPLv3+
URL:            https://github.com/radare/valabind
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRequires:  vala-devel

#Original package was planned to possibly co-exist in multiple versions
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Valabind is a tool to parse vala[1] or vapi files to transform them
into swig[2] interface files, C++, NodeJS-ffi or GIR.  With swig, you
can create language bindings for any API written in vala or C with a
vapi interface.  It can also generate bindings for C++.

%prep
%setup -qn %{gitname}-%{commit}

%build
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}"

%install
make install DESTDIR="%{buildroot}"

%files
%doc AUTHORS NOTES README.md TODO.md THANKS
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-cc
%{_mandir}/man1/*.1*

%changelog
* Sun Oct 18 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.9.2-2
- move the license to the new directory

* Sun Oct 11 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.9.2-1
- bump to 0.9.2

* Mon May 25 2015 Michal Ambroz <rebus AT_ seznam.cz> - 0.9.0-1
- bump to 0.9.0

* Tue Dec 17 2013 Eric Smith <spacewar@gmail.com> - 0.7.4-2
- Pass global_ldflags to make.

* Sat Nov 30 2013 Eric Smith <spacewar@gmail.com> - 0.7.4-1
- Initial version.
