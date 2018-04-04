Name:           python-olefile
Version:        0.45.1
License:        BSD
# URL:          https://github.com/decalage2/olefile
URL:            https://www.decalage.info/olefile


%global         gituser         decalage2
%global         gitname         olefile
%global         gitdate         20180126
%global         commit          93d0bde9115f4d3c54ea83c66b631afd1e741bc7
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         sum             Tools to analyze Microsoft OLE2 files
Summary:        %{sum}


# Build source is tarball release=1 or git commit=0
%global         build_release    1

%if 0%{?build_release}  > 0
# Build from the targball release
Release:        1%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%else
# Build from the git commit snapshot
Release:        1.%{gitdate}git%{shortcommit}%{?dist}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif #build_release


BuildArch:      noarch
BuildRequires:  python2-devel

BuildRequires:  python%{python3_pkgversion}-devel
# needed to generate documentation man-page
BuildRequires:  python-sphinx


%description
The olefile is a Python package from Philippe Lagadec (decalage2)
to parse, read and write Microsoft OLE2 files (also called Structured
Storage, Compound File Binary Format or Compound Document File
Format), such as Microsoft Office 97-2003 documents, vbaProject.bin
in MS Office 2007+ files, Image Composer and FlashPix files, Outlook
messages, StickyNotes, several Microscopy file formats,
McAfee antivirus quarantine files, etc.
See http://www.decalage.info/olefile for more info.



%package -n python2-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{gitname}}

%description -n python2-%{gitname}
The olefile is a Python package from Philippe Lagadec (decalage2)
to parse, read and write Microsoft OLE2 files (also called Structured
Storage, Compound File Binary Format or Compound Document File
Format), such as Microsoft Office 97-2003 documents, vbaProject.bin
in MS Office 2007+ files, Image Composer and FlashPix files, Outlook
messages, StickyNotes, several Microscopy file formats,
McAfee antivirus quarantine files, etc.
See http://www.decalage.info/olefile for more info.



%package -n python%{python3_pkgversion}-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}


%description -n python%{python3_pkgversion}-%{gitname}
The olefile is a Python package from Philippe Lagadec (decalage2)
to parse, read and write Microsoft OLE2 files (also called Structured
Storage, Compound File Binary Format or Compound Document File
Format), such as Microsoft Office 97-2003 documents, vbaProject.bin
in MS Office 2007+ files, Image Composer and FlashPix files, Outlook
messages, StickyNotes, several Microscopy file formats,
McAfee antivirus quarantine files, etc.
See http://www.decalage.info/olefile for more info.


%prep
# Build from tarball release version
%if 0%{?build_release} > 0
%autosetup -p 1 -n %{gitname}-%{version}

%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif



%build
%py2_build
pushd doc
make man
popd
%py3_build

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%py3_install

install -D -m644 doc/_build/man/olefile.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check
%{__python2} setup.py test
%{__python3} setup.py test

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{gitname}
%license LICENSE.txt
%{python2_sitelib}/*


%files -n python%{python3_pkgversion}-%{gitname}
%license LICENSE.txt
%doc README.html README.rst
%{python3_sitelib}/*
%{_mandir}/man1/%{name}.1*



%changelog
* Wed Apr 04 2018 Michal Ambroz <rebus at, seznam.cz> 0.45.1-1
- bump to 0.45.1 release

* Thu Jun 15 2017 Michal Ambroz <rebus at, seznam.cz> 0.45-0.3.dev1.53c619f4
- update from git

* Thu Jun 15 2017 Michal Ambroz <rebus at, seznam.cz> 0.45-0.2.dev1.53c619f4
- initial version
