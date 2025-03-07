Name:           python-pyzbar
Version:        0.1.9

Summary:        Read one-dimensional barcodes and QR codes from Python

License:        Python
URL:            https://pypi.python.org/pypi/pyzbar
%global         vcsurl https://github.com/NaturalHistoryMuseum/pyzbar
VCS:            git:%{vcsurl}

%global         pypi_name       pyzbar
%global         gituser         NaturalHistoryMuseum
%global         gitname         pyzbar
%global         gitdate         20211025
%global         commit          ff2892666fa7cd305f0a95f9808159809c6fc222
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Release:        %autorelease -s %{gitdate}git%{shortcommit}
# Source0:      %%{vcsurl}/archive/%%{version}.tar.gz#/%%{name}-%%{version}.tar.gz
Source0:        %{vcsurl}/archive/%{commit}/%{gitname}-%{version}-%{shortcommit}.tar.gz#/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%global common_description %{expand:
Read one-dimensional barcodes and QR codes from Python 2 and 3 using the zbar library.
- Pure python
- Works with PIL / Pillow images, OpenCV / imageio / numpy ndarrays, and raw bytes
- Decodes locations of barcodes
- No dependencies, other than the zbar library itself
- Tested on Python 2.7, and Python 3.5 to 3.10

The older zbar package is stuck in Python 2.x-land. The zbarlight package does not provide support for Windows and depends upon Pillow.
}

%description %common_description

%package -n python%{python3_pkgversion}-pyzbar
Summary:        Read one-dimensional barcodes and QR codes from Python

%description -n python%{python3_pkgversion}-pyzbar
%{common_description}


%prep
%autosetup -n %{gitname}-%{commit}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%py3_build


%install
%py3_install


%check
export PYTHON=%{__python3}
export PYTHON=%{__python3}
%{__python3} setup.py test


%files -n python%{python3_pkgversion}-pyzbar
%{_bindir}/read_zbar*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}*.egg-info

%changelog
%autochangelog