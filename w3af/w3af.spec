Name:           w3af
Version:        1.0
Release:        0.1.rc3%{?dist}
Summary:        Web Application Attack and Audit Framework
Group:          Applications/Internet
License:        GPLv2 and ( LGPLv3 and LGPLv2 and GPLv2+ and GPLv3 and CC-BY-SA )
URL:            http://w3af.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{name}%201.0-rc3%20%5Bmoyogui%5D/%{name}-1.0-rc3.tar.bz2
Source1:        %{name}.png
Patch0:         w3af-fedora.patch
Patch1:         w3af-paths.patch
Patch2:         w3af-dependencies.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python
Requires:       python SOAPpy python-fpconst graphviz-python pyPdf pygtk2 python-BeautifulSoup python-SocksiPy wordnet
#Requires:      python-ntlk #doesn't work

%description
The W3AF, is a Web Application Attack and Audit Framework.
The W3AF core and it's plug-ins are fully written in python.
The project has more than 130 plug-ins, which check for SQL injection,
cross site scripting (XSS), local and remote file inclusion and much more.

%package doc
Summary:        Web Application Attack and Audit Framework - documentation

%description doc
Documentation for the W3AF package.

%prep
%setup -q -n %{name}
%patch0 -p 1 -b .0fedora
%patch1 -p 1 -b .1paths
%patch2 -p 1 -b .2dependencies

#Fix permissions
find core extlib plugins -name "*.py" |xargs chmod -x
chmod +x plugins/attack/payloads/webshell/webshell.pl

#Fix dos eol
dos2unix extlib/nltk_contrib/readability/syllables_no.py
dos2unix extlib/nltk_contrib/readability/textanalyzer.py
dos2unix readme/GPL

#Gzip manpage 
gzip plugins/discovery/oHalberd/man/man1/halberd.1

#Old python
sed -i -e "s%/usr/bin/env python2.[0-9]%/usr/bin/env python%" extlib/nltk_contrib/mit/six863/tagging/tagparse.py
sed -i -e "s%/usr/bin/env python2.[0-9]%/usr/bin/env python%" extlib/nltk/test/doctest_driver.py

#Modify all unnecessary shebangs to comments
find core extlib plugins -name '*.py' |xargs sed -i -e 's%^#!%#%'
sed -i -e 's%^#!%#%' plugins/discovery/oHalberd/scripts/halberd

#Empty files
rm core/data/timeAnalysis.py
echo "<!-- dummy -->" >> core/ui/userInterface.dtd

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -r core extlib plugins profiles scripts tools %{buildroot}%{_datadir}/%{name}/
install -m 755 w3af_console w3af_gui %{buildroot}%{_datadir}/%{name}/
ln -s %{_datadir}/%{name}/w3af_gui %{buildroot}%{_bindir}/w3af_gui
ln -s %{_datadir}/%{name}/w3af_console %{buildroot}%{_bindir}/w3af_console

#Remove libraries which are installed separately or are no longer fuctional
rm -rf %{buildroot}%{_datadir}/%{name}/extlib/SOAPpy
rm -rf %{buildroot}%{_datadir}/%{name}/extlib/pygoogle
rm -rf %{buildroot}%{_datadir}/%{name}/extlib/pyPdf
rm -rf %{buildroot}%{_datadir}/%{name}/extlib/yaml
rm -rf %{buildroot}%{_datadir}/%{name}/extlib/fpconst-0.7.2
rm -rf %{buildroot}%{_datadir}/%{name}/plugins/discovery/oHalberd



#Locales
install -d %{buildroot}%{_datadir}/locale/es/LC_MESSAGES
install locales/es/LC_MESSAGES/w3af.mo %{buildroot}%{_datadir}/locale/es/LC_MESSAGES/w3af.mo

install -d %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES
install locales/ru/LC_MESSAGES/w3af.mo %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES/w3af.mo

#Desktop
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        --vendor fedora \
        fedora/%{name}.desktop

install -d %{buildroot}%{_datadir}/pixmaps
install %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc readme/CONTRIBUTORS readme/GPL  readme/INSTALL  readme/README  readme/TODO fedora/copyright
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_bindir}/w3af_gui
%{_bindir}/w3af_console
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{name}.png
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/w3af.mo
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/w3af.mo

%files doc
%defattr(-,root,root,-)
%doc readme/EN readme/FR


%changelog
* Tue Jan 05 2010 Michal Ambroz <rebus at, seznam.com> 1.0-0.1.rc3
- dec

* Tue Jan 05 2010 Michal Ambroz <rebus at, seznam.com> 1.0-0.1.rc3
- Initial SPEC for Fedora 12

