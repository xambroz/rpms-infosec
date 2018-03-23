# Generated from metasm-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name metasm

Name: rubygem-%{gem_name}
Version: 1.0.3
Release: 1%{?dist}
Summary: Metasm is a cross-architecture assembler, disassembler, linker, and debugger
License: LGPL
URL: http://metasm.cr0.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
Metasm is a cross-architecture assembler, disassembler, linker, and debugger.


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
%{gem_instdir}/.hgtags
%{gem_instdir}/BUGS
%{gem_instdir}/CREDITS
%{gem_instdir}/INSTALL
%license %{gem_instdir}/LICENCE
%{gem_instdir}/TODO
%exclude %{gem_instdir}/metasm.gemspec
%{gem_instdir}/metasm.rb
%{gem_instdir}/metasm
%{gem_instdir}/misc
%{gem_instdir}/samples
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/doc
%{gem_instdir}/tests

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.0.3-1
- Initial package
