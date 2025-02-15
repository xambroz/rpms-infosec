Name:           python-bluepy
Version:        1.3.0
Summary:        Python interface to Bluetooth LE
URL:            https://github.com/IanHarvey/bluepy
VCS:            git:https://github.com/IanHarvey/bluepy


%global         giturl          https://github.com/IanHarvey/bluepy
%global         commit          7ad565231a97c304c0eff45f2649cd005e69db09
%global         gitdate         20210503
%global         shortcommit     %(c=%{commit}; echo ${c:0:8})

Release:        %autorelease -s %{gitdate}git%{shortcommit}

#bluepy uses code from the bluez project, which is made available under
#Version 2 of the GNU Public License, bluepy itself is placed in the
#public domain
License:        Public Domain and GPLv2
Source0:        %{url}/archive/%{commit}/bluepy-%{version}.tar.gz#/bluepy-%{version}-%{gitdate}-%{shortcommit}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

%global _description %{expand:
Python interface to Bluetooth LE on Linux.
This is a project to provide an API to allow
access to Bluetooth Low Energy devices from Python.}

%description %_description

%package -n python3-bluepy
Summary:        %{summary}
BuildRequires:  python3-devel make gcc
BuildRequires:  glib2-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist sphinx}
%{?python_provide:%python_provide python3-bluepy}

%description -n python3-bluepy %_description

%package doc
Summary:        %{summary}

%description doc %_description
Documentation for %{name}.

%prep
%autosetup -n bluepy-%{commit}
rm -rf bluepy.egg-info
find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%set_build_flags
export PYTHONPATH=../
sed 's|CFLAGS =|CFLAGS +=|g' -i bluepy/Makefile
sed 's|CPPFLAGS =|CPPFLAGS +=|g' -i bluepy/Makefile
sed 's| $(LDLIBS)| $(LDFLAGS) $(LDLIBS)|g' -i bluepy/Makefile
%py3_build
make -C docs SPHINXBUILD=sphinx-build-3 html
rm -rf docs/_build/html/{.doctrees,.buildinfo,.nojekyll} -vf

%install
%py3_install

%py3_shebang_fix -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/bluepy/{get_services,scanner}.py

for file in %{buildroot}%{_bindir}/{thingy52,sensortag,blescan}; do
   chmod a+x $file
done

for file in %{buildroot}%{python3_sitelib}/bluepy/{get_services,scanner}.py; do
   chmod a+x $file
done

for file in %{buildroot}%{python3_sitelib}/bluepy/{*.c,*.h}; do
   rm -rf $file
done

%files -n python3-bluepy
%{python3_sitelib}/bluepy/
%{python3_sitelib}/bluepy-*.egg-info/
%{_bindir}/blescan
%{_bindir}/sensortag
%{_bindir}/thingy52
%license LICENSE.txt
%doc README README.md

%files doc
%license LICENSE.txt
%doc docs/_build/html

%changelog
%autochangelog
