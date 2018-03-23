# Generated from signet-0.8.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name signet

Name: rubygem-%{gem_name}
Version: 0.8.1
Release: 1%{?dist}
Summary: Signet is an OAuth 1.0 / OAuth 2.0 implementation
License: Apache-2.0
URL: https://github.com/google/signet/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.5
BuildRequires: ruby >= 1.9.3
# BuildRequires: rubygem(yard) >= 0.8
# BuildRequires: rubygem(yard) < 1
# BuildRequires: rubygem(rspec) >= 3.1
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(launchy) >= 2.4
# BuildRequires: rubygem(launchy) < 3
# BuildRequires: rubygem(kramdown) >= 1.5
# BuildRequires: rubygem(kramdown) < 2
# BuildRequires: rubygem(simplecov) >= 0.9
# BuildRequires: rubygem(simplecov) < 1
BuildArch: noarch

%description
Signet is an OAuth 1.0 / OAuth 2.0 implementation.


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
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_instdir}/signet.gemspec
%{gem_instdir}/tasks
%{gem_instdir}/website
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.8.1-1
- Initial package
