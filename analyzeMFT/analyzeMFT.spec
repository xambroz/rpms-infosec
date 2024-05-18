Name:		analyzeMFT
Summary:	analyzeMFT
Group:		Applications/Forensics Tools
Version:	3.0.1
License:	CPL-1.0

Release:	0.1%{?dist}
URL:		https://github.com/dkovar/analyzeMFT
# Releases	https://github.com/dkovar/analyzeMFT/releases
VCS:		https://github.com/dkovar/analyzeMFT

%global         gituser         dkovar
%global         gitname         analyzeMFT
%global         gitdate         20220908
%global         commit          16d12822563cd5cae8675788134ac0ff6e9f5c01
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})


Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

%if 0%{?centos}0%{?amzn} == 70
%define python3_pkgversion 36
%endif

BuildArch:      noarch
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-devel

%description
analyzeMFT.py is designed to fully parse the MFT file from an NTFS filesystem
and present the results as accurately as possible in multiple formats.

%prep
%autosetup -n %{name}-%{commit} -p 1

%build
%py3_build


%install
%py3_install
ln -s %{name}.py %{buildroot}%{_prefix}/bin/%{name}


%files
%doc CHANGES.txt README.txt
%license LICENSE.txt
%attr(755, root, root)	%{_bindir}/%{name}.py
%attr(-,   root, root)	%{_bindir}/%{name}
%attr(644, root, root)	%{python3_sitelib}/*/*
%attr(644, root, root)	%{python3_sitelib}/*egg-info

%changelog
* Mon Dec 04 2023 Michal Ambroz <rebus _AT seznam.cz> - 3.0.1-0.1
- update to 3.0.1 python3 version from git snapshot

* Fri Mar 23 2018 Lawrence R. Rogers <lrr@cert.org> - 2.0.19.1-1
- Release 2.0.19.1
	Changes current to 2018-03-23.

* Fri May 27 2016 Lawrence R. Rogers <lrr@cert.org> - 2.0.19-1
- Release 2.0.19
	v2.0.19,05/27/2016 - (Contributed by lespea)
			   - Properly deal with fncnt findings > 3
			   - Allow the user to use either windows or unix path seperators
			   - General code cleanup

* Fri May 27 2016 Lawrence R. Rogers <lrr@cert.org> - 2.0.18-1
- Release 2.0.18
	v2.0.18,05/24/2015 - Versioning hack

* Tue May 24 2016 Lawrence R. Rogers <lrr@cert.org> - 2.0.17-1
- Release 2.0.17
	v2.0.17,05/23/2015 - Versioning hack

* Sat May 21 2016 Lawrence R. Rogers <lrr@cert.org> - 2.0.16-1
- Release 2.0.16
	v2.0.16,05/21/2015 - Documentation fix and attribute fixes based on NTFS version with thanks to Joachim Metz 

* Sun Feb  8 2015 Lawrence R. Rogers <lrr@cert.org> - 2.0.15-1
- Release 2.0.15
	v2.0.15,02/08/2015 - fix 2's complement computation (Willi)
		   - Added anomaly detection back in. Missing since V2.0.0 in the summer of 2013

* Tue Oct 24 2014 Lawrence R. Rogers <lrr@cert.org> - 2.0.14-1
- Release 2.0.14
	v2.0.14,11/24/2014 - Fixing directory structure.

* Sat Mar 15 2014 Lawrence R. Rogers <lrr@cert.org> - 2.0.12-1
- Release 2.0.12
	v2.0.12,03/15/2014 -- (Contributed by Brice) Added -e, --excel switch to print date/times in format that will
			    cause Excel to import them properly.

* Fri Oct 04 2013 Lawrence R. Rogers <lrr@cert.org> - 2.0.11-1
- Release 2.0.11
	Initial release to the CERT Linux Repository
