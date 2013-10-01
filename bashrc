#!/bin/bash

## functions
has_ipv6()
{
    {
	which ifconfig && ifconfig | grep '2001:da8' && return 0 || return 1
    } >/dev/null 2>&1
}

is_in_2112()
{
    {
	which ifconfig && ifconfig | grep '10.2.112' && return 0 || return 1
    } >/dev/null 2>&1
}

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

### Build extra
EXJOBS=3

### distcc
if [[ $(hostname) == "laptop-x61" ]]; then
    if is_in_2112; then
	PATH="/usr/libexec/distcc:${PATH}"
	DISTCC_DIR="/var/tmp/paludis/distcc"
	EXJOBS=20
	DISTCC_HOSTS='--randomize 10.2.112.51,lzo'
    fi
    #EMAKE_WRAPPER="pump"
    #192.168.1.50,lzo,cpp
fi

### special care
case "${PN}" in
    xulrunner)
	custom_EXTRA_ECONF+=( --disable-elf-hack )
	EXJOBS=5
	;;&
    ocaml|notmuch)
	LDFLAGS=""
	;;&
    mc)
	EXJOBS=5
	DISTCC_HOSTS=
	;;&
    notmuch|db|nettle)
	;; # don't disable static
    glib|schroot|xulrunner|firefox)
	;; # no clang
    *)
	CC="clang"
	CXX="clang++"
	custom_EXTRA_ECONF=( --disable-static )
	;;
esac    

### finalize
CXXFLAGS="${CFLAGS}"
ECONF_WRAPPER="append_configure_option ${#custom_EXTRA_ECONF[@]} ${custom_EXTRA_ECONF[@]}"
