# Generated from postgres_ext-3.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name postgres_ext

Name: rubygem-%{gem_name}
Version: 3.0.0
Release: 1%{?dist}
Summary: Extends ActiveRecord to handle native PostgreSQL data types
License: MIT
URL: https://github.com/dockyard/postgres_ext
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(minitest)
# BuildRequires: rubygem(m)
# BuildRequires: rubygem(bourne) >= 1.3.0
# BuildRequires: rubygem(bourne) < 1.4
# BuildRequires: rubygem(database_cleaner)
# BuildRequires: rubygem(dotenv)
# BuildRequires: rubygem(pg) >= 0.13
# BuildRequires: rubygem(pg) < 1
BuildArch: noarch

%description
Adds missing native PostgreSQL data types to ActiveRecord and convenient
querying extensions for ActiveRecord and Arel.


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
%{gem_instdir}/gemfiles
%{gem_libdir}
%exclude %{gem_instdir}/postgres_ext.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docs
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 3.0.0-1
- Initial package
