# Generated from windows_error-0.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name windows_error

Name: rubygem-%{gem_name}
Version: 0.1.2
Release: 1%{?dist}
Summary: Provides a way to look up Windows NTSTATUS and Win32 Error Codes
License: BSD
URL: https://github.com/rapid7/windows_error
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.0
# BuildRequires: rubygem(yard)
# BuildRequires: rubygem(fivemat)
BuildArch: noarch

%description
The WindowsError gem provides an easily accessible reference for
standard Windows API Error Codes. It allows you to do comparisons
as well as direct lookups of error codes to translate the numerical
value returned by the API, into a meaningful and human readable message.


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
%{gem_instdir}/.pullreview.yml
%{gem_instdir}/.simplecov
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_instdir}/windows_error.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/.rspec
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Wed Mar 14 2018 Michal Ambroz <rebus at, seznam.cz> - 0.1.2-1
- Initial package
