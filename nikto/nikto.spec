Name:           nikto
Epoch:          1
Version:        2.5.0
Release:        1%{?dist}
Summary:        Web server scanner
URL:            https://www.cirt.net/Nikto2
VCS:            https://github.com/sullo/nikto

# =========== License review ===============
# GPL-2.0-only for the code
# /nikto-2.5.0/program/databases have "Redistributable, no modification permitted" type of license
# during review it was considered the nikto database to be content, similar to firmware.
# Also potentially the content is tainted by the GPL license as it is distributed in a bundle,
# which itself released with GPL-2.0-only license.
# 
# License text for the db files extracted and attached as nikto-database-license.txt
#
License:        GPL-2.0-only AND nikto-database-license
Source0:        https://github.com/sullo/nikto/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        nikto-database-license.txt

# nikto contains customized / fixed libwhisker library,
# tested with the system-wide libwhisker 2.5, but it was not working any more
# Patch use system-wide libwhisker2 instead of the embedded one
# Patch0:         nikto-2.5.0-libwhisker2.patch

# Update obsolete FSF address in the license text
Patch1:         https://github.com/sullo/nikto/pull/805.patch#/nikto-2.5.0-fsf-address.patch


BuildArch:      noarch
BuildRequires:  perl-generators

# Nikto can work well with outputs from nmap.
# It can parse hosts in a form of the nmap grepable optput
%if 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} >= 8 )
Recommends:     nmap
%endif

# Requires potentially not found by the auto dependency search
Requires:       perl(Time::HiRes)
Requires:       perl(bignum)
Requires:       perl(List::Util)
Requires:       perl(Net::hostent)
Requires:       perl(Net::SSLeay)
Requires:       perl(Net::SSLeay)
Requires:       perl(Text::ParseWords)
Requires:       perl(JSON::PP)
Requires:       perl(List::Util)
Requires:       perl(Getopt::Long)


# Nikto contains patched version of the libwhisker library
# forked at version 2.5, but heavily fixed over the years
# Nikto talks about this version as 2.5.1
Provides: bundled(perl-libwhisker2)  = 2.5

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(plugins::LW2\\)\\s*$


# We don't provide any perl modules
%global __provides_exclude_from %{_datadir}/nikto/plugins/JSON-PP.pm

%description
Nikto is an Open Source (GPL) web server scanner which performs comprehensive
tests against web servers for multiple items, including over 7000 potentially
dangerous files/programs, checks for outdated versions of over 1250 servers,
and version specific problems on over 270 servers.
    It also checks for server configuration items such as the presence of
multiple index files, HTTP server options, and will attempt to identify
installed web servers and software. Scan items and plugins are frequently
updated and can be automatically updated.

Nikto is not designed as a stealthy tool. It will test a web server in the
quickest time possible, and is obvious in log files or to an IPS/IDS.
However, there is support for LibWhisker's anti-IDS methods in case you want
to give it a try (or test your IDS system).


%prep
%autosetup -p 1

# change configfile path
sed -i "s:/etc/nikto.conf:%{_sysconfdir}/nikto/config:" program/nikto.pl

# enable nmap by default and set plugindir path
sed -i "s:# EXECDIR=/opt/nikto:EXECDIR=%{_datadir}/nikto:;
        s:# PLUGINDIR=/opt/nikto/plugins:PLUGINDIR=%{_datadir}/nikto/plugins:;
        s:# TEMPLATEDIR=/opt/nikto/templates:TEMPLATEDIR=%{_datadir}/nikto/templates:;
        s:# DOCDIR=/opt/nikto/docs:DOCDIR=%{_datadir}/nikto/docs:" program/nikto.conf.default

# Disable RFIURL by default - let users configure it themselves to trustworthy source
sed -i "s:^RFIURL=:#RFIURL=:" program/nikto.conf.default

# Copy the nikto-database-license snippet to build directory for packaging
cp -p %{SOURCE1} ./


%build
# no build required


%install
install -pD program/nikto.pl %{buildroot}%{_bindir}/nikto
install -pD program/replay.pl %{buildroot}%{_bindir}/nikto-replay
install -m 0644 -pD program/docs/nikto.1 %{buildroot}%{_mandir}/man1/nikto.1
mkdir -p %{buildroot}%{_datadir}/nikto/databases/
install -m 0644 -p program/databases/* %{buildroot}%{_datadir}/nikto/databases/
mkdir -p %{buildroot}%{_datadir}/nikto/plugins/
install -m 0644 -p program/plugins/* %{buildroot}%{_datadir}/nikto/plugins/
mkdir -p %{buildroot}%{_datadir}/nikto/templates/
install -m 0644 -p program/templates/* %{buildroot}%{_datadir}/nikto/templates/
install -m 0644 -pD program/nikto.conf.default %{buildroot}%{_sysconfdir}/nikto/config

# # remove unneeded files
# rm -f %%{buildroot}%%{_datadir}/nikto/plugins/LW2.pm


%files
%license COPYING
%license nikto-database-license.txt
%doc README.md Dockerfile program/docs/nikto.dtd program/docs/nikto_schema.sql
%{_bindir}/nikto*
%config(noreplace) %{_sysconfdir}/nikto
%{_datadir}/nikto
%{_mandir}/man1/nikto.1*


%changelog
* Thu Dec 07 2023 Michal Ambroz <rebus AT seznam.cz> - 1:2.5.0-1
- bump to 2.5.0 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.6-4
- #1651845 - add dependencies not detected automatically during build

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 08 2018 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.6-1
- bump to upstream version
- fix weekdays in changelog
- cherry pick patch from upstream for CVE-2018-11652 - bugs 1585612,1585614

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 24 2014 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.5-10
- updated link to the upstream package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:2.1.5-7
- Perl 5.18 rebuild

* Thu Apr 25 2013 Tom Callaway <spot@fedoraproject.org> - 1:2.1.5-6
- treat nikto database files as content, update license

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Paul Howarth <paul@city-fan.org> - 1:2.1.5-4
- don't rpm-provide perl JSON modules (#885143)

* Thu Oct 04 2012 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.5-3
- add databases directory
- omit initialization of SSL untill it is pushed to libwhiskers
  beware this can result in usage of Net::SSLeay and memory leaks

* Tue Sep 18 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1:2.1.5-2
- Rewrite libwiskers patch

* Mon Sep 17 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1:2.1.5-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 9 2011 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.4-2
- Fix the default config file

* Mon Mar 28 2011 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.4-1
- Version bump

* Sun Sep 12 2010 Michal Ambroz <rebus AT seznam.cz> - 1:2.1.3-1
- Version bump

* Mon Mar 22 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1:2.1.1-3
- Add missing changelog
- Version bump

* Mon Mar 22 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1:2.1.1-2
- Update version to 2.1.1 and fix version collisions, 
  based on SPEC provided by Michal Ambroz <rebus at, seznam.cz> 

* Mon Feb 08 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.03-3
- Resolve rhbz #515871

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 2.03-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.36-4
- fix license tag

* Wed May 30 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 1.36-3
- Add sed magic to really replace nikto-1.36-config.patch
* Mon May 28 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 1.36-2
- Remove libwhisker Requires
- Replace configfile patch with sed magic
- Update License
- Add database-license.txt to %%doc
* Fri May 04 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 1.36-1
- Initial build
