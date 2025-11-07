Name:           pdfid
Version:        0.2.10
Release:        %autorelease
Summary:        PDF triage program
License:        CC0-1.0
URL:            https://blog.didierstevens.com/programs/pdf-tools/
# URL:          https://blog.didierstevens.com/my-software/#pdfid
VCS:            https://github.com/DidierStevens/DidierStevensSuite

%global         version_under   %(echo %{version} | sed 's/\\./_/g')

Source0:        https://didierstevens.com/files/software/pdfid_v%{version_under}.zip
BuildArch:      noarch

BuildRequires:  unzip
BuildRequires:  python3-devel
Requires:       python3

%description
This tool is not a PDF parser, but it will scan a file to look for certain PDF
keywords, allowing you to identify PDF documents that contain (for example)
JavaScript or execute an action when opened. PDFiD will also handle name obfuscation.

%prep
%autosetup -c

# Mangle the python
sed -i -e 's|\#\!/usr/bin/env python|\#\!/usr/bin/python3|g;' pdfid.py

%build
# Nothing to build, pure Python script

%install
mkdir -p %{buildroot}%{_bindir}

# Install main script
install -p -m 755 pdfid.py %{buildroot}%{_bindir}/

%files
%{_bindir}/pdfid.py

%changelog
%autochangelog
