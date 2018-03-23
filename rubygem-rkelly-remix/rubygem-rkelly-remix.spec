# Generated from rkelly-remix-0.0.7.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rkelly-remix

Name: rubygem-%{gem_name}
Version: 0.0.7
Release: 1%{?dist}
Summary: RKelly Remix is a fork of the RKelly[https://github.com/tenderlove/rkelly] JavaScript parser
License: MIT
URL: https://github.com/nene/rkelly-remix
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(hoe) >= 3.13
# BuildRequires: rubygem(hoe) < 4
BuildArch: noarch

%description
RKelly Remix is a fork of the
RKelly[https://github.com/tenderlove/rkelly] JavaScript parser.


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
%exclude %{gem_instdir}/.gemtest
%{gem_instdir}/Manifest.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.0.7-1
- Initial package
