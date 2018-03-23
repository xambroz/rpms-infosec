# Generated from metasploit-payloads-1.3.31.gem by gem2rpm -*- rpm-spec -*-
%global gem_name metasploit-payloads

# Libraries here are used as a data payload for external systems, not for this one
%define _binaries_in_noarch_packages_terminate_build   0

Name: rubygem-%{gem_name}
Version: 1.3.31
Release: 1%{?dist}
Summary: This gem contains the compiled binaries required to make Meterpreter function, and eventually other payloads that require compiled binaries
License: 3-clause (or "modified") BSD
URL: http://www.metasploit.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.0
# BuildRequires: rubygem(gem-release)
BuildArch: noarch

%description
Compiled binaries for Metasploit's Meterpreter.


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
%{gem_instdir}/data
%{gem_libdir}
%exclude %{gem_instdir}/metasploit-payloads.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.3.31-1
- Initial package
