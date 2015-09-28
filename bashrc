#!/bin/bash

### default flags
CHOST="x86_64-pc-linux-gnu"
MY_CFLAGS=( -O3 -pipe )
MY_LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags
EXTRA_ECONF=( --disable-static )

### special care
case "${PN}" in
    NetworkManager)
	EXJOBS=1
	;;&
    gtk+)
	[[ $SLOT == 2 ]] && MY_LDFLAGS=( -Wl,-O1 )
	;;&
    gettext)
	MY_LDFLAGS=( -Wl,-O1 )
	;;&
    zip|busybox|jpeg|git|notmuch|talloc|db|ocaml|gtk+|pinktrace)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]/--disable-static/} )
	;;&
    *)
	;;
esac    

### host specific flags
## TODO how do we add  "-march=native" ?
## TODO use HOST from myconfig
HOST=`hostname|cut -d. -f1`
case "${HOST}" in
    dc-2|fs-3|gs-5)
	### target march and host march
	MY_CFLAGS+=( -march=core2 -msse4.1 )
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
	MY_CFLAGS+=( -march=core2 -msse4.1 )
esac

### finalize
x86_64_pc_linux_gnu_CFLAGS="${MY_CFLAGS[@]}"
i686_pc_linux_gnu_CFLAGS="${MY_CFLAGS[@]}"
x86_64_pc_linux_gnu_CXXFLAGS="${MY_CFLAGS[@]}"
i686_pc_linux_gnu_CXXFLAGS="${MY_CFLAGS[@]}"
LDFLAGS="${MY_LDFLAGS[@]}"

### Advanced customization
## NOTE: bashrc is sourced only once in builtin_init phase when cave-perform

source /etc/paludis/myconfig/scripts/utils

ECONF_WRAPPER="wrap_ebuild_phase try_enable_distcc :WRAP_END:"
EMAKE_WRAPPER="wrap_ebuild_phase try_enable_distcc :WRAP_END:"
EINSTALL_WRAPPER="wrap_ebuild_phase try_enable_distcc :WRAP_END:"

## cmake.exlib uses emake, but not econf; need export the distcc environment
##
## the problem is that ecmake doesn't provide a customization point, and hence
## it is not possible to allow net_access in sandboxing
### FIXME think it through
#[[ -n $EXHERES_PHASE ]] && try_enable_distcc
