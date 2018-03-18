# Generated from grpc-1.10.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name grpc

Name:           rubygem-%{gem_name}
Version:        1.10.0
Release:        1%{?dist}
Summary:        GRPC system in Ruby
License:        Apache-2.0
URL:            https://github.com/google/grpc/tree/master/src/ruby
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0:         rubygem-grpc-format.patch
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby-devel >= 2.0.0
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc
# BuildRequires: rubygem(facter) >= 2.4
# BuildRequires: rubygem(facter) < 3
# BuildRequires: rubygem(logging) >= 2.0
# BuildRequires: rubygem(logging) < 3
# BuildRequires: rubygem(simplecov) >= 0.14.1
# BuildRequires: rubygem(simplecov) < 0.15
# BuildRequires: rubygem(rake-compiler) >= 1.0
# BuildRequires: rubygem(rake-compiler) < 2
# BuildRequires: rubygem(rake-compiler-dock) >= 0.5.1
# BuildRequires: rubygem(rake-compiler-dock) < 0.6
# BuildRequires: rubygem(rspec) >= 3.6
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(rubocop) >= 0.49.1
# BuildRequires: rubygem(rubocop) < 0.50
# BuildRequires: rubygem(signet) >= 0.7.0
# BuildRequires: rubygem(signet) < 0.8

%description
Send RPCs from Ruby using GRPC.


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

%patch0 -p 1 -b .format

%build
# Create the gem as gem install only works on a gem file
export STRIP=true GRPC_CONFIG=dbg
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
export STRIP=true GRPC_CONFIG=dbg
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}

mkdir -p %{buildroot}%{gem_extdir_mri}/grpc
cp -a .%{gem_extdir_mri}/grpc/*.so %{buildroot}%{gem_extdir_mri}/grpc

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/src/


%check
pushd .%{gem_instdir}
# rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%exclude %{gem_instdir}/.yardopts
%{gem_instdir}/Makefile
%{gem_instdir}/etc
%{gem_instdir}/include
%{gem_instdir}/third_party
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.10.0-1
- Initial package
