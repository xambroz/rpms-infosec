#!/bin/bash
REMNUX_URL=https://remnux.org/get-remnux.sh
REMNUX=get-remnux.sh
PKGFILE=remnux_packages.txt


function translate_to_fedora {
    sed -e '
        s/default-jre/jre/;
	s/bundler/rubygem-bundler/;
	s/clamav-daemon/clamav-server/;
	s/epic5/epic/;
	s/gdb-minimal/gdb/;
        s/imagemagick/ImageMagick/;
	s/stunnel4/stunnel/;
	s/ruby-dev/ruby-devel/;
	s/upx-ucl/upx/;
	s/upenssh-client/openssh/;
	s/pdftk//;
        s/p7zip-full/p7zip-plugins/;
        s/python-capstone/capstone-python\ncapstone-python3/;
	s/lib32stdc++6/libstdc++/;
	s/libboost1.54-all-dev//;
	s/libc6-dev-i386//;
	s/libcanberra-gtk-module:i386//;
	s/libemail-outlook-message-perl//;
	s/libemu2//;
	s/python-dev/python-devel/;
	s/python-dnspython//;
	s/sysdig//;
	s/bundler/rubygem-bundler/;

    '
}


if [ ! -f "$REMNUX" ] ; then
	wget $REMNUX_URL
fi


if [ ! -f "$PKGFILE" ] ; then
    sed -n '
	{
		/install_ubuntu_14.04_packages/,/}/ {
			/packages="/,/"[ ]*$/ {
				s/packages="//;
				s/^[ ]*//g;
                                /"[ ]*$/ {
	    				s/\"[ ]*//g;
					q

				}
				p
			}
		}
	}
    ' "$REMNUX" | sort -u > $PKGFILE
fi

cat "$PKGFILE" | translate_to_fedora |\
while read PKG ; do
	dnf -y install "$PKG"
	if [ $? -ne 0 ] ; then 
		echo "$PKG" > missing.txt
        fi
done



