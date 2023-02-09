# Generated by go2rpm 1.8.2
%bcond_without check

# https://github.com/volatilityfoundation/dwarf2json
%global goipath         github.com/volatilityfoundation/dwarf2json
%global commit          c306d1132f014dc882ffc0ad22e97764bae49451

# ExclusiveArch to %%golang_arches_future and thus excludes the package from %%ix86. 
%gometa -f

%global common_description %{expand:
The dwarf2json is a Go utility that processes files containing symbol and
type information to generate Volatility3 Intermediate Symbol File (ISF) 
JSON output suitable for Linux and macOS analysis.
}

%global golicenses      LICENSE.txt
%global godocs          README.md

Name:           dwarf2json
Version:        0
Release:        %autorelease -p
Summary:        Convert ELF/DWARF symbol and type information into vol3's intermediate JSON

# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/OHECHDPLDJ7LLFUZXQMBBAXEXYTQMXOR/
# https://www.volatilityfoundation.org/license/vsl-v1.0
# https://github.com/volatilityfoundation/volatility3/issues/208
# License:        Volatility Software License
License:        vslv1
URL:            %{gourl}
Source:         %{gosource}

%description %{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o %{gobuilddir}/bin/dwarf2json %{goipath}

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/*

%gopkgfiles

%changelog
* Wed Feb 08 2023 Michal Ambroz <rebus _AT seznam.cz> - 0-0.1.20230208gitc306d11.fc37
- initial build
