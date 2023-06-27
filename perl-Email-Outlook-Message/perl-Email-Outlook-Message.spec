Name:           perl-Email-Outlook-Message
Version:        0.921
Release:        1%{?dist}
Summary:        Read Outlook .msg files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Email-Outlook-Message
Source0:        https://cpan.metacpan.org/modules/by-module/Email/Email-Outlook-Message-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Email::Address)
BuildRequires:  perl(Email::MIME)		>= 1.923
BuildRequires:  perl(Email::MIME::ContentType)	>= 1.014
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:  perl(Email::Sender)
%else
BuildRequires:  perl(Email::Sender)             >= 1.3
%endif
BuildRequires:  perl(Email::Simple)		>= 2.206
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::All)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(OLE::Storage_Lite)         >= 0.14
BuildRequires:  perl(POSIX)
# Test Suite
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(version) > 0.99
# Release Tests
BuildRequires:  perl(Test::Pod::Coverage)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Parses .msg message files as produced by Microsoft Outlook.


%prep
%setup -q -n Email-Outlook-Message-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}


%check

# Ignore test results on RHEL7
# RHEL7 having older versions of dependencies

%if 0%{?rhel} && 0%{?rhel} == 7
make test || true
%else
make test
%endif


%files
%license README
%doc CHANGELOG TODO
%{_bindir}/msgconvert
%{perl_vendorlib}/Email/
%{_mandir}/man1/msgconvert.1*
%{_mandir}/man3/Email::Outlook::Message::AddressInfo.3*
%{_mandir}/man3/Email::Outlook::Message::Attachment.3*
%{_mandir}/man3/Email::Outlook::Message::Base.3*
%{_mandir}/man3/Email::Outlook::Message.3*


%changelog
* Fri Feb 18 2022 Michal Ambroz <rebus AT_ seznam.cz> - 0.921-1
- bump to 0.921

* Thu Apr 08 2021 Michal Ambroz <rebus AT_ seznam.cz> - 0.920-1
- initial package
