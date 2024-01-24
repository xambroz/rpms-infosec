Name:           httpdump
Version:        0
Release:        0.13%{?dist}
Summary:        Capture and parse HTTP traffic
URL:            https://github.com/hsiafan/httpdump
VCS:            https://github.com/hsiafan/httpdump

# Upstream license specification: BSD-2-Clause
License:        BSD-2-Clause

%bcond_without check

# https://github.com/hsiafan/httpdump
%global goipath         github.com/hsiafan/httpdump
%global commit          4fd809447b593cc9e4420141691ec304b3fa4e9e
%global date            20231019

%gometa

%global common_description %{expand:
Capture and parse HTTP traffic.}

%global golicenses      LICENSE
%global godocs          README.md

Source0:        %{gosource}

BuildRequires:  golang(github.com/google/gopacket)
BuildRequires:  golang(github.com/google/gopacket/layers)
BuildRequires:  golang(github.com/google/gopacket/pcap)
BuildRequires:  golang(github.com/google/gopacket/tcpassembly/tcpreader)
BuildRequires:  golang(github.com/hsiafan/glow/flagx)
BuildRequires:  golang(github.com/hsiafan/glow/iox/filex)
BuildRequires:  golang(github.com/hsiafan/vlog)
BuildRequires:  golang(golang.org/x/text/encoding)
BuildRequires:  golang(golang.org/x/text/encoding/htmlindex)
BuildRequires:  golang(golang.org/x/text/transform)

%if %{with check}
# Tests
BuildRequires:  golang(github.com/stretchr/testify/assert)
%endif

%description
%{common_description}

%gopkg

%prep
%goprep

%build
%gobuild -o %{gobuilddir}/bin/httpdump %{goipath}
for cmd in httpport; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/*

%gopkgfiles

%changelog
* Wed Jan 24 2024 Michal Ambroz <rebus _AT seznam.cz> - 0-0.13
- bump to current git commit from 20231019

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Michal Ambroz <rebus _AT seznam.cz> - 0-0.10
- bump to current git commit from 20220727

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 0-0.7
- Rebuild for CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in
  golang

* Sat Jun 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0-0.6
- Rebuilt for CVE-2022-1996, CVE-2022-24675, CVE-2022-28327, CVE-2022-27191,
  CVE-2022-29526, CVE-2022-30629

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0-0.1.20200713gite6fa868
- Initial package for Fedora
