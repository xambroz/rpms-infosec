%define debug_package %{nil}
%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(plat_specific=False)")

%if 0%{?centos}0%{?amzn} == 70
%define python3_pkgversion 36
%endif

Summary:	winevt-kb - Windows Event Log Knowledge Base
Packager:	Lawrence R. Rogers (lrr@cert.org)
Vendor:		cert.org
Name:		winevt-kb
Version:	20190507
Release:	1%{?dist}
License:	ASL 2.0
Group:		Applications
Source:		%{name}-%{version}.tar.gz
URL:		https://github.com/libyal/winevt-kb/wiki

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}
Requires:	libbde-python%{python3_pkgversion} >= 20140531
Requires:	libewf-python%{python3_pkgversion} >= 20131210
Requires:	libexe-python%{python3_pkgversion} >= 20131229
Requires:	libfsntfs-python%{python3_pkgversion} >= 20151130
Requires:	libfvde-python%{python3_pkgversion} >= 20160719
Requires:	libfwnt-python%{python3_pkgversion} >= 20160418
Requires:	libqcow-python%{python3_pkgversion} >= 20131204
Requires:	libregf-python%{python3_pkgversion} >= 20150315
Requires:	libsigscan-python%{python3_pkgversion} >= 20150627
Requires:	libsmdev-python%{python3_pkgversion} >= 20140529
Requires:	libsmraw-python%{python3_pkgversion} >= 20140612
Requires:	libvhdi-python%{python3_pkgversion} >= 20131210
Requires:	libvmdk-python%{python3_pkgversion} >= 20140421
Requires:	libvshadow-python%{python3_pkgversion} >= 20160109
Requires:	libvslvm-python%{python3_pkgversion} >= 20160109
Requires:	libwrc-python%{python3_pkgversion} >= 20140128
Requires:	python%{python3_pkgversion}-construct >= 2.5.2
Requires:	python%{python3_pkgversion}-crypto >= 2.6.0
Requires:	python%{python3_pkgversion}-dfdatetime >= 20160814
Requires:	python%{python3_pkgversion}-dfvfs >= 20160803
Requires:	python%{python3_pkgversion}-dfwinreg >= 20170301
Requires:	python%{python3_pkgversion}-pytsk3 >= 20160721
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

%description
winevt-kb is a project to build a Windows Event Log knowledge base.

winevtrc is a Python module part of winevt-kb to allow reuse of Windows Event Log resources.

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
%attr(444, root, root)	%{python3_sitelib}/winevtrc*egg-info
%attr(755, root, root)	%{python3_sitelib}/winevtrc/
%attr(644, root, root)	%{_docdir}/%{name}/
%attr(644, root, root)	%{_docdir}/winevtrc
%attr(755, root, root)	%{_bindir}/*

%exclude %{python3_sitelib}/*/__pycache__/*

%changelog
* Tue May  7  2019 Lawrence R. Rogers <lrr@cert.org> 20190507-1
* Release 20190507-1
	Version from 20190507 - built using Python 3 only

* Fri Feb  1 2019 Lawrence R. Rogers <lrr@cert.org> 20181223-2
* Release 20181223-2
        Version as of 20181223
	-python packages renamed to -python2

* Sun Dec 23 2018 Lawrence R. Rogers <lrr@cert.org> 20181223-1
* Release 20181223-1
	Version 20181223
	Changed dependencies (pytsk3, dfwinreg, dfvfs
