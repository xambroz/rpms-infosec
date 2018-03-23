# Generated from filesize-0.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name filesize

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 1%{?dist}
Summary: filesize is a small class for handling filesizes with both the SI and binary prefixes, allowing conversion from any size to any other size
License: MIT
URL: https://github.com/dominikh/filesize
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.8.6
# BuildRequires: rubygem(rspec) >= 3.0
# BuildRequires: rubygem(rspec) < 4
BuildArch: noarch

%description
filesize is a small class for handling filesizes with both the SI and binary
prefixes, allowing conversion from any size to any other size.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/



%check
pushd .%{gem_instdir}
# rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.1.1-1
- Initial package
