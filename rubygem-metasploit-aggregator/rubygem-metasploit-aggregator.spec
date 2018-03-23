# Generated from metasploit-aggregator-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name metasploit-aggregator

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 1%{?dist}
Summary: metasploit-aggregator
License: BSD-3-Clause
URL: https://www.msf.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.0
# BuildRequires: rubygem(pry)
# BuildRequires: rubygem(rspec) >= 3.0
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(grpc-tools)
BuildArch: noarch

%description
metasploit-aggregator.


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


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# rspec spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/metasploit-aggregator
%{gem_instdir}/.ruby-gemset
%{gem_instdir}/.ruby-version
%exclude %{gem_instdir}/.travis.yml
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/metasploit-aggregator.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/.rspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.0.0-1
- Initial package
