#!/bin/bash

append_configure_option()
{
    n="$1"
    shift

    opts=()
    for ((i=0; i<n; ++i)); do
	opts+=( "$1" )
	shift
    done
    
    edo "$@" "${opts[@]}"
}

### basic flags
CHOST="x86_64-pc-linux-gnu"
CFLAGS="-march=core2 -O3 -pipe"
LDFLAGS="-Wl,-O1 -Wl,--as-needed -Wl,--sort-common"

### ECONF HACK
EXTRA_ECONF=( --disable-static )

### special care
[[ $(hostname) == "laptop-x61" ]] && USE_DISTCC=true
case "${PN}" in
    db)
	EXTRA_ECONF=()
	;;&
    xulrunner)
	EXTRA_ECONF+=( --disable-elf-hack )
	;;&
    ocaml|notmuch)
	LDFLAGS=""
	;;&
    *)
	;;
esac    

### finalize
CXXFLAGS="${CFLAGS}"
ECONF_WRAPPER="append_configure_option ${#EXTRA_ECONF[@]} ${EXTRA_ECONF[@]}"
EXJOBS=3

### distcc
if [[ ${USE_DISTCC} == "true" ]]; then
    EXJOBS=4
    PATH="/usr/libexec/distcc:${PATH}"
    DISTCC_DIR="/var/tmp/paludis/distcc"
    EMAKE_WRAPPER="pump"
    DISTCC_HOSTS="--randomize 192.168.6.50,lzo,cpp"
fi
