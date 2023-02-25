%global 	pypi_name 	gnureadline
%global 	pypi_version 	8.1.2



Name:           python-gnureadline
Version:        8.1.2
Release:        1%{?dist}
Summary:        The standard Python readline extension statically linked against the GNU readline library

License:        None
URL:            http://github.com/ludwigschwardt/python-gnureadline
Source0:        %{pypi_source}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)

%global _description %{expand:
Stand-alone GNU readline module First... STOP -Consider this: do you really
need this package in 2022? You typically don't if- you use the Python provided
by a standard Linux distribution like Ubuntu, Debian, CentOS, etc. *(It already
uses the proper readline.)* - you run **Windows** *(It won't work! Try*
pyreadline_ or prompt_toolkit_ *instead.)*
}

%description %_description


%package -n     python%{python3_pkgversion}-gnureadline
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-gnureadline}

%description -n python%{python3_pkgversion}-gnureadline
Stand-alone GNU readline module First... STOP -Consider this: do you really
need this package in 2022? You typically don't if- you use the Python provided
by a standard Linux distribution like Ubuntu, Debian, CentOS, etc. *(It already
uses the proper readline.)* - you run **Windows** *(It won't work! Try*
pyreadline_ or prompt_toolkit_ *instead.)*


%prep
%autosetup -n gnureadline-%{version}
# Remove bundled egg-info
rm -rf gnureadline.egg-info

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files gnureadline

%files -n python%{python3_pkgversion}-gnureadline -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{python3_sitearch}/__pycache__/*
%{python3_sitearch}/readline.py
# %%{python3_sitearch}/gnureadline-%%{version}-py%%{python3_version}.egg-info
# %%{python3_sitearch}/gnureadline.cpython-311-x86_64-linux-gnu.so

%changelog
* Sat Feb 25 2023 Michal Ambroz <rebus@seznam.cz> - 8.1.2-1
- Initial package.
