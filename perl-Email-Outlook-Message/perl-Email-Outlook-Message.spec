Name:           perl-Email-Outlook-Message
Version:        0.920
Release:        1%{?dist}
Summary:        Read Outlook .msg files
License:        GPL+ or Artistic
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
BuildRequires:  perl(Email::MIME)		>= 1.926
BuildRequires:  perl(Email::MIME::ContentType)	>= 1.014
BuildRequires:  perl(Email::Sender)
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
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}


%check
make test


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
* Thu Apr 08 2021 Michal Ambroz <rebus AT_ seznam.cz> - 0.920-1
- initial package
