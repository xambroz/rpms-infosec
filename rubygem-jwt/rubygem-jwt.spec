# Generated from jwt-2.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name jwt

Name: rubygem-%{gem_name}
Version: 2.1.0
Release: 1%{?dist}
Summary: JSON Web Token implementation in Ruby
License: MIT
URL: http://github.com/jwt/ruby-jwt
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.1
# BuildRequires: rubygem(rspec)
# BuildRequires: rubygem(simplecov)
# BuildRequires: rubygem(simplecov-json)
# BuildRequires: rubygem(codeclimate-test-reporter)
# BuildRequires: rubygem(codacy-coverage)
# BuildRequires: rubygem(rbnacl)
BuildArch: noarch

%description
A pure ruby implementation of the RFC 7519 OAuth JSON Web Token (JWT)
standard.


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
%{gem_instdir}/.codeclimate.yml
%{gem_instdir}/.ebert.yml
%exclude %{gem_instdir}/.gitignore
%{gem_instdir}/.reek.yml
%exclude %{gem_instdir}/.rubocop.yml
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE
%{gem_instdir}/Manifest
%{gem_libdir}
%exclude %{gem_instdir}/ruby-jwt.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/.rspec
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 2.1.0-1
- Initial package
