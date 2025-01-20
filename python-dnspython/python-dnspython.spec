Name:           python-dnspython
Version:        2.4.2
Release:        %autorelease
Summary:        DNS toolkit

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        ISC
URL:            https://www.dnspython.org
Source:         %{pypi_source dnspython}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'dnspython' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-dnspython
Summary:        %{summary}

%description -n python3-dnspython %_description

# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
# %%pyproject_extras_subpkg -n python3-dnspython dnssec,doh,doq,idna,trio,wmi
%pyproject_extras_subpkg -n python3-dnspython dnssec


%prep
%autosetup -p1 -n dnspython-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
# %%pyproject_buildrequires -x dnssec,doh,doq,idna,trio,wmi
%pyproject_buildrequires -x dnssec


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


%check
%pyproject_check_import


%files -n python3-dnspython -f %{pyproject_files}


%changelog
%{?%autochangelog: %autochangelog }