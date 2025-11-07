# Generated from wpscan-3.8.25.gem by gem2rpm -*- rpm-spec -*-
%global gem_name wpscan

Name: rubygem-%{gem_name}
Version: 3.8.25
Release: 1%{?dist}
Summary: WPScan - WordPress Vulnerability Scanner
License: Dual
URL: https://wpscan.com/wordpress-security-scanner
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.7
# BuildRequires: rubygem(memory_profiler) >= 1.0.0
# BuildRequires: rubygem(memory_profiler) < 1.1
# BuildRequires: rubygem(rspec) >= 3.12.0
# BuildRequires: rubygem(rspec) < 3.13
# BuildRequires: rubygem(rspec-its) >= 1.3.0
# BuildRequires: rubygem(rspec-its) < 1.4
# BuildRequires: rubygem(rubocop) >= 1.26.0
# BuildRequires: rubygem(rubocop) < 1.27
# BuildRequires: rubygem(rubocop-performance) >= 1.13.0
# BuildRequires: rubygem(rubocop-performance) < 1.14
# BuildRequires: rubygem(simplecov) >= 0.21.0
# BuildRequires: rubygem(simplecov) < 0.22
# BuildRequires: rubygem(simplecov-lcov) >= 0.8.0
# BuildRequires: rubygem(simplecov-lcov) < 0.9
# BuildRequires: rubygem(stackprof) >= 0.2.12
# BuildRequires: rubygem(stackprof) < 0.3
# BuildRequires: rubygem(webmock) >= 3.19.1
# BuildRequires: rubygem(webmock) < 3.20
BuildArch: noarch

%description
WPScan is a black box WordPress vulnerability scanner.


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


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# rspec spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/wpscan
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Tue Jan 16 2024 Michal Ambroz <rebus@seznam.cz> - 3.8.25-1
- Initial package
