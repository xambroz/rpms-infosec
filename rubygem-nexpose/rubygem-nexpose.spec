# Generated from nexpose-7.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name nexpose

Name: rubygem-%{gem_name}
Version: 7.2.0
Release: 1%{?dist}
Summary: Ruby API for Rapid7 Nexpose
License: BSD
URL: https://github.com/rapid7/nexpose-client
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.1
# BuildRequires: rubygem(codeclimate-test-reporter) >= 0.4.6
# BuildRequires: rubygem(codeclimate-test-reporter) < 0.5
# BuildRequires: rubygem(simplecov) >= 0.9.1
# BuildRequires: rubygem(simplecov) < 0.10
# BuildRequires: rubygem(rspec) >= 3.2
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(rubocop)
# BuildRequires: rubygem(webmock) >= 1.20.4
# BuildRequires: rubygem(webmock) < 1.21
# BuildRequires: rubygem(vcr) >= 2.9.3
# BuildRequires: rubygem(vcr) < 2.10
# BuildRequires: rubygem(github_changelog_generator)
# BuildRequires: rubygem(pry) = 0.9.12.6
BuildArch: noarch

%description
This gem provides a Ruby API to the Nexpose vulnerability management product
by Rapid7.


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
%license %{gem_instdir}/COPYING
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 7.2.0-1
- Initial package
