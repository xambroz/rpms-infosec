Name:           scapy
Version:        2.6.0
Release:        %autorelease
Summary:        Interactive packet manipulation tool and network scanner

%global         gituser         secdev
%global         gitname         scapy
%global         commit          9473f77d8b548c8e478e52838bdd4c12f5d4f4ff
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

License:        GPL-2.0-only
URL:            https://scapy.net/
#was            http://www.secdev.org/projects/scapy/
VCS:            https://github.com/secdev/scapy
#               https://github.com/secdev/scapy/releases
#               https://bitbucket.org/secdev/scapy/pull-request/80
#               https://scapy.readthedocs.io/en/latest/introduction.html
Source0:        %{vcs}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global         common_desc %{expand:
Scapy is a powerful interactive packet manipulation program built on top
of the Python interpreter. It can be used to forge or decode packets of
a wide number of protocols, send them over the wire, capture them, match
requests and replies, and much more.}


# By default build with python3 subpackage
%bcond_without     python3

# Build also the python2 package on releases up to fc31 and rhel8
%if (0%{?fedora} && 0%{?fedora} <= 31 ) || ( 0%{?rhel} && 0%{?rhel} <= 8 )
%bcond_without     python2
%else
%bcond_with        python2
%endif

# By default build the documentation only on Fedora due to cc-by-nc-sa license
%if 0%{?fedora}
%bcond_without     doc
%else
%bcond_with        doc
%endif




BuildArch:      noarch

BuildRequires:  make
BuildRequires:  sed

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with doc}
BuildRequires:  python2-tox
%endif
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with doc}
BuildRequires:  python%{python3_pkgversion}-tox
%endif
%endif

# Recommends only supported on fedora and rhel8+
%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
Recommends:     tcpdump
# Using database of manufactures /usr/share/wireshark/manuf
Recommends:     wireshark-cli
%endif

%description %{common_desc}

%if %{with python2}
%package -n python2-%{name}
Summary:        Interactive packet manipulation tool and network scanner

%{?python_provide:%python_provide python2-%{name}}

%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 ) 
Recommends:     python2-pyx
Recommends:     python2-matplotlib
Recommends:     ipython2
%endif

%description -n python2-%{name}
%{common_desc}

%endif


%if %{with python3}
%package -n python%{python3_pkgversion}-%{name}
Summary:        Interactive packet manipulation tool and network scanner

%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
Provides:       %{name} = %{version}-%{release}

%if (0%{?fedora}) || ( 0%{?rhel} && 0%{?rhel} >= 8 ) 
Recommends:     PyX
Recommends:     python%{python3_pkgversion}-matplotlib
Recommends:     ipython3
%endif

%description -n python%{python3_pkgversion}-%{name}
%{common_desc}
%endif

%if %{with doc}
%package doc
Summary:        Interactive packet manipulation tool and network scanner
License:        CC-BY-NC-SA-2.5

BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme

%description doc
%{common_desc}
%endif



%prep
%autosetup -p 1 -n %{name}-%{version}

# Remove shebang
# https://github.com/secdev/scapy/pull/2332
SHEBANGS=$(find ./scapy -name '*.py' -print | xargs grep -l -e '^#!.*env python')
for FILE in $SHEBANGS ; do
    sed -i.orig -e 1d "${FILE}"
    touch -r "${FILE}.orig" "${FILE}"
    rm "${FILE}.orig"
done



%build
%if %{with python2}
%py2_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
make -C doc/scapy html BUILDDIR=_build_doc SPHINXBUILD=sphinx-build-%python3_version

rm -f doc/scapy/_build_doc/html/.buildinfo
rm -f doc/scapy/_build_doc/html/_static/_dummy
%endif



%install
install -dp -m0755 %{buildroot}%{_mandir}/man1
install -Dp -m0644 doc/scapy.1* %{buildroot}%{_mandir}/man1/

%if %{with python2}
%py2_install
rm -f %{buildroot}%{python2_sitelib}/*egg-info/requires.txt


# Rename the executables
mv -f %{buildroot}%{_bindir}/scapy   %{buildroot}%{_bindir}/scapy2

%if ! %{with python3}
# Link the default to the py2 version of executables if py3 not built
ln -s %{_bindir}/scapy2   %{buildroot}%{_bindir}/scapy
%endif
%endif

%if %{with python3}
%py3_install
rm -f %{buildroot}%{python3_sitelib}/*egg-info/requires.txt

# Rename the executables
mv -f %{buildroot}%{_bindir}/scapy   %{buildroot}%{_bindir}/scapy3

# Link the default to the python3 version of executables
ln -s %{_bindir}/scapy3   %{buildroot}%{_bindir}/scapy
%endif



# check
# TODO: Need to fix/remove slow/failed test
# cd test/
# ./run_tests_py2 || true
# ./run_tests_py3 || true



%if %{with python2}
%files -n python2-%{name}
%license LICENSE
%if ! %{with python3}
%doc %{_mandir}/man1/scapy.1*
%{_bindir}/scapy
%endif
%{_bindir}/scapy2
%{python2_sitelib}/scapy/
%{python2_sitelib}/scapy-*.egg-info
%exclude %{python2_sitelib}/test/
%endif



%if %{with python3}
%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc %{_mandir}/man1/scapy.1*
%{_bindir}/scapy
%{_bindir}/scapy3
%{python3_sitelib}/scapy/
%{python3_sitelib}/scapy-*.egg-info
%exclude %{python3_sitelib}/test/
%endif


%if %{with doc}
%files doc
%doc doc/scapy/_build_doc/html
%endif


%changelog
%autochangelog