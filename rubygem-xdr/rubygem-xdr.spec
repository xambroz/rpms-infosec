# Generated from xdr-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name xdr

Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 1%{?dist}
Summary: XDR Helper Library
License: Apache 2.0
URL: https://github.com/stellar/ruby-xdr
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.0
# BuildRequires: rubygem(rspec) >= 3.1
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(guard-rspec)
# BuildRequires: rubygem(simplecov)
BuildArch: noarch

%description
XDR Helper Library.


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
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.yardopts
%{gem_instdir}/Guardfile
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_instdir}/xdr.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 2.0.0-1
- Initial package
