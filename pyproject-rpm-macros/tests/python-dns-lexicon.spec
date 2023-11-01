Name:           python-dns-lexicon
Version:        3.8.1
Release:        0%{?dist}
Summary:        Manipulate DNS records on various DNS providers in a standardized/agnostic way
License:        MIT
URL:            https://github.com/AnalogJ/lexicon
Source0:        %{url}/archive/v%{version}/lexicon-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel

# Upstream does not declare this dependency
# They dropped it later: https://github.com/AnalogJ/lexicon/issues/1240
BuildRequires:  python3-pkg_resources

%description
This package has extras specified in tox configuration,
we test that the extras are installed when -e is used.
This package also uses a custom toxenv and creates several extras subpackages.


%package -n     python3-dns-lexicon
Summary:        %{summary}

%description -n python3-dns-lexicon
...


%pyproject_extras_subpackage -n python3-dns-lexicon plesk route53


%prep
%autosetup -n lexicon-%{version}
# The tox configuration lists a [dev] extra, but that installs nothing (is missing).
# The test requirements are only specified via poetry.dev-dependencies.
# Here we amend the data a bit so we can test more things, adding the tests deps to the dev extra:
sed -i \
's/\[tool.poetry.extras\]/'\
'pytest = {version = ">3", optional = true}\n'\
'vcrpy = {version = ">1", optional = true}\n\n'\
'[tool.poetry.extras]\n'\
'dev = ["pytest", "vcrpy"]/' pyproject.toml


%generate_buildrequires
# We use the "light" toxenv because the default one installs the [full] extra and we don't have all the deps.
# Note that [full] contains [plesk] and [route53] but we specify them manually instead:
%pyproject_buildrequires -e light -x plesk -x route53


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files lexicon


%check
# we cannot use %%tox here, because the configured commands call poetry directly :/
# we use %%pytest instead, running a subset of tests not to waste CI time
%pytest -k "test_route53 or test_plesk"


%files -n python3-dns-lexicon -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{_bindir}/lexicon
