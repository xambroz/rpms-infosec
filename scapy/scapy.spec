Name:           scapy
Version:        2.7.0
Release:        %autorelease
Summary:        Interactive packet manipulation tool and network scanner

%global         gituser         secdev
%global         gitname         scapy
%global         gitdate         20251225
%global         commit          40fc5ecf9e69e9bd76664d63ae133d4973fcf81b
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         giturl          https://github.com/%{gituser}/%{gitname}

License:        GPL-2.0-only
URL:            https://scapy.net/
#was            http://www.secdev.org/projects/scapy/
VCS:            git:%{giturl}
#               https://github.com/secdev/scapy/releases
#               https://bitbucket.org/secdev/scapy/pull-request/80
#               https://scapy.readthedocs.io/en/latest/introduction.html
Source0:        %{giturl}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%global         common_desc %{expand:
Scapy is a powerful interactive packet manipulation program built on top
of the Python interpreter. It can be used to forge or decode packets of
a wide number of protocols, send them over the wire, capture them, match
requests and replies, and much more.}

# By default do not build documentation because of not allowed cc-by-nc-sa license
%bcond_with        doc


BuildArch:      noarch

BuildRequires:  make
BuildRequires:  sed
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with doc}
BuildRequires:  python%{python3_pkgversion}-tox
%endif

%if ( 0%{?rhel} && 0%{?rhel} == 8 )
# RHEL8 - deps bellow are for RHEL8
# This should be added by generate_buildrequires on newer platforms
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  pyproject-rpm-macros
%endif

# Check Tests
BuildRequires:  python%{python3_pkgversion}-cryptography
BuildRequires:  python%{python3_pkgversion}-tkinter


Recommends:     tcpdump
# Using database of manufactures /usr/share/wireshark/manuf
Recommends:     wireshark-cli

%description %{common_desc}


%package -n python%{python3_pkgversion}-%{name}
Summary:        Interactive packet manipulation tool and network scanner

%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
Provides:       %{name} = %{version}-%{release}

Recommends:     PyX
Recommends:     python%{python3_pkgversion}-matplotlib
Recommends:     ipython3

%description -n python%{python3_pkgversion}-%{name}
%{common_desc}


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


%if (0%{?fedora} && 0%{?fedora} > 33 ) || ( 0%{?rhel} && 0%{?rhel} > 8 ) || 0%{?flatpak}
%generate_buildrequires
%pyproject_buildrequires
%endif


%build
%pyproject_wheel

%if %{with doc}
make -C doc/scapy html BUILDDIR=_build_doc SPHINXBUILD=sphinx-build-%python3_version

rm -f doc/scapy/_build_doc/html/.buildinfo
rm -f doc/scapy/_build_doc/html/_static/_dummy
%endif



%install
install -dp -m0755 %{buildroot}%{_mandir}/man1
install -Dp -m0644 doc/scapy.1* %{buildroot}%{_mandir}/man1/

%pyproject_install
%pyproject_save_files scapy

# Rename the executables
mv -f %{buildroot}%{_bindir}/scapy   %{buildroot}%{_bindir}/scapy3

# Link the default to the python3 version of executables
ln -s scapy3 %{buildroot}%{_bindir}/scapy



%check
# Dummy import check
%pyproject_check_import -e 'scapy.arch.bpf.core' -e 'scapy.arch.bpf.supersocket' \
    -e 'scapy.arch.windows' -e 'scapy.arch.windows.native' -e 'scapy.arch.windows.structures' \
    -e 'scapy.contrib.cansocket_python_can' -e 'scapy.tools.generate_bluetooth' \
    -e 'scapy.tools.generate_ethertypes' -e 'scapy.tools.generate_manuf' -e 'scapy.tools.scapy_pyannotate'

# TODO: Need to fix/remove slow/failed test
# cd test/
# ./run_tests_py2 || true
# ./run_tests_py3 || true



%files -n python%{python3_pkgversion}-%{name} -f %{pyproject_files}
%license LICENSE
%doc %{_mandir}/man1/scapy.1*
%{_bindir}/scapy
%{_bindir}/scapy3


%if %{with doc}
%files doc
%doc doc/scapy/_build_doc/html
%endif


%changelog
%autochangelog
