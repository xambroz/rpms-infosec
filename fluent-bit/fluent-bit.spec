Name:           fluent-bit
Summary:        Fast and Lightweight Log processor and forwarder for Linux, BSD and OSX
Version:        1.7.4
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://fluentbit.io
Source0:        https://github.com/fluent/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Package contains several bundled libraries
# TODO - version review
# TODO - unbundle what is possible
# https://avro.apache.org/ - avro package retired in Fedora
Provides:       bundled(avro) = 1.10.0
Provides:       bundled(chunkio) = 1.1.1
Provides:       bundled(flb_libco)
Provides:       bundled(jansson) = 2.13.1
Provides:       bundled(jemalloc) = 5.2.1
# jsmn - commit 053d3cd29200edb1bfd181d917d140c16c1f8834.
Provides:       bundled(jsmn)
Provides:       bundled(libbacktrace)
Provides:       bundled(luajit) = 2.1.0
Provides:       bundled(mbedtls) = 2.24.0
Provides:       bundled(miniz)
Provides:       bundled(monkey)
Provides:       bundled(mpack)
Provides:       bundled(msgpack-c)
Provides:       bundled(onigmo)
Provides:       bundled(rbtree)
Provides:       bundled(sqlite) = 3.33.0
Provides:       bundled(tutf8e)
Provides:       bundled(xxHash) = 0.8.0


# TODO - License review
# ASL 2.0 - ./LICENSE
#           ./lib/mbedtls-2.24.0/LICENSE
#           ./lib/mpack-amalgamation-1.0/LICENSE
#           ./lib/jansson-fd3e9e3/LICENSE
#           ./lib/libbacktrace-ca0de05/LICENSE
#           ./lib/tutf8e/LICENSE
#           ./lib/jsmn/LICENSE
#           ./lib/monkey/mk_core/deps/libevent/LICENSE
#           ./lib/monkey/LICENSE
#           ./lib/miniz/LICENSE
# ASL 2.0 - ./lib/avro/LICENSE
#           ./lib/xxHash-0.8.0/LICENSE
# ASL 2.0 - ./lib/chunkio/LICENSE 
#           ./lib/chunkio/tests/lib/acutest/LICENSE.md
#           ./lib/chunkio/cmake/sanitizers-cmake/LICENSE
#           ./tests/lib/shunit2/LICENSE
#           ./tests/internal/data/signv4/aws-sig-v4-test-suite/LICENSE
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.hdrhistogram
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.crc32c
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.tinycthread
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSES.txt
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.lz4
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.snappy
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.pycrc
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.wingetopt
#           ./plugins/out_kafka/librdkafka-1.6.0/packaging/cmake/Modules/LICENSE.FindZstd
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.fnv1a
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.regexp
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.queue
#           ./plugins/out_kafka/librdkafka-1.6.0/LICENSE.murmur2
#           ./plugins/filter_geoip2/libmaxminddb/LICENSE
#           ./cmake/sanitizers-cmake/LICENSE


BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
# librdkafka jemalloc and some cmake tests need c++
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(jansson)


%description
Fluent Bit is a fast Log Processor and Forwarder for Linux, Embedded Linux, MacOS and BSD 
family operating systems. It's part of the Fluentd Ecosystem and a CNCF sub-project.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%autosetup -p 1 -n "%{name}-%{version}"

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFLB_PROXY_GO=Off
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_sysconfdir}/fluent-bit
%{_unitdir}/fluent-bit.service

%files devel
%{_includedir}/%{name}
%{_libdir}/fluent-bit/*.so

%changelog
* Thu Apr 22 2021 Florian Dubourg <florian.dubourg@dhl.com> 1.7.4-1
- Original version for DHL
