Name:           python-olefile
Version:        0.47
Release:        %autorelease
Summary:        Python package to parse, read and write Microsoft OLE2 files

%global         srcname         olefile
%global         _description    %{expand:
olefile is a Python package to parse, read and write Microsoft OLE2 files
(also called Structured Storage, Compound File Binary Format or Compound
Document File Format), such as Microsoft Office 97-2003 documents,
vbaProject.bin in MS Office 2007+ files, Image Composer and FlashPix files,
Outlook messages, StickyNotes, several Microscopy file formats, McAfee
antivirus quarantine files, etc.
}

License:        BSD-2-Clause
URL:            https://github.com/decalage2/olefile
# was           https://www.decalage.info/olefile
#               https://pypi.python.org/pypi/olefile/
#               https://github.com/decalage2/olefile/releases
Source0:        %{pypi_source olefile %version zip}

# Build without python2 package for newer releases > fc32 and > rhel8
# python2 package already released for rhel8
# https://pagure.io/fesco/issue/2266
%if (0%{?fedora} && 0%{?fedora} > 33 ) || ( 0%{?rhel} && 0%{?rhel} > 8 ) || 0%{?flatpak}
%bcond_with     python2
%else
%bcond_without  python2
%endif


BuildArch:      noarch
BuildRequires:  make
BuildRequires:  dos2unix
BuildRequires:  /usr/bin/find

%description %{_description}

%package doc
Summary:        %{summary}
BuildArch:      noarch

# Generate documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%description doc %{_description}
This package contains documentation for %{name}.


%if 0%{?with_python2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{_description}
Python2 version.
%endif


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
#BuildRequires:  python%%{python3_pkgversion}-sphinx_rtd_theme
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname} %{_description}
Python3 version.


%prep
%autosetup -p1 -n %{srcname}-%{version}

# Fix windows EOL
find ./ -type f -name '*.py' -exec dos2unix '{}' ';'
dos2unix doc/*.rst


%if (0%{?fedora} && 0%{?fedora} > 33 ) || ( 0%{?rhel} && 0%{?rhel} > 8 ) || 0%{?flatpak}
%generate_buildrequires
%pyproject_buildrequires
%endif


%build
%if 0%{?with_python2}
%py2_build
%endif

%pyproject_wheel

make -C doc html BUILDDIR=_doc_build SPHINXBUILD=sphinx-build



%install
%if 0%{?with_python2}
%py2_install
%endif

%pyproject_install
%pyproject_save_files -l olefile



%check
# Tests got left out in the 0.44 source archive
# https://github.com/decalage2/olefile/issues/56
%if 0%{?with_python2}
PYTHONPATH=%{buildroot}%{python2_sitelib} %{__python2} tests/test_olefile.py
%endif

PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} tests/test_olefile.py


%files doc
%doc doc/_doc_build/html


%if 0%{?with_python2}
%files -n python2-%{srcname}
%doc README.md
%license doc/License.rst
%{python2_sitelib}/olefile-*.egg-info
%{python2_sitelib}/olefile/
%endif

%files -n python%{python3_pkgversion}-%{srcname}  -f %{pyproject_files}
%doc README.md
%license doc/License.rst


%changelog
%autochangelog
