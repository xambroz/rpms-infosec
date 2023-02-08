#!/usr/bin/bash -eu

if [ $# -ne 1 ]; then
  echo "Usage: ./vendor_meta.sh pip-10.0.0/src/pip/_vendor/vendor.txt"
  exit 1
fi

licenses=''

while read req; do
  req=$(echo $req | cut -f1 -d' ')
  name=$(echo $req | cut -f1 -d'=')
  version=$(echo $req | cut -f3 -d'=' | tr -d '\r')
  echo "Provides: bundled(python%{1}dist($name)) = $version"
  license="$(pyp2rpm -v ${version} --no-venv ${name} | grep '^License:' | sed -e 's/License:\s*//')"
  licenses="$licenses\n$name: $license"
done < $1

echo
echo
echo -e "$licenses"
