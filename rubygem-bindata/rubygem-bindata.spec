# Generated from bindata-2.4.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bindata

Name: rubygem-%{gem_name}
Version: 2.4.3
Release: 1%{?dist}
Summary: A declarative way to read and write binary file formats
License: Ruby
URL: http://github.com/dmendel/bindata
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(minitest) > 5.0.0
# BuildRequires: rubygem(coveralls)
BuildArch: noarch

%description
BinData is a declarative way to read and write binary file formats.
This means the programmer specifies *what* the format of the binary
data is, and BinData works out *how* to read and write data in this
format.  It is an easier ( and more readable ) alternative to
ruby's #pack and #unpack methods.


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
# ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_instdir}/BSDL
%license %{gem_instdir}/COPYING
%{gem_instdir}/INSTALL
%exclude %{gem_instdir}/bindata.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog.rdoc
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/NEWS.rdoc
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 2.4.3-1
- Initial package
