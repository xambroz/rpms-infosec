Name:           dc3dd
Version:        7.2.646
Release:        16%{?dist}
Summary:        Patched version of GNU dd for use in computer forensics

License:        GPL-3.0-or-later
URL:            http://sourceforge.net/projects/dc3dd/
Source0:        http://downloads.sourceforge.net/dc3dd/%{name}-%{version}.7z

#Fixing build error: automatic de-ANSI-fication support has been removed
#Removing the check for AM_C_PROTOTYPES
Patch1:         dc3dd-01_automake.patch

# Original Archlinux patch to fix build with recent libtools version
# Author: mschlenker
Patch2:         dc3dd-02_fix-FTBFS-with-glibc-2.28.patch


BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  gnulib-devel
BuildRequires:  perl(Locale::gettext)
BuildRequires:  perl(I18N::Langinfo)
BuildRequires:  p7zip
BuildRequires:  m4, readline-devel, autoconf, automake
BuildRequires:  make

%description
dc3dd is a patched version of GNU dd to include a number of features useful
for computer forensics. Many of these features were inspired by dcfldd, but
were rewritten for dc3dd.

* Pattern writes. The program can write a single hexadecimal value or a
    text string to the output device for wiping purposes.
* Piecewise and overall hashing with multiple algorithms and variable 
    size windows. Supports MD5, SHA-1, SHA-256, and SHA-512. Hashes can be 
    computed before or after conversions are made.
* Progress meter with automatic input/output file size probing
* Combined log for hashes and errors
* Error grouping. Produces one error message for identical sequential 
    errors
* Verify mode. Able to repeat any transformations done to the input 
    file and compare it to an output.
* Ability to split the output into chunks with numerical or alphabetic 
    extensions


%prep
%autosetup -S git

#Missing x flag in version 7.2.646 makes the build fail
chmod +x build-aux/git-version-gen configure

# ChangeLog having wrong ends of lines
sed -i -e 's|\r||g' ChangeLog


%build
autoreconf -vif #BZ925238 - support aarch64
# TODO check the --enable-hdparm option
%configure 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc ABOUT-NLS AUTHORS ChangeLog README README.coreutils THANKS THANKS-to-translators TODO Sample_Commands.txt NEWS Options_Reference.txt
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*

%changelog
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 19 2021 Michal Ambroz <rebus [AT] seznam.cz> - 7.2.646-13
- add dependency to perl(I18N::Langinfo) to fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 28 2019 Michal Ambroz <rebus [AT] seznam.cz> - 7.2.646-9
- License change to GPLv3+ (the lib/getdate.c is no longer gplv2+)

* Sun Oct 20 2019 Michal Ambroz <rebus [AT] seznam.cz> - 7.2.646-8
- use Archlinux patch to fix FTBFS, do not update gnulib embedded library files

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 28 2018 Michal Ambroz <rebus [AT] seznam.cz> - 7.2.646-6
- fix FTBFS, update gnulib embedded library files

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.646-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Michal Ambroz <rebus [AT] seznam.cz> - 7.2.646-1
- bump to 7.2.646

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.641-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 02 2016 Michal Ambroz <rebus [AT] seznam.cz> - 7.2.641-1
- bump to 7.2.641
- add BR for Locale::gettext

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.614-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.614-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.614-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.614-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 22 2013 Michal Ambroz <rebus [AT] seznam.cz> - 7.1.614-6
- Fix the build issue with new automake

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.614-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 7.1.614-4
- Fix BZ 925238 - rerun autoconf to add support for aarch64

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.614-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.614-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Adam Miller <maxamillion@fedoraproject.org> - 7.1.614-1
- Update to upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.12.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 10 2009 Adam Miller <maxamillion [AT] gmail.com> - 6.12.3-3
- Fixed Source0 listing as reported https://www.redhat.com/archives/fedora-devel-list/2009-August/msg00591.html

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 19 2009 Adam Miller <maxamillion [AT] gmail.com> - 6.12.3-1
- New release of dc3dd

* Thu Mar 05 2009 Adam Miller <maxamillion [AT] gmail.com> - 6.12.2-3
- Cleaned up the .spec by looping through files needing EOF encoding fix

* Mon Mar 02 2009 Adam Miller <maxamillion [AT] gmail.com> - 6.12.2-2
- Removed .gmo binaries, fixed source0, added doc items, fixed EOF encoding
- fixed licencing listing

* Mon Feb 23 2009 Adam Miller <maxamillion [AT] gmail.com> - 6.12.2-1
- First build of dc3dd for fedora
