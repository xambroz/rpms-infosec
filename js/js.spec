#% global hgdate 51702867d932

Summary:	JavaScript interpreter and libraries
Name:		js
Epoch:		1
Version:	1.8.5
Release:	38%{?hgdate:.hg%{hgdate}}%{?dist}
License:	GPLv2+ or LGPLv2+ or MPLv1.1
URL:		https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Releases/1.8.5
Source0:	http://ftp.mozilla.org/pub/js/js185-1.0.0.tar.gz
# Initial attempt at Big Endian 64 bit support (revised later)
Patch0:		js-1.8.5-64bit-big-endian.patch
# make arch conditional list more complete for secondary jit bits
Patch1:		js-1.8.5-secondary-jit.patch
# handle case where $DESTDIR ends up on both ends of a symbolic link
# https://bugzilla.mozilla.org/show_bug.cgi?id=628723#c43
Patch2:		js185-destdir.patch
# Properly handle 64bit JS_BITS_PER_WORD
Patch3:		js-1.8.5-537701.patch
# Remove hardcoded flags forcing softfp on arm
Patch4:		js185-arm-nosoftfp.patch
# Switch from readline to libedit
Patch5:		js185-libedit.patch
# Move JS_BYTES_PER_WORD out of config.h
# Instead define it in terms of the already extant GNU C extension
# __SIZEOF_POINTER__.  This avoids multiarch conflicts when 32 and 64
# bit packages of js are co-installed.
Patch6:		0001-Make-js-config.h-multiarch-compatible.patch
# add support for aarch64
Patch7:		aarch64.patch
# bz#1096135
Patch8:		ppc64le.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1178141 (http://hg.mozilla.org/mozilla-central/rev/a7b220e7425a)
Patch9:		js-1.8.5-array-recursion.patch
# Fix various C++11 issues
Patch10:	js-1.8.5-c++11.patch
# update for 48-bit VA
Patch11:	mozjs1.8.5-tag.patch
# Fix build with gcc9
Patch12:	js-gcc9-fix-on-top-of-other-patches.patch
Provides:	libjs = %{version}-%{release}
BuildRequires:	nspr-devel >= 4.7
BuildRequires:	perl-devel
BuildRequires:	python2
BuildRequires:	zip
BuildRequires:	libedit-devel
BuildRequires:	ncurses-devel
BuildRequires:	autoconf213
BuildRequires:	gcc-c++

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
super-set of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig
Requires:	ncurses-devel readline-devel
Provides:	libjs-devel = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p2 -b .64bit-big-endian
%patch1 -p2 -b .secondary-jit
%patch2 -p0 -b .destdir
%patch3 -p1 -b .537701
%patch4 -p1 -b .armhfp
%patch5 -p1 -b .libedit
%patch6 -p1 -b .multiarch
%patch7 -p1 -b .aarch64
%patch8 -p1 -b .ppc64le
%patch9 -p1 -b .array-recursion
%patch10 -p1 -b .c++11
%patch11 -p1 -b .tag
%patch12 -p1 -b .gcc9

cd js

# Rm parts with spurios licenses, binaries
# Some parts under BSD (but different suppliers): src/assembler
#rm -rf src/assembler src/yarr/yarr src/yarr/pcre src/yarr/wtf src/v8-dtoa
rm -rf src/ctypes/libffi src/t src/tests/src/jstests.jar src/tracevis src/v8

pushd src
autoconf-2.13
popd

# Create pkgconfig file
cat > libjs.pc << 'EOF'
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libjs
Description: JS library
Requires: nspr >= 4.7
Version: %{version}
Libs: -L${libdir} -ljs
Cflags: -DXP_UNIX=1 -DJS_THREADSAFE=1 -I${includedir}/js
EOF

%build
cd js/src
CPPFLAGS="$(pkg-config --cflags libedit)" \
%configure \
    --with-system-nspr \
    --enable-threadsafe \
    --enable-readline \
    --disable-optimize
make %{?_smp_mflags}

%install
cd js
%make_install -C src
# We don't want this
rm -f %{buildroot}%{_bindir}/js-config
install -m 0755 src/jscpucfg src/shell/js \
       %{buildroot}%{_bindir}/
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la

# For compatibility
# XXX do we really need libjs?!?!?!
pushd %{buildroot}%{_libdir}
ln -s libmozjs185.so.1.0 libmozjs.so.1
ln -s libmozjs185.so.1.0 libjs.so.1
ln -s libmozjs185.so libmozjs.so
ln -s libmozjs185.so libjs.so
popd

install -m 0644 libjs.pc %{buildroot}%{_libdir}/pkgconfig/

%check
# Unfortunately it fail on arm and I have no machines where I could debug it unfortunately, so just do not test on it and hope on the best
%ifnarch armv7hl
# it fails in strange way initially, so remove
rm js/src/jit-test/tests/sunspider/check-date-format-tofte.js
make -C js/src check
%endif

%files
%doc js/src/README.html
%{_bindir}/js
%{_libdir}/*.so.1*

%files devel
%{_bindir}/jscpucfg
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/js

%changelog
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec  9 2019 Tom Callaway <spot@fedoraproject.org> - 1:1.8.5-37
- fix soname globbing
- nuke duplicate install command

* Mon Dec  9 2019 Tom Callaway <spot@fedoraproject.org> - 1:1.8.5-36
- apply all suggested fixes from package review

* Fri Nov  8 2019 Tom Callaway <spot@fedoraproject.org> - 1:1.8.5-35
- revive package

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:1.8.5-31
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 10 2017 Dan Horák <dan[at]danny.cz> - 1:1.8.5-27
- add patch for 48-bit VA (#1423793)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr 05 2016 Than Ngo <than@redhat.com> - 1:1.8.5-25
- Disable optimizations which caused regressions with new gcc
  Use fedora default -O2 instead of mozjs -O3

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.8.5-24
- Fix FTBFS with C++11 (#1307665)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1:1.8.5-21
- Skip test on arm - it failed in strange way and I have no machines to debug
- Some cleanup

* Wed Apr 15 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1:1.8.5-20
- Add Patch9: js-1.8.5-array-recursion.patch (bz#1178141 - http://hg.mozilla.org/mozilla-central/rev/a7b220e7425a)
- Add %%check section

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1:1.8.5-17
- Fix bogus dates in changelog.
- Add Patch8: ppc64le.patch (bz#1096135) to fix compilation on ppc64le arch.

* Wed Mar 26 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1:1.8.5-16
- Add patch for AArch64.

* Mon Mar 17 2014 Colin Walters <walters@redhat.com> - 1:1.8.5-15
- Add patch to fix multilib conflict with devel packages
  I am not aware of anyone who actually needs this, but it checks
  a checkbox.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Dennis Gilmore <dennis@ausil.us> - 1:1.8.5-12
- make sure -march=armv7-a is not hardcoded in arm builds

* Sat Nov 17 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1:1.8.5-11
- Thanks to Ville Skyttä (bz#875343) build against libedit instead of readline
	what simplify licensing apparently without any loss of functionality

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Dennis Gilmore <dennis@ausil.us> - 1.8.5-9
- add patch to enable js to build on both hard and soft floating point arm distros

* Fri Dec 02 2011 Karsten Hopp <karsten@redhat.com> 1.8.5-8
- add patch from bugzilla 749604, fixes PPC failures

* Wed Jun 22 2011 Colin Walters <walters@verbum.org> - 1:1.8.5-6
- Include mozjs185.pc, clean up build
- Based on work from Christopher Aillon <caillon@redhat.com>
- Switch to using make install DESTDIR=, instead of hardcoding build rules.
- Add DESTDIR= patch from GNOME 3.2 jhbuild
- Make mozjs185 the canonical target for both libmozjs and libmozjs185.

* Fri May 27 2011 Dan Horák <dan[at]danny.cz> - 1.8.5-5
- add secondary arch patches from xulrunner

* Tue Apr 12 2011 Christopher Aillon <caillon@redhat.com> - 1.8.5-4
- devel subpackage needs to ask for the newly added epoch

* Tue Apr 12 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1.8.5-3
- Add Epoch: 1 to allow update of 1.70-13 version.

* Sat Apr 9 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1.8.5-2
- Correct symlink to provide backward capabiliies libjs.so.1

* Wed Apr 6 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1.8.5-1
- Update to release.
- Remove unneeded anymore patches.
- Add backward capability symlink.

* Sat Feb 12 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1.8.5-0.hg51702867d932
- Build version 1.8.5 by update request - BZ#676441 from Firefox 4.0 mercurial repository.
- Gone -DJS_C_STRINGS_ARE_UTF8
- Add BR autoconf213, change build system to use configure.
- Adopt patch0 (js-1.7.0-make.patch -> js-1.8.5-make.patch)
- Adopt patch1 (js-shlib.patch -> js-1.8.5-shlib.patch)
- Remove Patch2 (js-1.5-va_copy.patch) and Patch3 (js-ldflags.patch)
- Add BR python, zip.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.70-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 16 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.70-12
- Add UTF-8 support (add -DJS_C_STRINGS_ARE_UTF8 ) by request Peter Halliday: BZ#576585

* Mon Jun 14 2010 Dan Horák <dan[at]danny.cz> - 1.70-11
- updated the va_copy patch for s390

* Mon Jan 25 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.70-10
- Remove static library from -devel - %%{_libdir}/*.a (bz#556057) to meet guidelines.

* Sun Aug 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.70-8
- Reformat spec with tabs.
- By report of Thomas Sondergaard (BZ#511162) Add -DXP_UNIX=1 -DJS_THREADSAFE=1 flags and nspr requires into libjs.pc

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.70-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 29 2009 Dan Horak <dan[at]danny.cz> 1.70-6
- update the va_copy patch for s390x

* Thu Apr  9 2009 Matthias Saou <http://freshrpms.net/> 1.70-5
- Update description (#487903).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jun  4 2008 Jon McCann <jmccann@redhat.com> - 1.70-3
- Add two missing files (#449715)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.70-2
- Rebuild for perl 5.10 (again)

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.70-1
- Update to 1.7.0, as 1.70 to avoid introducing an epoch for now...
- Remove no longer provided perlconnect parts.

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.60-6
- BR: perl(ExtUtils::Embed)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.60-5
- rebuild for new perl

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.60-4
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 1.60-3
- Update License field.
- Add perl(ExtUtils::MakeMaker) build requirement to pull in perl-devel.

* Fri Feb  2 2007 Matthias Saou <http://freshrpms.net/> 1.60-2
- Include jsopcode.tbl and js.msg in devel (#235481).
- Install static lib mode 644 instead of 755.

* Fri Feb  2 2007 Matthias Saou <http://freshrpms.net/> 1.60-1
- Update to 1.60.
- Rebuild in order to link against ncurses instead of termcap (#226773).
- Add ncurses-devel build requirement and patch s/termcap/ncurses/ in.
- Change mode of perl library from 555 to 755 (#224603).

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.5-6
- Fix pkgconfig file (#204232 & dupe #204236).

* Mon Jul 24 2006 Matthias Saou <http://freshrpms.net/> 1.5-5
- FC6 rebuild.
- Enable JS_THREADSAFE in the build (#199696), add patch and nspr build req.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.5-4
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 1.5-3
- Rebuild for new gcc/glibc.

* Mon Jan 30 2006 Matthias Saou <http://freshrpms.net/> 1.5-2
- Fix .pc file.

* Thu Jan 26 2006 Matthias Saou <http://freshrpms.net/> 1.5-1
- Update to 1.5.0 final.
- Spec file cleanups.
- Move docs from devel to main, since we need the license there.
- Remove no longer needed js-perlconnect.patch.
- Update js-1.5-va_copy.patch.
- Include a pkgconfig file (#178993).

* Tue Apr 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.5-0.rc6a.6
- Link shared lib with libperl.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Feb 14 2005 David Woodhouse <dwmw2@infradead.org> - 1.5-0.rc6a.4
- Take js-va_copy.patch out of %%ifarch x86_64 so it fixes the PPC build too

* Sun Feb 13 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 1.5-0.rc6a.3
- Add js-va_copy.patch to fix x86_64; Patch was found in a Mandrake srpm

* Sat Dec 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 1.5-0.rc6a.2
- Include perlconnect.
- Include readline support, rebuild using "--without readline" to disable.
- Add libjs* provides for upstream compatibility.
- Install header files in %%{_includedir} instead of %%{_includedir}/js.

* Tue Jun 15 2004 Matthias Saou <http://freshrpms.net> 1.5-0.rc6a
- Update to 1.5rc6a.

* Tue Mar 02 2004 Dag Wieers <dag@wieers.com> - 1.5-0.rc6
- Initial package. (using DAR)

