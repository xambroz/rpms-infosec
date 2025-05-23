%define debug_package %{nil}

Summary:	Simultaneously perform an MD5 and SHA1 checksum on files

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		2hash
Version:	0.2
Release:	1%{?dist}
URL:		http://trog.qgl.org/20061027/2hash-simultaneous-md5-and-sha1-hashing

License:	GPL

Group:		Applications/Forensics Tools

Source0:	https://trog.qgl.org/download.php/%{name}-v%{version}.tar.gz
BuildRequires:	gcc-c++
BuildRequires:	libstdc++-devel
%if 0%{?fedora} >= 8
BuildRequires:	glibc-static
%endif
%if 0%{?rhel} >= 6
BuildRequires:	glibc-static
%endif
%if 0%{?rhel} == 5
BuildRequires:	glibc-devel
%endif
BuildRoot:	%{buildroot}

%description
2hash simultaneously performs a md5 and a sha1 checksum on file(s).
If you want two checksums for additionally integrity checking, you previously
had to run md5sum and sha1sum serially causing the integrity checks to 
take 100% longer than running a single check alone. 2hash runs both hashes 
in parallel, only having to read the file once. It allows you to 
get both hash values with only about an 8% time increase over md5 alone, 
and only about a 2% time increase over sha1 alone. It runs about 90%
quicker than using both md5 and sha1 one after the other... 

%prep
%setup -n %{name}-v%{version}


%build
%{__make}

%install
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc INSTALL README
%attr(555,bin,bin)	%{_bindir}/2hash

%changelog
