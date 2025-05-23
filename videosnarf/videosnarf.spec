%define debug_package %{nil}

Summary:	Output detected media sessions

Packager:	Lawrence R. Rogers (lrr@cert.org)

Vendor:		cert.org
Name:		videosnarf
Version:	0.63
Release:	1%{?dist}
URL:		http://ucsniff.sourceforge.net/videosnarf.html

License:	GPL

Group:		Applications/Forensics Tools
Source:		%{name}-%{version}.tar.gz
Patch1:		%{name}-%{version}-patch-001

BuildRoot:	%{_tmppath}/rpm-root-%{name}-v%{version}
BuildRequires:	libnet-devel libpcap-devel
BuildRequires:	gcc-c++
Requires:	libnet libpcap

%description
VideoSnarf is a new security assessment tool that takes an offline
pcap as input, and outputs any detected media streams (RTP sessions),
including common audio codecs as well as H264 Video support. Why did we
write VideoSnarf? To give security assessment professionals options to
decode media traffic other than forcing them to use UCSniff. We know that
some people, for whatever reason, might not be using UCSniff to capture
and decode VoIP/Video traffic. For example, some people might want to
use Ettercap and their favorite Sniffer (tshark/Wireshark) to capture
the traffic, or they might have a monitor SPAN Session and are running
a dedicated sniffer and want to re-construct the traffic just using a
pcap trace file. VideoSnarf was inspired by the rtpbreak tool. To our
knowledge, it is the first tool to detect RTP sessions that are encoded
with the H.264 Video Codec, and output raw H264 files. VideoSnarf
also supports the following common audio codecs: G711ulaw, G711alaw,
G722, G729, G723, and G726. These are the most common audio codecs
found in enterprise networks where you are going to be doing security
assessments.

%prep
%setup -q
%patch1 -p1

%build
%configure
%{__make}

%install
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%attr(555, bin, bin)	%{_bindir}/%{name}

%changelog
