# Generated from openvas-omp-0.0.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name openvas-omp

Name: rubygem-%{gem_name}
Version: 0.0.4
Release: 1%{?dist}
Summary: Communicate with OpenVAS manager through OMP
License: MIT
URL: http://github.com/kost/openvas-omp
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(shoulda)
# BuildRequires: rubygem(jeweler) >= 1.5.2
# BuildRequires: rubygem(jeweler) < 1.6
# BuildRequires: rubygem(rcov)
BuildArch: noarch

%description
Communicate with OpenVAS manager through OMP. 
This library is used for communication with OpenVAS manager over OMP.
You can start, stop, pause and resume scan. Watch progress and status of
scan, download report, etc.


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
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/TODO
%{gem_instdir}/VERSION
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/.document
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.0.4-1
- Initial package
