%define	debug_package	%{nil}
%global _build_id_links	none

%if 0%{?centos} || 0%{?amzn}
%define __python                %(echo which python3 | scl enable rh-python38 -)
%else
%define __python                /usr/bin/python3
%endif

%if 0%{?centos}0%{?amzn} == 70
%define python3_pkgversion 36
%endif


%define	rel			3
%define VirtualEnvironment      %{name}-%{version}-%{rel}
%define VirtualEnvironmentPath  %{_prefix}/local/lib/PythonVirtualEnvironments

Name:		wdpassport-utils
Version:	0.2
Release:	%{rel}%{?dist}
Summary:	Lock, Unlock, and Manage Western Digital My Passport Drives
Group:		Applications
License:	GPL3
Source0:	%{name}-%{version}.tar.gz
URL:		https://github.com/0-duke/wdpassport-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?amzn}
BuildRequires:  rh-python36-python-virtualenv
BuildRequires:  rh-python38-python rh-python38-python-devel
BuildRequires:  rust
Requires:       rh-python38-python
%endif

%if 0%{?centos} == 8 || 0%{?rhel} == 8
BuildRequires:  python3-virtualenv python38-devel python38
%endif

%if 0%{?centos} == 9 || 0%{?rhel} == 9
BuildRequires:  python3-virtualenv python3-devel python3
%endif

%if 0%{?centos} == 7 && 0%{?amzn} == 0
BuildRequires:  python36-virtualenv
BuildRequires:  rh-python38-python rh-python38-python-devel
Requires:       rh-python38-python
%endif

%if 0%{?fedora}
BuildRequires:  python3-virtualenv python3-devel
%endif

Requires:	python%{python3_pkgversion}

%description
A Linux command-line utility to lock, unlock, and manage the hardware encryption functionality
of Western Digital My Passport external drives. Written in Python 3.

WD My Passport drives support hardware encryption. New drives arrive in a passwordless state ---
they can be used without locking or unlocking. After a password is set, drives become locked
when they are unplugged and must be unlocked when they are plugged in to mount the volume and
see its content.

This utlity can:

* Show drive status.
* Set and change the drive's password.
* Unlock an encrypted drive, given the password.
* Reset the drive in case of a lost password.
* Passwords given on the command line are converted into binary password data in a mechanism
  intended to be compatible with WD's unlock software that is used in Microsoft Windows.

This tool was originally written by 0-duke in 2015 based on reverse engineering research by
DanLukes and an implementation by DanLukes and KenMacD. crypto-universe converted this project
and the underlying SCSI interface library py_sg to Python 3. JoshData updated the library to
work with the latest WD My Passport device.

%prep
%setup

%setup -cT
sudo mkdir -p %{VirtualEnvironmentPath}
sudo chown %(id -u).%(id -g) %{VirtualEnvironmentPath}
cd %{VirtualEnvironmentPath}
rm -rf %{VirtualEnvironment}

%if 0%{?amzn}
echo virtualenv -p $(echo which python3.8 | scl enable rh-python38 -) %{VirtualEnvironment} | scl enable rh-python36 -
%endif

%if 0%{?centos}0%{?amzn} == 70
echo virtualenv-3 -p $(echo which python3 | scl enable rh-python38 -) %{VirtualEnvironment} | scl enable rh-python38 -
%endif

%if 0%{?centos} == 8
virtualenv-3 -p $(which python3.8) %{VirtualEnvironment}
%endif

%if 0%{?centos} == 9
virtualenv -p $(which python3) %{VirtualEnvironment}
%endif

%if 0%{?fedora}
virtualenv %{VirtualEnvironment}
%endif

cd %{VirtualEnvironment}
tar zxf %{SOURCE0}

%build
cd %{VirtualEnvironmentPath}/%{VirtualEnvironment}

for p in pip %{VirtualEnvironmentPath}/%{VirtualEnvironment}/%{name}-%{version}
do
        sh -c "source bin/activate;pip3 install --upgrade \"$p\""
done
chmod 755 bin/%{name}.py 

%install
%{__mkdir_p} %{buildroot}/%{VirtualEnvironmentPath}
cd %{VirtualEnvironmentPath}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/
install -m444 %{VirtualEnvironment}/%{name}-%{version}/LICENSE   %{buildroot}%{_docdir}/%{name}-%{version}
install -m444 %{VirtualEnvironment}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}-%{version}
rm -rf %{VirtualEnvironment}/%{name}-%{version}
find %{VirtualEnvironment} | cpio -pdm %{buildroot}/%{VirtualEnvironmentPath}

%__install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/sh
. %{VirtualEnvironmentPath}/%{VirtualEnvironment}/bin/activate
exec sudo %{VirtualEnvironmentPath}/%{VirtualEnvironment}/bin/%{name}.py "$@"
EOF
cd %{buildroot}%{_bindir}
ln %{name} %{name}.py


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%{VirtualEnvironmentPath}/%{VirtualEnvironment}
%attr(755, root, root)	%{VirtualEnvironmentPath}/%{VirtualEnvironment}/bin/%{name}.py
%attr(755, root, root)	%{_bindir}/%{name}
%attr(755, root, root)	%{_bindir}/%{name}.py
%{_docdir}/%{name}-%{version}

%changelog
* Thu Mar 31 2022 Lawrence R. Rogers <lrr@@cert.org> - 0.2-2
- Release 0.2-2
	Sets permissions on the executable

* Sat Mar 26 2022 Lawrence R. Rogers <lrr@@cert.org> - 0.2-2
- Release 0.2-2
	This version now builds the virtual environment at package building time, not at package installation time.

* Thu Sep  9 2021 Lawrence R. Rogers <lrr@@cert.org> - 0.2-1
- Release 0.2-1
	Initial release
	See https://github.com/0-duke/wdpassport-utils
