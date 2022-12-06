Name:           python-xlmmacrodeobfuscator
Version:        0.2.7
Release:        1%{?dist}
Summary:        XLM Emulation engine to deobfuscate malicious XLM macros, also known as Excel 4

License:        Apache License 2.0
URL:            https://github.com/DissectMalware/XLMMacroDeobfuscator
# Source0:        https://files.pythonhosted.org/packages/source/x/xlmmacrodeobfuscator/XLMMacroDeobfuscator-%%{version}.tar.gz
Source0:        https://github.com/DissectMalware/XLMMacroDeobfuscator/releases/download/v%{version}/XLMMacroDeobfuscator-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
 XLMMacroDeobfuscator XLMMacroDeobfuscator can be used to decode obfuscated XLM
macros (also known as Excel 4.0 macros). It utilizes an internal XLM emulator
to interpret the macros, without fully performing the code.It supports both
xls, xlsm, and xlsb formats. It uses [xlrd2]( [pyxlsb2]( and its own parser to
extract cells and other information from xls, xlsb and xlsm files,
respectively.

%package -n     python3-xlmmacrodeobfuscator
Summary:        %{summary}
%{?python_provide:%python_provide python3-xlmmacrodeobfuscator}

Requires:       python3dist(defusedxml)
Requires:       python3dist(lark-parser)
Requires:       python3dist(msoffcrypto-tool)
Requires:       python3dist(pyxlsb2)
Requires:       python3dist(roman)
Requires:       python3dist(setuptools)
Requires:       python3dist(untangle) = 1.2.1
Requires:       python3dist(xlrd2)
%description -n python3-xlmmacrodeobfuscator
 XLMMacroDeobfuscator XLMMacroDeobfuscator can be used to decode obfuscated XLM
macros (also known as Excel 4.0 macros). It utilizes an internal XLM emulator
to interpret the macros, without fully performing the code.It supports both
xls, xlsm, and xlsb formats. It uses [xlrd2]( [pyxlsb2]( and its own parser to
extract cells and other information from xls, xlsb and xlsm files,
respectively.


%prep
%autosetup -n XLMMacroDeobfuscator-%{version}
# Remove bundled egg-info
rm -rf xlmmacrodeobfuscator.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-xlmmacrodeobfuscator
%license LICENSE
%doc README.md
%{_bindir}/xlmdeobfuscator
%{python3_sitelib}/XLMMacroDeobfuscator
%{python3_sitelib}/XLMMacroDeobfuscator-%{version}-py%{python3_version}.egg-info

%changelog
* Tue Dec 06 2022 Michal Ambroz <rebus@seznam.cz> - 0.2.7-1
- Initial package.
