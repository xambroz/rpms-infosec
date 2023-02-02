#!/bin/bash

# libcstring	DONE
copr build-package rebus/infosec --name libcstring

# libcerror	DONE
#	libcstring
copr build-package rebus/infosec --name libcerror


# libcthreads
#	libcstring
#	libcerror
copr build-package rebus/infosec --name libcthreads


# libcdata	DONE
#         libcstring \
#        libcerror \
#        libcthreads \
copr build-package rebus/infosec --name libcdata	

# libcdatetime	DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libcdatetime	


# libclocale	DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libclocale	

# libcnotify	DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libcnotify	


# libcsplit	DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libcsplit	


# libuna		PARTIAL !!!!!!!!
#        libcstring \
#        libcerror \
#        libcdatetime \
#        libclocale \
#        libcnotify \
#        libcfile \
#        libcsystem \
copr build-package rebus/infosec --name libuna		


# libcfile	DONE
#	libclocale \
#        libcnotify \
#        libuna \
copr build-package rebus/infosec --name libcfile	

# libcpath	DONE
#        libcstring \
#        libcerror \
#        libclocale \
#        libcsplit \
#        libuna \
copr build-package rebus/infosec --name libcpath	


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
copr build-package rebus/infosec --name libbfio		


# libfcache	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
copr build-package rebus/infosec --name libfcache	


# libfdata	DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libcnotify \
#        libfcache \
copr build-package rebus/infosec --name libfdata	


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
copr build-package rebus/infosec --name libfvalue	


# libfguid	DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libfguid	


# libfdatetime	DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libfdatetime	


# libfwnt		DONE
#        libcstring \
#        libcerror \
#        libcthreads \
#        libcdata \
#        libcnotify \
copr build-package rebus/infosec --name libfwnt		


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
copr build-package rebus/infosec --name libhmac		


# libcaes		DONE
#        libcstring \
#        libcerror \
copr build-package rebus/infosec --name libcaes		


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
copr build-package rebus/infosec --name libodraw	


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
copr build-package rebus/infosec --name libsmdev	


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
copr build-package rebus/infosec --name libsmraw	


# libcsystem	DONE
#        libcstring \
#        libcerror \
#        libclocale \
#        libcnotify \
#        libuna \
copr build-package rebus/infosec --name libcsystem	


# libfmapi	DONE
copr build-package rebus/infosec --name libfmapi	


# libmapidb	DONE
copr build-package rebus/infosec --name libmapidb	

