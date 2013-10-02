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
CFLAGS="-O3 -pipe"
LDFLAGS="-Wl,-O1 -Wl,--as-needed -Wl,--sort-common"
EXJOBS=3

[[ -f /etc/paludis/myconfig/bashrc.`hostname` ]] && source /etc/paludis/myconfig/bashrc.`hostname`

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
	source /etc/paludis/myconfig/clang-lto/bashrc
	custom_EXTRA_ECONF=( --disable-static )
	;;
esac    

### finalize
CXXFLAGS="${CFLAGS}"
ECONF_WRAPPER="append_configure_option ${#custom_EXTRA_ECONF[@]} ${custom_EXTRA_ECONF[@]}"
