Name:           sqlmap
Version:        1.7
Release:        1%{?dist}
Summary:        Penetration testing tool detecting and exploiting SQL injection flaws


%global         _binaries_in_noarch_packages_terminate_build 0
%global         gituser         sqlmapproject
%global         gitname         sqlmap
%global         commit          05293e01a4012d9ba09ec66343aa0c14f7a492f7
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})



Group:          Development/Languages

# sqlmap itself licensed with GPLv2
# cloak.py licensed with LGPLv2.1+
License:        GPLv2 and LGPLv2+
URL:            http://sqlmap.org/
#               https://github.com/sqlmapproject/sqlmap
# Source0:       https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Generated with help2man via script sqlmap-genmanpage.sh
Source1:        sqlmap.1
# Generated with help2man --no-info --no-discard-stderr sqlmapapi > ../SOURCES/sqlmapapi.1
Source2:        sqlmapapi.1



#Patch the makefiles for compilation of the udf libraries for Fedora
Patch0:         sqlmap-udfmakefile.patch

#Patch the release number to avoid reading it from .svn files
Patch1:         sqlmap-revision.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python
BuildRequires:  mysql-devel
Requires:       python(abi) >= 2.6
Requires:       upx

%description
An open source penetration testing tool that automates the process of
detecting and exploiting SQL injection flaws and taking over of back-end
database servers.
It comes with a broad range of features lasting from database
fingerprinting, over data fetching from the database, to accessing the
underlying file system and executing commands on the operating system via
out-of-band connections.


%prep
#setup -qn %{gitname}-%{commit}
%autosetup -n %{name}-%{version}

#Modify all unnecessary shebangs to comments
find extra lib plugins -name '*.py' |xargs sed -i -e 's|^#!|#|;'

#Change env python to explicit python version
find extra lib plugins tamper waf thirdparty -name '*.py' |xargs sed -i -e 's|/usr/bin/env python|/usr/bin/python|;'


#Remove binary plugins
#rm -rf udf
#rm -rf lib/contrib/upx
#rm -f  shell/runcmd.exe_

#Uncloack files
find ./ -name '*.*_' -type f -exec python ./extra/cloak/cloak.py -d -i '{}' \;

#Remove source files for other OS
#rm -rf extra/runcmd
#rm -rf extra/udfhack/windows

#Rwmove .svn files
find ./ -name ".svn" |xargs rm -rf


%build
#%ifarch x86_64
#        cd extra/udfhack/linux/64/lib_mysqludf_sys
#        make all
#        cd ../lib_postgresqludf_sys
#        make all
#%endif

#%ifarch i386
#        cd extra/udfhack/linux/32/lib_mysqludf_sys
#        make all
#        cd ../lib_postgresqludf_sys
#        make all
#%endif



%install
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_mandir}/man1

cp -r extra lib plugins procs shell tamper thirdparty txt udf waf xml %{buildroot}%{_datadir}/%{name}
install -m 755 sqlmap.py %{buildroot}%{_datadir}/%{name}/
ln -s %{_datadir}/%{name}/%{name}.py %{buildroot}%{_bindir}/%{name}
install -m 755 sqlmapapi.py %{buildroot}%{_datadir}/%{name}/
ln -s %{_datadir}/%{name}/%{name}api.py %{buildroot}%{_bindir}/%{name}api
install -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/

# Install manpage
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/


#Remove devel files from the installation
find %{buildroot}%{_datadir}/%{name} -name *.c|xargs rm



%files
%license LICENSE
%doc doc/[A-Z]*
%dir %{_datadir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}api
%{_datadir}/%{name}/*
%{_sysconfdir}/%{name}/%{name}.conf
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}api.1*


%changelog
* Thu Jan 4 2018 Michal Ambroz <rebus AT seznam.cz> - 1.2-1
- Update to 1.2

* Thu Dec 7 2017 Michal Ambroz <rebus AT seznam.cz> - 1.1.12-1
- Update to 1.1.12

* Sat May 12 2012 Michal Ambroz <rebus AT seznam.cz> - 0.9-1
- Update to 0.9

* Sat Apr 03 2010 Michal Ambroz <rebus AT seznam.cz> - 0.8-1
- Initial dirty build for Fedora
- TODO - split noarch and binary plugin package
-      - buildl libraries from source

