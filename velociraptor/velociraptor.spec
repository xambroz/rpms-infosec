Name:           velociraptor
Version:        0.6.2
Release:        1%{?dist}
Summary:        Velociraptor endpoint visibility tool for security incident response

# https://github.com/Velocidex/velociraptor/blob/master/LICENSE
License:        AGPL-3.0-or-later
URL:            https://github.com/Velocidex/velociraptor
Source0:        https://github.com/Velocidex/velociraptor/releases/download/v%{version}/velociraptor-v0.6.2-linux-amd64
Source1:        https://github.com/Velocidex/velociraptor/releases/download/v%{version}/velociraptor-v0.6.2-linux-amd64.sig

# gpg2 --search-key 0572F28B4EF19A043F4CBBE0B22A7FB19CB6CFA1
# gpg2 --list-public-keys 0572F28B4EF19A043F4CBBE0B22A7FB19CB6CFA1
# gpg2 --export --export-options export-minimal 0572F28B4EF19A043F4CBBE0B22A7FB19CB6CFA1 > gpgkey-0572F28B4EF19A043F4CBBE0B22A7FB19CB6CFA1.gpg
Source2:	gpgkey-0572F28B4EF19A043F4CBBE0B22A7FB19CB6CFA1.gpg

BuildRequires:  gnupg2

%description
Velociraptor is a tool for collecting host based state information using The Velociraptor Query Language (VQL) queries.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
pwd
mkdir -p %{name}-%{version}
cd %{name}-%{version}
pwd

%build
echo Nothing to build
chmod +x %{SOURCE0}
%{SOURCE0} --help
%{SOURCE0} config generate

%install



%files
#%license add-license-file-here
#%doc add-docs-here



%changelog
* Mon Jan 17 2022 Michal Ambroz <rebus@seznam.cz>
- 
