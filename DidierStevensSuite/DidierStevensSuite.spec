Name:           DidierStevensSuite
Version:        20231016
%global         baserelease 1
Summary:        Forensics tools from Didier Stevens Lab

License:        free as beer
URL:            https://blog.didierstevens.com/didier-stevens-suite/
VCS:            https://github.com/DidierStevens/DidierStevensSuite

%global         gituser         DidierStevens
%global         gitname         DidierStevensSuite
%global         gitdate         %{version}
%global         commit          41b01df75c8bb332f37d2e9eb4c8279583164d0e
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Build by default from the git snapshot as Didier doesn't do any releases
%bcond_with     release

# Build from git release version
%if %{with release}
Release:       %{baserelease}%{?dist}
# Source0:     https://github.com/%%{gituser}/%%{gitname}/archive/v%%{upversion}.tar.gz#/%%{name}-%%{upversion}.tar.gz
Source0:       https://github.com/%{gituser}/%{gitname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
# Build from git commit baseline
Release:       %{baserelease}.git%{shortcommit}%{?dist}
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

# use shared directory in linux for the data files
Patch0:        DidierStevensSuite-20231016-1768-json.patch

# die gracefully on broken pipe for xmldump.py
Patch1:        DidierStevensSuite-20231016-brokenpipe.patch

BuildArch: noarch
#BuildRequires:  

# Require the utilities packaged separately
Requires:       xorsearch

# ssdeep.py requires python3-ppdeep
Requires:       python3-ppdeep



%description
Forensics tools from Didier Stevens Lab

%prep
%if %{with release}
    %autosetup -n %{gitname}-%{version} -p 1
%else
    %autosetup -n %{gitname}-%{commit} -p 1
%endif

# remove Linux/OSX binaries
rm -rf Linux OSX

# remove Windows binaries
rm *.exe *.dll

# be explicit about python to use
sed -i -e 's%/usr/bin/env python$%/usr/bin/python3%g;' \
       -e 's%/usr/bin/python$%/usr/bin/python3%g;' *.py



%build


%install
mkdir -p %{buildroot}/usr/share/%{name}
cp -p 1768.json %{buildroot}/usr/share/%{name}/
cp -p file-magic.def %{buildroot}/usr/share/%{name}/
cp -p format-bytes.library %{buildroot}/usr/share/%{name}/
cp -p pdfid.ini %{buildroot}/usr/share/%{name}/


mkdir -p %{buildroot}/usr/share/%{name}/yara
cp -r *.yara %{buildroot}/usr/share/%{name}/yara/

mkdir -p %{buildroot}/usr/share/%{name}/lua
cp -r *.lua %{buildroot}/usr/share/%{name}/lua/


mkdir -p %{buildroot}/usr/bin
chmod +x *.py
cp -r *.py %{buildroot}/usr/bin/


%files
%doc
/usr/bin/*.py
/usr/share/%{name}


%changelog
* Wed Feb  3 2016 Michal Ambroz <rebus at, seznam.cz>
- initial package for Fedora
