# Generated from google-protobuf-3.5.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name google-protobuf

Name: rubygem-%{gem_name}
Version: 3.5.1.2
Release: 1%{?dist}
Summary: Protocol Buffers
License: BSD-3-Clause
URL: https://developers.google.com/protocol-buffers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc
# BuildRequires: rubygem(rake-compiler-dock) >= 0.6.0
# BuildRequires: rubygem(rake-compiler-dock) < 0.7
# BuildRequires: rubygem(rake-compiler) >= 0.9.5
# BuildRequires: rubygem(rake-compiler) < 0.10
# BuildRequires: rubygem(test-unit) >= 3.0
# BuildRequires: rubygem(test-unit) < 4
# BuildRequires: rubygem(test-unit) >= 3.0.9
# BuildRequires: rubygem(rubygems-tasks) >= 0.2.4
# BuildRequires: rubygem(rubygems-tasks) < 0.3

%description
Protocol Buffers are Google's data interchange format.


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

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/

mkdir -p %{buildroot}%{gem_extdir_mri}/google
cp -a .%{gem_extdir_mri}/google/*.so %{buildroot}%{gem_extdir_mri}/google/




# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/


%check
pushd .%{gem_instdir}
# ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/tests

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 3.5.1.2-1
- Initial package
