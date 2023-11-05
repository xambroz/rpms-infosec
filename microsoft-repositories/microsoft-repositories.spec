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
Source2:        microsoft-azure-cli.repo
Source3:        microsoft-azurecore.repo
Source4:        microsoft-cyclecloud.repo
Source5:        microsoft-edge.repo
Source6:        microsoft-mssql.repo
Source7:        microsoft-prod.repo
Source8:        microsoft-skype.repo
Source9:        microsoft-teams.repo
Source10:        microsoft-vscode.repo

%description
Respositories for linux software from Microsoft to be used with gnome-software
or dnf/yum installation
Example:
dnf search teams --enablerepo=microsoft*

%prep

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

%ifarch x86_64
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE5} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE6} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE7} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE8} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/yum.repos.d/
cp %{SOURCE10} %{buildroot}%{_sysconfdir}/yum.repos.d/
%endif
mkdir -p %{buildroot}%{_prefix}/lib/fedora-third-party/conf.d
cp microsoft-repositories.conf %{buildroot}%{_prefix}/lib/fedora-third-party/conf.d/
%files
%{_sysconfdir}/yum.repos.d/microsoft-*.repo
%{_prefix}/lib/fedora-third-party/conf.d/microsoft-repositories.conf
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-microsoft.asc
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-microsoft-SKYPE.asc

%changelog
* Sun Nov 05 2023 Michal Ambroz <rebus _AT seznam.cz> - 38-1
- initial package