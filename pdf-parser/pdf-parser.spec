Name:           pdf-parser
Version:        0.7.11
Release:        %autorelease
Summary:        Tool for parsing PDF documents
License:        CC0-1.0 and MIT
URL:            https://blog.didierstevens.com/programs/pdf-tools/
# URL:          https://blog.didierstevens.com/my-software/#pdf-parser
VCS:            https://github.com/DidierStevens/DidierStevensSuite

%global         version_under   %(echo %{version} | sed 's/\\./_/g')

Source0:        https://didierstevens.com/files/software/pdf-parser_V%{version_under}.zip
BuildArch:      noarch

BuildRequires:  unzip
BuildRequires:  python3-devel
Requires:       python3

%description
pdf-parser is a tool to parse a PDF document to identify the fundamental elements used in the analyzed file.
It will not render a PDF document or extract text/images/... from a PDF document.
This tool is part of Didier Stevens' collection of PDF analysis tools.

%prep
%autosetup -c

# Mangle the python
sed -i -e 's|\#\!/usr/bin/env python|\#\!/usr/bin/python3|g;' pdf-parser.py

%build
# Nothing to build, pure Python script

%install
mkdir -p %{buildroot}%{_bindir}

# Install main script
install -p -m 755 pdf-parser.py %{buildroot}%{_bindir}/

%files
%{_bindir}/pdf-parser.py

%changelog
%autochangelog