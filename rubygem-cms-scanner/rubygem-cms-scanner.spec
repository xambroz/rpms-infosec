# Generated from cms_scanner-0.13.9.gem by gem2rpm -*- rpm-spec -*-
%global gem_name cms_scanner

Name: rubygem-%{gem_name}
Version: 0.13.9
Release: 1%{?dist}
Summary: CMS Scanner Framework (experimental)
License: MIT
URL: https://github.com/wpscanteam/CMSScanner
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.7
# BuildRequires: rubygem(rspec) >= 3.12.0
# BuildRequires: rubygem(rspec) < 3.13
# BuildRequires: rubygem(rspec-its) >= 1.3.0
# BuildRequires: rubygem(rspec-its) < 1.4
# BuildRequires: rubygem(rubocop) >= 1.26.0
# BuildRequires: rubygem(rubocop) < 1.27
# BuildRequires: rubygem(rubocop-performance) >= 1.18.0
# BuildRequires: rubygem(rubocop-performance) < 1.19
# BuildRequires: rubygem(simplecov) >= 0.22.0
# BuildRequires: rubygem(simplecov) < 0.23
# BuildRequires: rubygem(simplecov-lcov) >= 0.8.0
# BuildRequires: rubygem(simplecov-lcov) < 0.9
# BuildRequires: rubygem(webmock) >= 3.18.1
# BuildRequires: rubygem(webmock) < 3.19
BuildArch: noarch

%description
Framework to provide an easy way to implement CMS Scanners.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

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
%{gem_instdir}/app
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Tue Jan 16 2024 Michal Ambroz <rebus@seznam.cz> - 0.13.9-1
- Initial package
