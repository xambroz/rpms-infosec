%define	debug_package		%{nil}
%define VirtualEnvironment      %{_prefix}/local/lib/PythonVirtualEnvironments/%{name}-%{version}
%define vpython %{venv}/bin/python
%define vpip    %{venv}/bin/pip


Name:		rekall-forensics
Version:	1.7.2.rc1
Release:	1%{?dist}
Summary:	Advanced forensic and incident response framework
Group:		Applications
License:	GPL3
Source:		%{name}-%{version}.tar.gz
URL:		http://www.rekall-forensic.com
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	readline-devel
Requires:	gcc-c++
Requires:	patch
%if 0%{?centos} == 8 || 0%{?rhel} == 8
Requires:	python3-virtualenv python3-devel
%endif
%if 0%{?centos} == 7
Requires:	python-virtualenv python36-devel
%endif
%if 0%{?fedora} >= 29
Requires:	python3-virtualenv python36 python3-devel
%endif
%if 0%{?fedora} == 26 || 0%{?fedora} == 27 || 0%{?fedora} == 28
Requires:	python2-virtualenv python3-devel
%endif
%if 0%{?fedora} == 24 || 0%{?fedora} == 25
Requires:	python2-virtualenv python3-devel redhat-rpm-config
%endif
%if 0%{?fedora} == 23
Requires:	python-virtualenv python3-devel redhat-rpm-config
%endif

%description
Rekall is an advanced forensic and incident response framework. While
it began life purely as a memory forensic framework, it has now evolved
into a complete platform.  Rekall implements the most advanced analysis
techniques in the field, while still being developed in the open, with a
free and open source license. Many of the innovations implemented within
Rekall have been published in peer reviewed papers .

Rekall provides an end-to-end solution to incident responders and forensic
analysts. From state of the art acquisition tools, to the most advanced
open source memory analysis framework.

%prep
echo Nothing to prep

%build
echo Nothing to build

%post
echo Building the Python Virtual Environment for Rekall. This will take a while. > /proc/$PPID/fd/1
mkdir -p %{VirtualEnvironment}
%if 0%{?fedora} >= 29
virtualenv --python=/usr/bin/python3.6 -q %{VirtualEnvironment}
%else
%if 0%{?centos} == 8 || 0%{?rhel} == 8
virtualenv-3 -q %{VirtualEnvironment}
%else
virtualenv -q %{VirtualEnvironment}
%endif
%endif
. %{VirtualEnvironment}/bin/activate
cp /dev/null /tmp/%{name}-%{version}-install.log
for p in pip future==0.16.0 pybindgen rekall
do
        echo -n Installing $p in the virtual environment ... > /proc/$PPID/fd/1
        pip install --upgrade "$p" >> /tmp/%{name}-%{version}-install.log 2>&1
        echo " Done" > /proc/$PPID/fd/1
done
echo Done building the Python Virtual Environment for Rekall. > /proc/$PPID/fd/1

%postun
rm -rf %{VirtualEnvironment}

%install
%__install -d %{buildroot}%{VirtualEnvironment}
%__install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/rekall.py << 'EOF'
#!/bin/sh
. %{VirtualEnvironment}/bin/activate
exec rekall "$@"
EOF

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%attr(755, root, root)	%{_bindir}/rekall.py

%changelog
* Mon Jun 10 2019 Lawrence R. Rogers <lrr@cert.org> 1.7.2.rc1-1
* Release 1.7.2.rc1-1
	Version 1.7.2.rc1

* Thu Jan  3 2019 Lawrence R. Rogers <lrr@cert.org> 1.7.1-1
* Release 1.7.1-1
	Initial release
