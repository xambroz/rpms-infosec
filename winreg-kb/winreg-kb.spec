%define debug_package %{nil}
%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(plat_specific=False)")

%if 0%{?centos}0%{?amzn} == 70
%define python3_pkgversion 36
%endif

Summary:	winreg-kb - A project to build a Windows Registry Knowledge Base

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		winreg-kb
Version:	20190507
Release:	1%{?dist}

License:	ASL 2.0

Group:		Applications
Source:		%{name}-%{version}.tar.gz
URL:		https://github.com/libyal/winreg-kb/wiki

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}
Requires:       python%{python3_pkgversion}-crypto >= 2.6
Requires:       python%{python3_pkgversion}-dfdatetime >= 20180324
Requires:       python%{python3_pkgversion}-dfvfs >= 20181209
Requires:       python%{python3_pkgversion}-dfwinreg >= 20180712
Requires:       python%{python3_pkgversion}-dtfabric >= 20170524
Requires:       libbde-python%{python3_pkgversion} >= 20140531
Requires:       libewf-python%{python3_pkgversion} >= 20131210
Requires:	libfsapfs-python%{python3_pkgversion} >= 20181205
Requires:       libfsntfs-python%{python3_pkgversion} >= 20151130
Requires:       libfvde-python%{python3_pkgversion} >= 20160719
Requires:       libfwnt-python%{python3_pkgversion} >= 20160418
Requires:       libfwsi-python%{python3_pkgversion} >= 20150606
Requires:       libqcow-python%{python3_pkgversion} >= 20131204
Requires:       libregf-python%{python3_pkgversion} >= 20150315
Requires:       libsigscan-python%{python3_pkgversion} >= 20150627
Requires:       libsmdev-python%{python3_pkgversion} >= 20140529
Requires:       libsmraw-python%{python3_pkgversion} >= 20140612
Requires:       python%{python3_pkgversion}-pytsk3 >= 20160721
Requires:       libvhdi-python%{python3_pkgversion} >= 20131210
Requires:       libvmdk-python%{python3_pkgversion} >= 20140421
Requires:       libvshadow-python%{python3_pkgversion} >= 20160109
Requires:       libvslvm-python%{python3_pkgversion} >= 20160109
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

%description
winreg-kb is a project to build a Windows Registry Knowledge Base.

winregrc is a Python module part of winreg-kb to allow reuse of Windows
Registry Resources.

%prep
%setup 

%build
%py3_build

%install
mkdir -p %{buildroot}/%{_docdir}/%{name}
%py3_install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644, root, root, 0755)
%doc ACKNOWLEDGEMENTS AUTHORS LICENSE README
%attr(444, root, root)	%{python3_sitelib}/winregrc*egg-info
%attr(755, root, root)	%{python3_sitelib}/winregrc/
%attr(644, root, root)	%{_docdir}/%{name}/
%attr(644, root, root)	%{_docdir}/winregrc
%attr(755, root, root)	%{_bindir}/*

%exclude %{python3_sitelib}/*/__pycache__/*

%changelog
* Fri Feb  1 2019 Lawrence R. Rogers <lrr@cert.org> 20181223-2
* Release 20181223-2
        Version as of 20181223
	-python packages renamed to -python2

* Sun Dec 23 2018 Lawrence R. Rogers <lrr@cert.org> - 20181223-1
* Release 20181223-1
	Version from 20181223 and updated dependencies.

* Tue Aug  8 2017 Lawrence R. Rogers <lrr@cert.org> - 20170525-2
* Release 20170525-
	Rebuilt for new version of python-construct.

