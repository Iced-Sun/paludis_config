#!/bin/bash
source /etc/paludis/myconfig/scripts/utils

### default flags
CHOST="x86_64-pc-linux-gnu"
CFLAGS=( -O3 -pipe )
LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags
EXTRA_ECONF=( --disable-static )

### default host specific flags
[[ -f /etc/paludis/myconfig/host/`hostname`/bashrc ]] && source /etc/paludis/myconfig/host/`hostname`/bashrc

### special care
case "${PN}" in
    w3m|paludis)
	LDFLAGS=( -Wl,-O1 )
	;;&
    libseccomp|firefox|xulrunner|nspr|talloc|notmuch)
	AUTOTOOL=false
	;;&
    nettle|db)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]/--disable-static/} )
	;;&
    *)
	;;
esac    

### finalize
CFLAGS="${CFLAGS[@]}"
CXXFLAGS="${CFLAGS}"
LDFLAGS="${LDFLAGS[@]}"

# extra econf
if [[ ${AUTOTOOL}x != falsex ]]; then
    ECONF_WRAPPER="append_configure_option ${#EXTRA_ECONF[@]} ${EXTRA_ECONF[@]}"
fi
