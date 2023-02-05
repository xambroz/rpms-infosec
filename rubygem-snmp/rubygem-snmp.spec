%global gem_name snmp

Name:           rubygem-%{gem_name}
Version:        1.3.2
Release:        7%{?dist}
Summary:        A Ruby implementation of SNMP (the Simple Network Management Protocol)
License:        MIT
URL:            https://github.com/hallidave/ruby-snmp
VCS:            https://github.com/hallidave/ruby-snmp
# GEM           https://rubygems.org/gems/snmp/
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem(minitest)
BuildArch:      noarch

%if 0%{?el7}
Provides:       rubygem(%{gem_name}) = %{version}
%endif



%description
A Ruby implementation of SNMP (the Simple Network Management Protocol).


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

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
# Do not run check on EPEL7, Minitest is lacking Test method there
%if !0%{?el7}
pushd .%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd
%endif

%files
%dir %{gem_instdir}
%{gem_instdir}/data
%{gem_libdir}
%license %{gem_instdir}/README.rdoc
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Sun Feb 05 2023 Michal Ambroz <rebus _AT seznam.cz> - 1.3.2-7
- fix EPEL7 build

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Vít Ondruch <vondruch@redhat.com> - 1.3.2-1
- Update to snmp 1.3.2.
  Resolves: rhbz#1722616

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Vít Ondruch <vondruch@redhat.com> - 1.2.0-4
- Fix unstable TestVarBind#test_integer_create_from_string test.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 10 2014 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0 as per 1120178

* Mon Jul 14 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Update to snmp 1.1.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.0-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.0-4
- Fix broken dependencies.

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.0-3
- Rebuilt for Ruby 1.9.3.

* Sun Jan 08 2012 <stahnma@fedoraproject.org> - 1.1.0-2
- Ensure %%check can run properly

* Sun Jan 08 2012 <stahnma@fedoraproject.org> - 1.1.0-1
- Fix FTBFS bug  715639

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 10 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.0.3-1
- New version

* Mon May 24 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.0.2-1
- Fixes from review bug #587438
- Initial package
