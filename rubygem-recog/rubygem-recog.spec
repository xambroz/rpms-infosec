# Generated from recog-2.1.18.gem by gem2rpm -*- rpm-spec -*-
%global gem_name recog

Name: rubygem-%{gem_name}
Version: 2.1.18
Release: 1%{?dist}
Summary: Network service fingerprint database, classes, and utilities
License: BSD
URL: https://www.github.com/rapid7/recog
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.1
# BuildRequires: rubygem(rspec)
# BuildRequires: rubygem(yard)
# BuildRequires: rubygem(redcarpet)
# BuildRequires: rubygem(cucumber)
# BuildRequires: rubygem(aruba)
# BuildRequires: rubygem(simplecov)
BuildArch: noarch

%description
Recog is a framework for identifying products, services, operating systems,
and hardware by matching fingerprints against data returned from various
network probes. Recog makes it simply to extract useful information from web
server banners, snmp system description fields, and a whole lot more.


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
# cucumber
# rspec spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/recog_export
%{_bindir}/recog_match
%{_bindir}/recog_verify
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%{gem_instdir}/misc
%exclude %{gem_instdir}/recog.gemspec
%{gem_instdir}/xml
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/.rspec
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/features
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 2.1.18-1
- Initial package
