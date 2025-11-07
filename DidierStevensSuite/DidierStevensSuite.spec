Name:           DidierStevensSuite
Version:        20250306
Summary:        Forensics tools from Didier Stevens Lab

License:        CC0-1.0
URL:            https://blog.didierstevens.com/didier-stevens-suite/
VCS:            git:https://github.com/DidierStevens/DidierStevensSuite

%global         gituser         DidierStevens
%global         gitname         DidierStevensSuite
%global         gitdate         %{version}
%global         commit          104bb4fe77e24f0891a954af349449227d06f77d
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# Build by default from the git snapshot as Didier doesn't do any releases
%bcond_without  release

# Build from git release version
%if %{with release}
Release:       %autorelease
# Source0:     https://github.com/%%{gituser}/%%{gitname}/archive/v%%{upversion}.tar.gz#/%%{name}-%%{upversion}.tar.gz
Source0:       https://didierstevens.com/files/software/DidierStevensSuite.zip#/%{name}-%{version}.zip
%else
# Build from git commit baseline
Release:       %autorelease -s %{gitdate}git%{shortcommit}
Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{gitdate}git%{shortcommit}.tar.gz
%endif

# use shared directory in linux for the data files
Patch0:        DidierStevensSuite-20231016-1768-json.patch

BuildArch: noarch
#BuildRequires:  

# Require the utilities packaged separately
Requires:       xorsearch
Requires:       pdf-parser
Requires:       pdfid

# ssdeep.py requires python3-ppdeep
Requires:       python3-ppdeep



%description
Forensics tools from Didier Stevens Lab

%prep
%if %{with release}
    %autosetup -n %{gitname} -p 1
%else
    %autosetup -n %{gitname}-%{commit} -p 1
%endif

# remove Linux/OSX binaries
rm -rf Linux OSX

# remove Windows binaries
rm *.exe *.dll

# Remove files tracked separately
rm \
    pdf-parser.py \
    pdfid.py


# be explicit about python to use, dos2unix
sed -i \
    -e 's/\r//g' \
    -e 's%/usr/bin/env python$%/usr/bin/python3%g;' \
    -e 's%/usr/bin/python$%/usr/bin/python3%g;' \
     *.py

# dos2unix
sed -i -e 's/\r//g' *.yara

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
%{_bindir}/*.py
%{_datadir}/%{name}


%changelog
%autochangelog
