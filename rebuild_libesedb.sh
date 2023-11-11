#!/bin/bash

SEQUENCE1="
libcstring
libcerror
libcthreads
libcdata
libcdatetime
libclocale
libcnotify
libcsplit
"

SEQUENCE2="
libuna
libcfile
libcpath
libbfio
libfcache
libfdata
libfvalue
libfguid
libfdatetime
libfwnt
libhmac
libcaes
libodraw
libsmdev
libsmraw
libcsystem
libfmapi
libmapidb
"

for I in $SEQUENCE ; do
    copr build-package rebus/infosec --name "$I"
    RESULT=$!
    if [ "$RESULT" -ne 0 ] ; then
        echo "==== ERROR: failed package $I "
        exit
    fi
done

# libcstring	DONE
# libcerror	DONE

# libcthreads
#	libcerror

# libcdata	DONE
#        libcerror \
#        libcthreads \

# libcdatetime	DONE
#        libcerror \


# libclocale	DONE
#        libcerror \

# libcnotify	DONE
#        libcerror \


# libcsplit	DONE
#        libcerror \

# libuna		PARTIAL !!!!!!!!
#        libcstring \
#        libcerror \
#        libcdatetime \
#        libclocale \
#        libcnotify \
#        libcfile \
#        libcsystem \


# libcfile	DONE
#	libclocale \
#        libcnotify \
#        libuna \

# libcpath	DONE
#        libcstring \
#        libcerror \
#        libclocale \
#        libcsplit \
#        libuna \


# libbfio		DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libclocale \
#        libcnotify \
#        libcsplit \
#        libuna \
#        libcfile \
#        libcpath \


# libfcache	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \


# libfdata	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libcnotify \
#        libfcache \


# libfvalue	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libcnotify \
#        libuna \
#        libfdatetime \
#        libfguid \
#        libfwnt \


# libfguid	DONE
#        libcstring \
#        libcerror \

# libfdatetime	DONE
#        libcstring \
#        libcerror \


# libfwnt		DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libcnotify \


# libhmac		DONE
#        libcstring \
#        libcerror \
#        libclocale \
#        libcnotify \
#        libcsplit \
#        libuna \
#        libcfile \
#        libcpath \
#        libcsystem \


# libcaes		DONE
#        libcstring \
#        libcerror \


# libodraw	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libclocale \
#        libcnotify \
#        libcsplit \
#        libuna \
#        libcfile \
#        libcpath \
#        libbfio \
#        libcsystem \
#        libhmac \


# libsmdev	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libclocale \
#        libcnotify \
#        libuna \
#        libcfile \
#        libcsystem \


# libsmraw	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libclocale \
#        libcnotify \
#        libcsplit \
#        libuna \
#        libcfile \
#        libcpath \
#        libbfio \
#        libfcache \
#        libfdata \
#        libfvalue \
#        libcsystem \
#        libhmac \


# libcsystem	DONE
#        libcstring \
#        libcerror \
#        libclocale \
#        libcnotify \
#        libuna \


# libfmapi	DONE

# libmapidb	DONE
