Name:           python-markupsafe
Version:        2.0.1
Release:        0%{?dist}
Summary:        Implements a XML/HTML/XHTML Markup safe string for Python
License:        BSD
URL:            https://github.com/pallets/markupsafe
Source0:        %{url}/archive/%{version}/MarkupSafe-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
This package installs test- and docs-requirements from files
and uses them to run tests and build documentation.
It also has a less common order of the %%files section.


%package -n python3-markupsafe
Summary:        %{summary}

%description -n python3-markupsafe
...


# In this spec, we put %%files early to test it still works
%files -n python3-markupsafe -f %{pyproject_files}
%license LICENSE.rst
%doc CHANGES.rst README.rst


%prep
%autosetup -n markupsafe-%{version}

# we don't have pip-tools packaged in Fedora yet
sed -i /pip-tools/d requirements/dev.in

# help the macros understand the URL in requirements/docs.in
sed -Ei 's/sphinx\.git@([0-9a-f]+)/sphinx.git@\1#egg=sphinx/' requirements/docs.in


%generate_buildrequires
# requirements/dev.in recursively includes tests.in and docs.in
# we also list tests.in manually to verify we can pass multiple arguments,
# but it should be redundant if this was a real package
%pyproject_buildrequires requirements/dev.in requirements/tests.in


%build
%pyproject_wheel
%make_build -C docs html SPHINXOPTS='-n %{?_smp_mflags}'


%install
%pyproject_install
%pyproject_save_files markupsafe


%check
%pytest

