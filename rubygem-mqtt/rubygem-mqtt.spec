# Generated from mqtt-0.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mqtt

Name: rubygem-%{gem_name}
Version: 0.5.0
Release: 1%{?dist}
Summary: Implementation of the MQTT protocol
License: MIT
URL: http://github.com/njh/ruby-mqtt
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(yard) >= 0.8.7
# BuildRequires: rubygem(rspec) >= 3.5.0
# BuildRequires: rubygem(simplecov) >= 0.9.2
BuildArch: noarch

%description
Pure Ruby gem that implements the MQTT protocol, a lightweight protocol for
publish/subscribe messaging.


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
%license %{gem_instdir}/LICENSE.md
%{gem_instdir}/NEWS.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.5.0-1
- Initial package
