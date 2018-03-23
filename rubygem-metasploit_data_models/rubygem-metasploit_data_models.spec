# Generated from metasploit_data_models-2.0.16.gem by gem2rpm -*- rpm-spec -*-
%global gem_name metasploit_data_models

Name: rubygem-%{gem_name}
Version: 2.0.16
Release: 1%{?dist}
Summary: Database code for MSF and Metasploit Pro
License: BSD
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.1
# BuildRequires: rubygem(metasploit-yard)
# BuildRequires: rubygem(yard-activerecord)
# BuildRequires: rubygem(yard-metasploit-erd)
# BuildRequires: rubygem(yard) < 0.8.7.4
# BuildRequires: rubygem(pry)
# BuildRequires: rubygem(redcarpet)
BuildArch: noarch

%description
Implements minimal ActiveRecord models and database helper code used in both
the Metasploit Framework (MSF) and Metasploit commercial editions.


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

# Fix dependencies for activemodel/activerecord/pg
sed -i -e 's|~> 4.2|>= 4.2|;
    s|<pg>.freeze, ."= 0.20|<pg>.freeze, [">= 0.20|' \
    %{gem_name}.gemspec

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
# Run the test suite.
popd

%files
%dir %{gem_instdir}
%{_bindir}/mdm_console
%{gem_instdir}/.coveralls.yml
%exclude %{gem_instdir}/.gitignore
%{gem_instdir}/.simplecov
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE
%{gem_instdir}/RELEASING.md
%{gem_instdir}/UPGRADING.md
%{gem_instdir}/app
%{gem_instdir}/bin
%{gem_instdir}/config
%{gem_instdir}/console_db.yml
%{gem_instdir}/db
%{gem_libdir}
%exclude %{gem_instdir}/metasploit_data_models.gemspec
%{gem_instdir}/script
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/.rspec
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 2.0.16-1
- Initial package
