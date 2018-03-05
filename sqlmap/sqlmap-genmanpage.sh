#!/bin/bash

help2man --no-info \
    --source="FEDORA" \
    --name="penetration testing tool for sql injection in web applications" \
    --output=sqlmap.1 \
    --include=sqlmap.1.template \
    --help-option=-hh \
    sqlmap

sed -i -e '
s|^__H__$||;
s|^___ ___..._____ ___ ___$||;
s/^|_ \\-| . ...     | ..| . |$//;
s/^|_ .-| \. ...     | \..| \. |$//;
s/^|___|_  ..._|_|_|__,|  _|$//;
s|^{1.2.*}$||;
s/^|_|V$//;
s/^|_|   //;
s/___//;
s|^Target:|.SH TARGET|;
s|^Request:|.SH REQUEST|;
s|^Optimization:|.SH OPTIMIZATION|;
s|^Injection:|.SH INJECTION|;
s|^\([A-Z][a-z ]*\):$|.SH \U\1|;
s|^.IP$||;
s|.B python|.B |;
' sqlmap.1

