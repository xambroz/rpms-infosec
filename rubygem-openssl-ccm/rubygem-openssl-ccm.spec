# Generated from openssl-ccm-1.2.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name openssl-ccm

Name: rubygem-%{gem_name}
Version: 1.2.1
Release: 1%{?dist}
Summary: RFC 3610 - CCM
License: MIT
URL: https://github.com/smalllars/openssl-ccm
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.0.0
# BuildRequires: rubygem(yard) >= 0.8
# BuildRequires: rubygem(yard) < 1
# BuildRequires: rubygem(yard) >= 0.8.7.6
# BuildRequires: rubygem(rubocop) >= 0.34
# BuildRequires: rubygem(rubocop) < 1
# BuildRequires: rubygem(rubocop) >= 0.34.2
# BuildRequires: rubygem(test-unit) >= 3.1
# BuildRequires: rubygem(test-unit) < 4
# BuildRequires: rubygem(test-unit) >= 3.1.4
# BuildRequires: rubygem(coveralls) >= 0.8
# BuildRequires: rubygem(coveralls) < 1
# BuildRequires: rubygem(coveralls) >= 0.8.2
BuildArch: noarch

%description
Ruby Gem for RFC 3610 - Counter with CBC-MAC (CCM).


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
# ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.rubocop.yml
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.2.1-1
- Initial package
