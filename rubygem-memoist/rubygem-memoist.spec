# Generated from memoist-0.16.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name memoist

Name: rubygem-%{gem_name}
Version: 0.16.0
Release: 1%{?dist}
Summary: memoize methods invocation
License: MIT
URL: https://github.com/matthewrudy/memoist
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(benchmark-ips)
# BuildRequires: rubygem(minitest) >= 5.10
# BuildRequires: rubygem(minitest) < 6
BuildArch: noarch

%description
memoize methods invocation.


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
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_instdir}/memoist.gemspec
%{gem_instdir}/script
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.16.0-1
- Initial package
