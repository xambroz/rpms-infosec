# Generated from rspec-rerun-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rspec-rerun

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 1%{?dist}
Summary: Re-run failed RSpec tests
License: MIT
URL: https://github.com/dblock/rspec-rerun
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(rubocop) = 0.31.0
# BuildRequires: rubygem(bump)
BuildArch: noarch

%description
Re-run failed RSpec tests.


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
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.1.0-1
- Initial package
