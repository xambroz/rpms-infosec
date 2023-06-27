Name:           ipcalcpl
Version:        0.41
Release:        1%{?dist}
Group:          Applications/Internet
Summary:        Perl implementation of ipcalc.

License:        GPL-2.0-or-later
URL:            http://jodies.de/ipcalc
Source0:        http://jodies.de/ipcalc-archive/ipcalc-%{version}.tar.gz

BuildArch:      noarch

%description
Perl implementation of the IP calculator. The version, which is common
to find on the Debian systems as ipcalc package.

%prep
%setup -q -n ipcalc-%{version}

%build

%install
install -D -d %{buildroot}%{_bindir}
install -m 0755 ipcalc %{buildroot}%{_bindir}/ipcalc.pl


%files
%doc changelog contributors
%license license
%{_bindir}/ipcalc.pl

%changelog
* Thu Oct 06 2016 Michal Ambroz <rebus at, seznam.cz> - 0.41-1
- initial build for Fedora 29


