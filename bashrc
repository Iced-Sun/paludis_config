#!/bin/bash
source /etc/paludis/myconfig/scripts/utils

### default flags
CHOST="x86_64-pc-linux-gnu"
CFLAGS=( -O3 -pipe )
LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags
EXTRA_ECONF=( --disable-static )

### special care
case "${PN}" in
    wine)
	CFLAGS=( -O2 -pipe )
	;;&
    w3m|paludis)
	LDFLAGS=( -Wl,-O1 )
	;;&
    autoconf|libseccomp|firefox|xulrunner|nspr|talloc|notmuch)
	AUTOTOOL=false
	;;&
    nettle|db)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]/--disable-static/} )
	;;&
    *)
	;;
esac    

### host specific flags
HOST=`hostname|cut -d. -f1`
case "${HOST}" in
    dc-2|fs-3|gs-5)
	CFLAGS+=( -march=core2 -msse4.1 )
	EXJOBS=10
	case "${PN}" in
	    bind-tools)
		EXTRA_ECONF+=( --with-gssapi )
		;;&
	    *)
		;;
	esac
	;;&
    laptop-x61)
	CFLAGS+=( -march=core2 -msse4.1 )
	### distcc
	if is_in_2112; then
	    PATH="/usr/libexec/distcc:${PATH}"
	    DISTCC_DIR="/var/tmp/paludis/distcc"
	    EXJOBS=10
	    DISTCC_HOSTS='--randomize 10.2.112.2,lzo'
	fi
	#EMAKE_WRAPPER="pump"
	#192.168.1.50,lzo,cpp
esac

### finalize
CFLAGS="${CFLAGS[@]}"
CXXFLAGS="${CFLAGS}"
LDFLAGS="${LDFLAGS[@]}"

# extra econf
if [[ ${AUTOTOOL}x != falsex ]]; then
    ECONF_WRAPPER="append_configure_option ${#EXTRA_ECONF[@]} ${EXTRA_ECONF[@]}"
fi
