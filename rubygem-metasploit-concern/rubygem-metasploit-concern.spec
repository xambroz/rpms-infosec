# Generated from metasploit-concern-2.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name metasploit-concern

Name: rubygem-%{gem_name}
Version: 2.0.5
Release: 1%{?dist}
Summary: Automatically include Modules from app/concerns
License: BSD
URL: https://github.com/rapid7/metasploit-concern
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.0
# BuildRequires: rubygem(metasploit-yard)
# BuildRequires: rubygem(metasploit-erd)
BuildArch: noarch

%description
Automatically includes Modules from
app/concerns/<module_with_concerns>/<concern>.rb into <module_with_concerns>
to ease monkey-patching associations and validations on ActiveRecord::Base
descendents from other gems when layering schemas.


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

# Fix dependencies for activemodel/activerecord
sed -i -e 's|~> 4.2|>= 4.2|' %{gem_name}.gemspec

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
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 2.0.5-1
- Initial package
