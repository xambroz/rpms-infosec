# Generated from os-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name os

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 1%{?dist}
Summary: Simple and easy way to know if you're on windows or not (reliably), as well as how many bits the OS is, etc
License: BSD
URL: http://github.com/rdp/os
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(rspec) >= 2.0
BuildArch: noarch

%description
The OS gem allows for some useful and easy functions, like OS.windows? (=>
true or false) OS.bits ( => 32 or 64) etc".


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
%{gem_instdir}/.autotest
%license %{gem_instdir}/LICENSE
%{gem_instdir}/VERSION
%{gem_instdir}/autotest
%{gem_libdir}
%exclude %{gem_instdir}/os.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/.document
%doc %{gem_instdir}/ChangeLog
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.0.0-1
- Initial package
