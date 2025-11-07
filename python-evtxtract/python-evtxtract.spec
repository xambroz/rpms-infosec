Name:           python-evtxtract
Version:        0.2.4
Release:        %autorelease
License:        APLv2
Summary:        Recover and reconstruct fragments of EVTX log files from raw binary data
URL:            https://github.com/williballenthin/EVTXtract
VCS:            git:%{url}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/evtxtract-0.2.4.tar.gz

# Fix version
# code released as 0.2.4 was still presenting itself as 0.2.3
Patch0:         https://github.com/williballenthin/EVTXtract/pull/25.patch#/%{name}-0.2.4-version.patch


%global         origname        EVTXtract
%global         lname %(echo %{origname} | tr '[A-Z]' '[a-z]')
%global         common_description %{expand:
EVTX records are XML fragments encoded using a Microsoft-specific binary XML
representation. Despite the convenient format, it is not easy to recover EVTX event log records
from a corrupted file or unallocated space. This is because the complete representation of a
record often depends on other records found nearby. The event log service recognizes similarities
among records and refactors commonalities into "templates". A template is a fixed structure with
placeholders that reserve space for variable content. The on-disk event log record structure
is a reference to a template, and a list of substitutions (the variable content the replaces
a placeholder in a template). To decode a record into XML, the event log service resolves the
template and replaces its placeholders with the entries of the substitution array. Therefore,
template corruption renders many records unrecoverable within the local 64KB "chunk". However,
the substitution array for the remaining records may still be intact. If so, it may be
possible to produce XML fragments that match the original records if the damaged template can
be reconstructed. For many common events, such as process creation or account logon, empirical
testing demonstrates the relevant templates remain mostly constant. In these cases, recovering
event log records boils down to identifying appropriate templates found in other EVTX chunks.

Algorithm

 1. Scan for chunk signatures ("ElfChnk")
    a. check header for sane values (0x80 <= size <= 0x200)
    b. verify checksums (header, data)
 2. Extract records from valid chunks found in (1)
 3. Extract templates from valid chunks found in (1)
 4. Scan for record signatures
    a. check header for sane values
    a. extract timestamp
    c. attempt to parse substitutions
    d. attempt to decode substitutions into EID, other fields
 5. Reconstruct records by reusing old templates with recovered substitutions
}

%description %{common_description}

%package -n     python%{python3_pkgversion}-evtxtract
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-evtxtract}

%description -n python%{python3_pkgversion}-evtxtract
%common_description

# Provide also the upstream name of the github repository with upper-case letters
%py_provides %{python3_pkgversion}-EVTXtract


%prep
%autosetup -p 1 -n %{origname}-%{version}


%build
#%%pyproject_wheel


%install
#%%pyproject_install


%check
%tox


%files -n python%{python3_pkgversion}-evtxtract
%license LICENSE.TXT
%{python3_sitelib}/evtxtract
%{python3_sitelib}/evtxtract-*.dist-info
%{_bindir}/evtxtract


%changelog
%autochangelog
