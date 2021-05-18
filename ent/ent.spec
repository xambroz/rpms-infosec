Name:           ent
Version:        20080128
Release:        1%{?dist}
Summary:        A pseudo-random number sequence test program

License:        GPLv2+
URL:            https://www.fourmilab.ch/random/
Source0:        https://www.fourmilab.ch/random/random.zip

BuildRequires:  unzip
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  sed


%description
Utility ent (as entropy) applies various tests to sequences of bytes stored
in files and reports the results of those tests. The program is useful for
evaluating pseudo-random number generators for encryption and statistical
sampling applications, compression algorithms, and other applications,
where the information density of a file is of interest.

%prep
%autosetup -c -n %{name}-%{version} -p 1
rm -f ent.exe

# Cut the license text from documetation to separate license file
sed '/<blockquote class="rights">/!d;
     s//&\n/;
     s/.*\n//;
     :a;
     /<\/blockquote>/bb;
     $!{n;ba};
     :b;
     s//\n&/;
     P;D' ent.html > license.txt

%build
%set_build_flags
%make_build


%install
install -d %{buildroot}%{_bindir}
install -m 755 ent %{buildroot}%{_bindir}


%check
make check

%files
%doc ent.html entitle.gif
%license license.txt
%{_bindir}/%{name}


%changelog
* Fri Jun 15 2018 Michal Ambroz <rebus AT seznam.cz> - 20080128-1
- initial build for Fedora 28
