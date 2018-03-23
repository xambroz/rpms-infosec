# Generated from nessus_rest-0.1.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name nessus_rest

Name: rubygem-%{gem_name}
Version: 0.1.6
Release: 1%{?dist}
Summary: Communicate with Nessus Scanner (version 6+) over REST/JSON interface
License: MIT
URL: https://github.com/kost/nessus_rest-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(pry)
# BuildRequires: rubygem(yard)
BuildArch: noarch

%description
Ruby library for Nessus (version 6+) JSON/REST interface. This library is used
for communication with Nessus over REST interface. You can start, stop, pause
and resume scan. Watch progress and status of scan, download report, etc. .


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
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/VERSION
%{gem_libdir}
%exclude %{gem_instdir}/nessus_rest.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/.document
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.1.6-1
- Initial package
