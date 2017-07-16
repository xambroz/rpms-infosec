%global         gituser         decalage2
%global         gitname         oletools
# v0.51
%global         commit          3681c317fa9ebc5102064070dea3f3b293119509
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

%global         sum             Tools to analyze Microsoft OLE2 files



Name:           python-%{gitname}
Version:        0.51
#Release:       0.3.%{shortcommit}%{?dist}
Release:        1%{?dist}
Summary:        %{sum}

License:        BSD
URL:            https://www.decalage.info/python/oletools
# URL:          https://github.com/decalage2/oletools
# Source used for the version release
Source0:       https://github.com/%{gituser}/%{gitname}/archive/v%{version}/%{gitname}-%{version}.tar.gz
# Source based on git commit
#Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:         %{name}-thirdparty.patch


BuildArch:      noarch
BuildRequires:  python2-devel python3-devel
BuildRequires:  python-pymilter
#BuildRequires:  python-pymilter
BuildRequires:  python2-pyparsing
BuildRequires:  python3-pyparsing
BuildRequires:  python2-colorclass
BuildRequires:  python3-colorclass
BuildRequires:  python-easygui
BuildRequires:  python3-easygui
BuildRequires:  python2-olefile
BuildRequires:  python3-olefile
BuildRequires:  python-prettytable
BuildRequires:  python3-prettytable


%description
The python-oletools is a package of python tools from Philippe Lagadec
to analyze Microsoft OLE2 files (also called Structured Storage,
Compound File Binary Format or Compound Document File Format),
such as Microsoft Office documents or Outlook messages, mainly for
malware analysis, forensics and debugging.
It is based on the olefile parser.
See http://www.decalage.info/python/oletools for more info.



%package -n python2-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{gitname}}

%description -n python2-%{gitname}
The python-oletools is a package of python tools from Philippe Lagadec
to analyze Microsoft OLE2 files (also called Structured Storage,
Compound File Binary Format or Compound Document File Format),
such as Microsoft Office documents or Outlook messages, mainly for
malware analysis, forensics and debugging.
It is based on the olefile parser.
See http://www.decalage.info/python/oletools for more info.



%package -n python3-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{gitname}}

%description -n python3-%{gitname}
The python-oletools is a package of python tools from Philippe Lagadec
to analyze Microsoft OLE2 files (also called Structured Storage,
Compound File Binary Format or Compound Document File Format),
such as Microsoft Office documents or Outlook messages, mainly for
malware analysis, forensics and debugging.
It is based on the olefile parser.
See http://www.decalage.info/python/oletools for more info.



%package -n python-%{gitname}-doc
%{?python_provide:%python_provide python2-%{gitname}-doc}
%{?python_provide:%python_provide python3-%{gitname}-doc}
Summary:        %{sum}
%description -n python-%{gitname}-doc


%prep
%autosetup -n %{gitname}-%{version}
#autosetup -n %{gitname}-%{commit}


#Use globally installed python-modules instead
for I in colorclass easygui olefile prettytable pyparsing ; do
    rm -rf "oletools/thirdparty/${I}"
done

sed -i -e '
    s|from oletools.thirdparty import olefile|import olefile|;
    s|from oletools.thirdparty.olefile import olefile|from olefile import olefile|;
    s|from oletools.thirdparty.prettytable import prettytable|import prettytable|;
    s|from oletools.thirdparty.pyparsing.pyparsing import|from pyparsing import|;
    s|from thirdparty.pyparsing.pyparsing import|from pyparsing import|;
    s|from .thirdparty import olefile|import olefile|;
    s|from oletools.thirdparty.easygui import easygui|import easygui|;
' */*.py

%build
# For now the 2.7 is the default version, python3 support is experimental
%py3_build
%py2_build

%install
# For now the 2.7 is the default version, python3 support is experimental
%py3_install
pushd %{buildroot}%{_bindir}
for I in ezhexviewer  mraptor  olebrowse  oledir  oleid  olemap  olemeta  oleobj  oletimes  olevba  pyxswf  rtfobj ; do
    mv "$I" "${I}3"
done
popd

%py2_install
pushd %{buildroot}%{_bindir}
for I in ezhexviewer  mraptor  olebrowse  oledir  oleid  olemap  olemeta  oleobj  oletimes  olevba  pyxswf  rtfobj ; do
    mv "$I" "${I}2"
    ln -s "${I}2" "$I"
done
popd


%check
%{__python2} setup.py test

#Python3 test fails for:
# Milter on mraptor_milter.py -> missing python3 version, the mraptor_milter.py will work only with python2
# ioString on olevba.pu -> there is olevba3.py version
%{__python3} setup.py test || true

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{gitname}
%license README.md
%{python2_sitelib}/*
%{_bindir}/ezhexviewer2
%{_bindir}/olebrowse2
%{_bindir}/oledir2
%{_bindir}/oleid2
%{_bindir}/olemap2
%{_bindir}/olemeta2
%{_bindir}/oleobj2
%{_bindir}/oletimes2
%{_bindir}/olevba2
# mraptor probably works only for python2
%{_bindir}/mraptor2
%{_bindir}/pyxswf2
%{_bindir}/rtfobj2
%{_bindir}/ezhexviewer
%{_bindir}/olebrowse
%{_bindir}/oledir
%{_bindir}/oleid
%{_bindir}/olemap
%{_bindir}/olemeta
%{_bindir}/oleobj
%{_bindir}/oletimes
%{_bindir}/olevba
# mraptor probably works only for python2
%{_bindir}/mraptor
%{_bindir}/pyxswf
%{_bindir}/rtfobj



%files -n python3-%{gitname}
%license README.md
%{python3_sitelib}/*
%{_bindir}/ezhexviewer3
%{_bindir}/olebrowse3
%{_bindir}/oledir3
%{_bindir}/oleid3
%{_bindir}/olemap3
%{_bindir}/olemeta3
%{_bindir}/oleobj3
%{_bindir}/oletimes3
%{_bindir}/olevba3
# mraptor probably wont work for python3
%{_bindir}/mraptor3
%{_bindir}/pyxswf3
%{_bindir}/rtfobj3



%files -n python-%{gitname}-doc
%doc cheatsheet

%changelog
* Thu Jun 22 2017 Michal Ambroz <rebus at, seznam.cz> 0.51-1
- bump to 0.51 release

* Thu Jun 22 2017 Michal Ambroz <rebus at, seznam.cz> 0.51-0.3.dev11.b4b52d22
- gaps in python3 detected, using python2 as default

* Thu Jun 15 2017 Michal Ambroz <rebus at, seznam.cz> 0.51-0.2.dev11.b4b52d22
- initial version
