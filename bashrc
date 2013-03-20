#!/bin/bash

### base
CHOST="x86_64-pc-linux-gnu"
CFLAGS="-march=core2 -O3 -pipe"
LDFLAGS="-Wl,-O1 -Wl,--as-needed -Wl,--sort-common"

disable_static_lib()
{
    "$@" --disable-static
}
ECONF_WRAPPER="disable_static_lib"



### special care
[[ $(hostname) == "laptop-x61" ]] && USE_DISTCC=true
case "${PN}" in
    ocaml|notmuch)
	LDFLAGS=""
	;;&
    *)
	;;
esac    

### finalize
CXXFLAGS="${CFLAGS}"
EXJOBS=3

### distcc
if [[ ${USE_DISTCC} == "true" ]]; then
    EXJOBS=4
    PATH="/usr/libexec/distcc:${PATH}"
    DISTCC_DIR="/var/tmp/paludis/distcc"
    EMAKE_WRAPPER="pump"
    DISTCC_HOSTS="--randomize 192.168.6.50,lzo,cpp"
fi
