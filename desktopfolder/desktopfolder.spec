Name:		desktopfolder
Version:	1.1.3
Summary:	alternative gnome menu

%global gituser 
%global gitname Gnomenu
%global commit	44700a14fc6042168c50cf1ac46b46fd6e758e62
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%global gitdate	20200420
%global fgittag	.git%{gitdate}.%{shortcommit}
%global extdir		gnomenupanacier.gmail.com
%global gschemadir	%{_datadir}/glib-2.0/schemas

Release:	1%{?fgittag:.%{fgittag}}%{?dist}

License:GPL-2.0-only
URL:		https://github.com/The-Panacea-Projects/Gnomenu
%if 0%{?shortcommit:1}
Source0:	https://github.com/The-Panacea-Projects/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz#/%{name}-v%{version}-%{gitdate}-%{shortcommit}.tar.gz
%else
Source0:	https://github.com/The-Panacea-Projects/%{name}/archive/v%{version}.tar.gz#/%{name}-v%{version}.tar.gz
%endif


BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	intltool
BuildRequires:	vala
BuildRequires:	glib2-devel
BuildRequires:	gtk3-devel
BuildRequires:	cairo-devel
BuildRequires:	json-glib-devel
BuildRequires:	libwnck3-devel
BuildRequires:	libgee-devel
BuildRequires:	gtksourceview3-devel
BuildRequires:	

BuildRequires:	%{_bindir}/glib-compile-schemas

Requires:	gnome-shell-extension-common

%description
Gno-Menu is a traditional styled full featured Gnome-Shell apps menu, that aims to offer all the essentials in a simple uncluttered intuitive interface.

%prep
%autosetup %{?commit:-n %{name}-%{commit}}

%build
./update-locale.sh
glib-compile-schemas --strict --targetdir=%{extdir}/schemas/ %{extdir}/schemas

%install
mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions
cp -ar %{extdir} %{buildroot}%{_datadir}/gnome-shell/extensions/%{extdir}
%find_lang %{name} --all-name

# Fedora and EPEL 8 handles post scripts via triggers
%if 0%{?rhel} && 0%{?rhel} <= 7
%postun
if [ $1 -eq 0 ] ; then
	%{_bindir}/glib-compile-schemas %{gschemadir} &> /dev/null || :
fi

%posttrans
%{_bindir}/glib-compile-schemas %{gschemadir} &> /dev/null || :
%endif

%files -f %{name}.lang
%license COPYING
%{_datadir}/gnome-shell/extensions/%{extdir}

%changelog
* Wed Feb 08 2023 Jeremy Newton <alexjnewt at hotmail dot com> - 44-1
- Update to v44

* Mon Jan 30 2023 Jeremy Newton <alexjnewt at hotmail dot com> - 43-1
- Update to v43

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 15 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 42-1
- Update to v42

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 39-4.20220331.git2394e7f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 31 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 39-3.20220331.git2394e7f
- Update to git snapshot to fix f36

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 30 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 39-1
- Update to v39

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Jeremy Newton <alexjnewt at hotmail dot com> - 38-1
- Update to v38

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 10 2021 Jeremy Newton <alexjnewt at hotmail dot com> - 37-1
- Initial package
