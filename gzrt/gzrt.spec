Name:           gzrt
Group:          System Environment/Libraries
License:        LGPLv3+
Version:        0.8
Summary:        Recover data from a corrupted gzip file
URL:            https://github.com/arenn/gzrt

%global         gitdate         20131002
%global         gituser         arenn
%global         gitname         gzrt
%global         commit          d8ff007856652403b595669a821b0097b60d4854
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:		gzrt-debug.patch


%description
Recover data from a corrupted gzip file


%prep
%autosetup -n %{gitname}-%{commit}


%build
CFLAGS="$CFLAGS -ggdb"
export CFLAGS
%make_build


%install
install -d -p %{buildroot}%{_bindir}
install -D -p -m 755 gzrecover %{buildroot}%{_bindir}/gzrecover

install -d -p %{buildroot}/%{_mandir}/man1
install -D -p -m 644 gzrecover.1 %{buildroot}%{_mandir}/man1/gzrecover.1


%files
%doc README ChangeLog
%{_bindir}/gzrecover
%{_mandir}/man1/gzrecover.*


%changelog
%{?%autochangelog: %autochangelog }
