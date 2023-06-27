# TODO

Name:           spike
Version:        2.9
Release:        1%{?dist}
Summary:        fuzzer

License:        GPL-2.0-only
#Was URL:       http://www.immunitysec.com/resources-freesoftware.shtml
URL:            https://web.archive.org/web/20141103111846/http://www.immunitysec.com:80/resources-freesoftware.shtml

# http://www.immunitysec.com/downloads/SPIKE2.9.tgz
# Archive
# https://web.archive.org/web/20140622211021/http://www.immunitysec.com/downloads/SPIKE2.9.tgz
Source0:        https://web.archive.org/web/20140622211021/http://www.immunitysec.com/downloads/SPIKE2.9.tgz
Patch0:         spike-001-makefile.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf

#Requires:       

%description
Network protocol fuzer, usefull for identifying for buffer overflows or similar weaknesses.
Requires a strong knowledge of C to use, but produces significant results.


%prep
%autosetup -n SPIKE -p 1

# Fix structure
cd SPIKE
mv * ../
cd ..


# Fix permissions
find ./ -type f -exec chmod -x '{}' ';'

chmod +x src/configure
mv src/configure.in src/configure.ac

# Remove pre-compiled binaries in the src
cd src
rm -f cifs plonk smtp_send_tcp webmitm

rm aclocal.m4 configure



%build
cd src
aclocal
automake --add-missing
autoupdate
autoreconf
%configure
%make_build
# make cifs


%install
pushd src
%make_install
popd

mkdir -p %{buildroot}%{_datadir}/spike/
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}


cp -p -r src/audits %{buildroot}%{_datadir}/spike/
cp -p -r src/testscripts %{buildroot}%{_datadir}/spike/
cp -p -r src/*.spk %{buildroot}%{_datadir}/spike/
cp -p -r  backups %{buildroot}%{_datadir}/spike/
cp -p -r data %{buildroot}%{_datadir}/spike/
cp -p -r dcedump %{buildroot}%{_datadir}/spike/
cp -p -r include %{buildroot}%{_datadir}/spike/
cp -p src/libdlrpc.so %{buildroot}%{_libdir}/
cp -p src/citrix %{buildroot}%{_bindir}/
cp -p src/closed_source_web_server_fuzz %{buildroot}%{_bindir}/
cp -p src/dceoversmb %{buildroot}%{_bindir}/
cp -p src/dltest %{buildroot}%{_bindir}/
cp -p src/do_post %{buildroot}%{_bindir}/
cp -p src/generic_chunked %{buildroot}%{_bindir}/
cp -p src/generic_listen_tcp %{buildroot}%{_bindir}/
cp -p src/generic_send_tcp %{buildroot}%{_bindir}/
cp -p src/generic_send_udp %{buildroot}%{_bindir}/
cp -p src/generic_web_server_fuzz %{buildroot}%{_bindir}/
cp -p src/generic_web_server_fuzz2 %{buildroot}%{_bindir}/
cp -p src/gopherd %{buildroot}%{_bindir}/
cp -p src/halflife %{buildroot}%{_bindir}/
cp -p src/line_send_tcp %{buildroot}%{_bindir}/
cp -p src/msrpcfuzz %{buildroot}%{_bindir}/
cp -p src/msrpcfuzz_udp %{buildroot}%{_bindir}/
cp -p src/ntlm2 %{buildroot}%{_bindir}/
cp -p src/ntlm_brute %{buildroot}%{_bindir}/
cp -p src/pmspike %{buildroot}%{_bindir}/
cp -p src/post_fuzz %{buildroot}%{_bindir}/
cp -p src/post_spike %{buildroot}%{_bindir}/
cp -p src/quake %{buildroot}%{_bindir}/
cp -p src/quakeserver %{buildroot}%{_bindir}/
cp -p src/sendmsrpc %{buildroot}%{_bindir}/
cp -p src/ss_spike %{buildroot}%{_bindir}/
cp -p src/statd_spike %{buildroot}%{_bindir}/
cp -p src/sunrpcfuzz %{buildroot}%{_bindir}/
cp -p src/webfuzz %{buildroot}%{_bindir}/
cp -p src/x11_spike %{buildroot}%{_bindir}/



%files
%license GPL.txt
%doc documentation README.txt CHANGELOG.txt
%doc src/README.* src/*.txt
%{_bindir}/*
%{_libdir}/
%{_datadir}/spike/


%changelog
* Sat Feb 11 2023 Michal Ambroz <rebus@seznam.cz>
- 
