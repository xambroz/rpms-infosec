# Generated from rex-nop-0.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rex-nop

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 1%{?dist}
Summary: Ruby Exploitation(REX) library for NOP generation
License: BSD
URL: https://github.com/rapid7/rex-nop
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.0
# BuildRequires: rubygem(rspec) >= 3.0
# BuildRequires: rubygem(rspec) < 4
BuildArch: noarch

%description
This library contains the opty2 library for dynamic generation of x86
multi-byte NOPs.
This is useful in writing exploits and encoders. It allows you to dynamic
generate variable
length instruction sets that are equivalent to a No Operation(NOP) without
using
the actual 0x90 bytecode. The original code was written by Optyx and spoonm. .


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
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_instdir}/CODE_OF_CONDUCT.md
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/rex-nop.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/.rspec
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.1.1-1
- Initial package
