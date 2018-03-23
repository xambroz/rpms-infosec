# Generated from packetfu-1.1.13.gem by gem2rpm -*- rpm-spec -*-
%global gem_name packetfu

Name: rubygem-%{gem_name}
Version: 1.1.13
Release: 1%{?dist}
Summary: PacketFu is a mid-level packet manipulation library
License: BSD
URL: https://github.com/packetfu/packetfu
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.1.0
# BuildRequires: rubygem(rspec)
# BuildRequires: rubygem(rspec-its)
# BuildRequires: rubygem(sdoc)
# BuildRequires: rubygem(pry)
# BuildRequires: rubygem(coveralls)
BuildArch: noarch

%description
PacketFu is a mid-level packet manipulation library for Ruby. With
it, users can read, parse, and write network packets with the level of
ease and fun they expect from Ruby.
.


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
%{gem_instdir}/.mailmap
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/bench
%{gem_instdir}/gem-public_cert.pem
%{gem_libdir}
%exclude %{gem_instdir}/packetfu.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/.document
%exclude %{gem_instdir}/.rspec
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/spec
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.1.13-1
- Initial package
