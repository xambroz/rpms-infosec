# Generated from patch_finder-1.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name patch_finder

Name: rubygem-%{gem_name}
Version: 1.0.2
Release: 1%{?dist}
Summary: Patch Finder
License: BSD-3-clause
URL: http://github.com/wchen-r7/patch-finder
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(rspec) >= 3.0
# BuildRequires: rubygem(rspec) < 4
BuildArch: noarch

%description
Generic Patch Finder.


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
%{_bindir}/msu_finder
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/patch_finder.gemspec
%{gem_instdir}/tools
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docs

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 1.0.2-1
- Initial package
