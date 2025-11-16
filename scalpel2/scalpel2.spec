Name:           scalpel2
Version:        2.2
Epoch:          2
Summary:        Fast file carver working on disk images


%global         gituser         nolaforensix
%global         gitname         scalpel-2.02
%global         gitdate         20240111
%global         commit          3dd1cacd0abf00973eec4ded1b5dec1cad27d1ef
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease -s %{gitdate}git%{shortcommit}

License:        GPL-2.0-or-later
URL:            https://github.com/nolaforensix/scalpel-2.02
VCS:            git:%{url}
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  tre-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
%ifarch %{java_arches}
BuildRequires:  java-devel
%endif

%description
Scalpel is a fast file carver that reads a database of header and footer
definitions and extracts matching files from a set of image files or raw
device files. Scalpel is independent on used file-system and will carve
files from FATx, NTFS, ext2/3, or raw partitions. It is useful for both
digital forensics investigation and file recovery.


%prep
%autosetup -n %{gitname}-%{commit}

# Remove Windows binary files
rm -rf *.exe *.dll

# Modify conf to have some usable configuration out of the box
# In upstream distribution configuration everything is commented out
# Sed script will uncomment common file extensions
sed -i -e "s/^#[ ]*$//;
           s/\t/        /g;
           s/^#   [ ]*\([a-z][a-z] \)/        \1/;
           s/^#   [ ]*\([a-z][a-z][a-z] \)/        \1/;
           s/^#   [ ]*\([a-z][a-z][a-z][a-z] \)/        \1/;
           s/^\(.*case[ ]*size\)/#\1/" %{name}.conf



%build
autoreconf -f -i
%configure --with-pic
make clean
%make_build V=1


%install
%make_install

mkdir -p %{buildroot}/%{_sysconfdir}
install -m 644 %{name}.conf %{buildroot}/%{_sysconfdir}/

rm -f  %{buildroot}/%{_libdir}/libscalpel*.a
rm -f  %{buildroot}/%{_libdir}/libscalpel*.la


%check
# dummy check
src/scalpel2 -h | grep -e "Verbose mode" > /dev/null


%files
%doc README.md Changelog
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
%autochangelog
