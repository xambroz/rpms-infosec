Name:           microsoft-repositories
Version:        38
Release:        1%{?dist}
Summary:        Microsoft Repository files for searchable repositories
License:        MIT
URL:            https://learn.microsoft.com/en-us/linux/packages
VCS:            https://github.com/xambroz/rpms-infosec/tree/master/microsoft-repositories


# based on:
# https://packages.microsoft.com/rhel/9/prod/Packages/p/packages-microsoft-prod.rpm
# https://packages.microsoft.com/config/fedora/38/prod.repo
# Microsoft is compiling majority of the interesting packages (like azurecli or powershell)
# for rhel, just some for Fedora
# so adding repositories for current Fedora + RHEL9/8/7
Source0:        https://packages.microsoft.com/keys/microsoft.asc#/RPM-GPG-KEY-microsoft.asc
Source1:        https://repo.skype.com/data/SKYPE-GPG-KEY#/RPM-GPG-KEY-microsoft-SKYPE.asc
Source2:        microsoft-repositories.conf
Source3:        microsoft-azure-cli.repo
Source4:        microsoft-azurecore.repo
Source5:        microsoft-cyclecloud.repo
Source6:        microsoft-edge.repo
Source7:        microsoft-mssql.repo
Source8:        microsoft-prod.repo
Source9:        microsoft-skype.repo
Source10:       microsoft-teams.repo
Source11:       microsoft-vscode.repo

%description
Respositories for linux software from Microsoft to be used with gnome-software
or dnf/yum installation
Example:
dnf search teams --enablerepo=microsoft*

%prep

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
cp %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg

%ifarch x86_64
mkdir -p %{buildroot}%{_prefix}/lib/fedora-third-party/conf.d
cp %{SOURCE2} %{buildroot}%{_prefix}/lib/fedora-third-party/conf.d/

mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE5} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE6} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE7} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE8} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE10} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE11} %{buildroot}%{_sysconfdir}/yum.repos.d/
%endif


%files
%ifarch x86_64
%{_sysconfdir}/yum.repos.d/microsoft-*.repo
%{_prefix}/lib/fedora-third-party/conf.d/microsoft-repositories.conf
%endif
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-microsoft.asc
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-microsoft-SKYPE.asc

%changelog
* Sun Nov 05 2023 Michal Ambroz <rebus _AT seznam.cz> - 38-1
- initial package