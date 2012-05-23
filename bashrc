#!/bin/bash
CHOST="x86_64-pc-linux-gnu"
CFLAGS="-march=core2 -O2 -pipe"
[[ $(hostname) == "laptop-x61" ]] && CFLAGS+=" -msse4.1"
LDFLAGS="-Wl,-O1 -Wl,--as-needed -Wl,--sort-common"

case "${PN}" in
    ocaml|notmuch)
	LDFLAGS=""
	;;&
    *)
	;;
esac    
CXXFLAGS="${CFLAGS}"

EXJOBS=4
if [[ $(hostname) == "laptop-x61" ]]; then
    PATH="/usr/libexec/distcc:${PATH}"
    DISTCC_DIR="/var/tmp/paludis/distcc"
    EMAKE_WRAPPER="pump"
    DISTCC_HOSTS="--randomize 192.168.6.50,lzo,cpp"
fi
