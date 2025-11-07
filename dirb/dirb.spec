Name:           dirb
Version:        2.22
%global         fileversion 222
Release:        1%{?dist}
Summary:        URL Bruteforcer

License:        GPL
URL:            https://sourceforge.net/projects/dirb/
Source0:        http://downloads.sourceforge.net/dirb/%{name}%{fileversion}.tar.gz

# Patches from Debian package - https://packages.debian.org/source/sid/dirb
Patch0:         dirb-ext_vars.patch
Patch1:         dirb-gcc10.patch
Patch2:         dirb-html2dict_man.patch
Patch3:         dirb-gendict_man.patch
Patch4:         dirb-manpage_cleaning.patch
Patch5:         dirb-spelling.patch
Patch6:         dirb-fix-bug-with-rootdir-as-home.patch
Patch7:         dirb-fix-usage-examples.patch
Patch8:         dirb-path-as-is.patch
Patch9:        dirb-client_cert.patch


BuildRequires:  libcurl-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  automake


%description
DIRB - URL Bruteforcer: DIRB is a Web Content Scanner. It looks for
hidden Web Objects. It basically works by launching a dictionary
based attack against a web server and analizing the response.
DIRB main purpose is to help in web application auditing.


%prep
# original package has strange permissions, setup/autosetup macro cant be used
# %%setup -n %%{name}%%{fileversion}
tar xzvf %{SOURCE0}
chmod -R u+rwX %{name}%{fileversion}
cd %{name}%{fileversion}
chmod +x configure

%patch 0 -p 1
%patch 1 -p 1
%patch 2 -p 1
%patch 3 -p 1
%patch 4 -p 1
%patch 5 -p 1
%patch 6 -p 1
%patch 7 -p 1
%patch 8 -p 1
%patch 9 -p 1



%build
cd %{name}%{fileversion}
%configure
%make_build


%install
%make_install


%files
%license LICENSE.txt
%doc add-docs-here



%changelog
* Sun Jul 16 2023 Michal Ambroz <rebus@seznam.cz>
- initial package for Fedora

