%global debug_package %{nil}

Name:          untex
Version:       1.3
Release:       3.1%{?dist}
Summary:       Command to strip LaTeX commands from input
Group:         Applications/Publishing
URL:           https://github.com/lukasdietrich/untex
Source:        ftp://ftp.thp.uni-duisburg.de/pub/source/%{name}-%{version}.tar.gz
License:       GPL
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
Like detex untex removes some LaTeX commands from the files listed in the
arguments (or standard input) and prints the output to standard output.
Has some alternative options, and the source code too, of course.

%prep
%setup -q

%build
make -j1

%install
rm -rf $RPM_BUILD_ROOT

install -D -m 755 untex $RPM_BUILD_ROOT%{_bindir}/untex
install -D -m 644 untex.man $RPM_BUILD_ROOT%{_mandir}/man1/untex.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/untex
%{_mandir}/man1/untex.*

%changelog
* Wed Jun 29 2011 Huaren Zhong <huaren.zhong@gmail.com> - 1.3
- Rebuild for Fedora

* Wed Dec 12 2007 Aleph0 <aleph0@openmamba.org> 1.3-2mamba
- fixed manpage name

* Wed Dec 28 2005 Alessandro Ramazzina <alessandro.ramazzina@qilinux.it> 1.3-1qilnx
- package created by autospec
