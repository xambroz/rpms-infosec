Name:           scalpel
Version:        2.1
Summary:        Fast file carver working on disk images


%global         gituser         sleuthkit
%global         gitname         scalpel
%global         gitdate         20210326
%global         commit          35e1367ef2232c0f4883c92ec2839273c821dd39
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease -p -e rc2 -s %{shortcommit}

License:        GPL-2.0-or-later
URL:            https://github.com/sleuthkit/scalpel
VCS:            git:%{url}
Source0:        %{url}/archive/%{commit}/%{name}-%{version}-git%{gitdate}-%{shortcommit}.tar.gz

BuildRequires:  make
BuildRequires:  gcc-c++
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
export CXXFLAGS="-std=c++14 $RPM_OPT_FLAGS"
./bootstrap
%configure --with-pic
%make_build


%install
%make_install

mkdir -p %{buildroot}/%{_sysconfdir}
install -m 644 %{name}.conf %{buildroot}/%{_sysconfdir}/

rm -f  %{buildroot}/%{_libdir}/libscalpel*.a
rm -f  %{buildroot}/%{_libdir}/libscalpel*.la


%check
# dummy check
./scalpel -h | grep -e "Verbose mode" > /dev/null


%files
%doc README Changelog
%license LICENSE-2.0.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/libscalpel_test
%{_mandir}/man1/%{name}.1*
%{_libdir}/libscalpel*.so*


%changelog
%autochangelog
