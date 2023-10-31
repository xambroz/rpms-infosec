Name:           python-xlmmacrodeobfuscator
Version:        0.2.7
Release:        2%{?dist}
Summary:        XLM Emulation engine to deobfuscate malicious XLM macros, also known as Excel 4

License:        Apache-2.0
URL:            https://github.com/DissectMalware/XLMMacroDeobfuscator
#               https://github.com/DissectMalware/XLMMacroDeobfuscator/releases/tag/v0.2.7
# Source0:        https://files.pythonhosted.org/packages/source/x/xlmmacrodeobfuscator/XLMMacroDeobfuscator-%%{version}.tar.gz
Source0:        https://github.com/DissectMalware/XLMMacroDeobfuscator/releases/download/v%{version}/XLMMacroDeobfuscator-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%global _description %{expand:
 XLMMacroDeobfuscator XLMMacroDeobfuscator can be used to decode obfuscated XLM
macros (also known as Excel 4.0 macros). It utilizes an internal XLM emulator
to interpret the macros, without fully performing the code.It supports both
xls, xlsm, and xlsb formats. It uses [xlrd2]( [pyxlsb2]( and its own parser to
extract cells and other information from xls, xlsb and xlsm files,
respectively.
}

%description %_description

%package -n     python%{python3_pkgversion}-xlmmacrodeobfuscator
Summary:        %{summary}
%if 0%{?rhel}
%{?python_provide:%python_provide python%{python3_pkgversion}-XLMMacroDeobfuscator}
%else
%py_provides python3-XLMMacroDeobfuscator
%endif


Requires:       python%{python3_pkgversion}-defusedxml
Requires:       python%{python3_pkgversion}-lark-parser
Requires:       python%{python3_pkgversion}-msoffcrypto-tool
Requires:       python%{python3_pkgversion}-pyxlsb2
Requires:       python%{python3_pkgversion}-roman
Requires:       python%{python3_pkgversion}-untangle = 1.2.1
Requires:       python%{python3_pkgversion}-xlrd2

%description -n python%{python3_pkgversion}-xlmmacrodeobfuscator %_description



%prep
%autosetup -n XLMMacroDeobfuscator-%{version}
# Remove bundled egg-info
rm -rf xlmmacrodeobfuscator.egg-info

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-xlmmacrodeobfuscator
%license LICENSE
%doc README.md
%{_bindir}/xlmdeobfuscator
%{python3_sitelib}/XLMMacroDeobfuscator
%{python3_sitelib}/XLMMacroDeobfuscator-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Oct 26 2023 Michal Ambroz <rebus@seznam.cz> - 0.2.7-2
- change SPDX license from long to short format

* Tue Dec 06 2022 Michal Ambroz <rebus@seznam.cz> - 0.2.7-1
- Initial package.
