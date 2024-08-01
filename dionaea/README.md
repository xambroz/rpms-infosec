# dionaea

Dionaea honeypot is low interaction honeypot, embedding python
as scripting language, using libemu to detect shell-codes, supporting
ipv6 and TLS.

## Dependencies
- libidn			https://src.fedoraproject.org/rpms/libidn
- loudmouth		https://src.fedoraproject.org/rpms/loudmouth
- udns			https://src.fedoraproject.org/rpms/udns
- libev			https://src.fedoraproject.org/rpms/libev
- python3-bson		https://src.fedoraproject.org/rpms/python-pymongo
- libdasm			https://src.fedoraproject.org/rpms/libdasm
- libemu			https://src.fedoraproject.org/rpms/libemu

## Packages
- dionaea
- python3-dionaea
- dionaea-doc

## Known issues
- p0f - the p0f API used in upstream dionaea code is currently (2024) referring to version 2.* of p0f,
  while we have version 3.* in Fedora. Configuring p0f interface to dionaea in /etc/dionaea/services-enabled/p0f.yaml currently results in severe segfaults especially when blackhole module is used for handling a port.

