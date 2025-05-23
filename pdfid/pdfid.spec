Name:           pdfid
Version:        0.0.10
Release:        %autorelease
Summary:        PDF triage program

License:        CC0-1.0
URL:            https://blog.didierstevens.com/programs/pdf-tools/
# URL:          https://blog.didierstevens.com/my-software/#pdf-parser
VCS:            https://github.com/DidierStevens/DidierStevensSuite
Source0:        https://didierstevens.com/files/software/pdf-parser_V0_7_11.zip
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
# Create wrapper script
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/usr/bin/bash
exec python3 %{_bindata}/pdf-parser.py "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%{_bindir}/pdfid.py

%changelog
%autochangelog
