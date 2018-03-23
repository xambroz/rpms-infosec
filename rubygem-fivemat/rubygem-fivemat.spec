# Generated from fivemat-1.3.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fivemat

Name: rubygem-%{gem_name}
Version: 1.3.6
Release: 1%{?dist}
Summary: Why settle for a test output format when you could have a test output fivemat?
License: MIT
URL: https://github.com/tpope/fivemat
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
MiniTest/RSpec/Cucumber formatter that gives each test file its own line of
dots.


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
# Run the test suite.
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%license %{gem_instdir}/LICENSE
%license %{gem_instdir}/MIT-LICENSE
%exclude %{gem_instdir}/fivemat.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.3.6-1
- Initial package
