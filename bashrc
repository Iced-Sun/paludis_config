#!/bin/bash

### default flags
CHOST="x86_64-pc-linux-gnu"
MY_CFLAGS=( `${CHOST}-gcc -march=native -E -v - </dev/null 2>&1 | sed -n -e 's/^.*- -/-/p'` -pipe -O3 )
MY_LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags
EXTRA_ECONF=( --disable-static )

### special care
case "${PN}" in
    glibc|paludis)
	MY_CFLAGS=( -march=native -pipe -O2 )
	USE_DISTCC=no
	;;&
    openjdk8|notmuch|db|pinktrace|git|busybox|ocaml)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]/--disable-static/} )
	;;&
    *)
	;;
esac    

### host specific flags
## TODO use HOST from myconfig
HOST=`hostname|cut -d. -f1`
case "${HOST}" in
    dc-2|fs-3|gs-5)
	EXJOBS=10
	case "${PN}" in
	    bind-tools)
		EXTRA_ECONF+=( --with-gssapi )
		;;&
	    *)
		;;
	esac
	;;&
esac

### finalize
## note: under the hood of multiarch, the final CFLAGS/CPPFLAGS is computed as
##   computed_CFLAGS=${x86_64_pc_linux_gnu_CFLAGS:-CFLAGS}
##   computed_CPPFLAGS=${x86_64_pc_linux_gnu_CFLAGS} ${x86_64_pc_linux_gnu_CPPFLAGS:-CPPFLAGS}
#eval "${CHOST//-/_}_CFLAGS=\${MY_CFLAGS[@]}"
#eval "${CHOST//-/_}_CXXFLAGS=\${MY_CFLAGS[@]}"
#eval "${CHOST//-/_}_LDFLAGS=\${MY_LDFLAGS[@]}"
CFLAGS=${MY_CFLAGS[@]}
CXXFLAGS=${MY_CFLAGS[@]}
LDFLAGS=${MY_LDFLAGS[@]}

### Advanced customization
## NOTE: bashrc is sourced only once in builtin_init phase when cave-perform

if [[ x${USE_DISTCC} != "xno" ]]; then
    source /etc/paludis/myconfig/scripts/utils

    ECONF_WRAPPER="wrap_ebuild_phase try_enable_distcc :WRAP_END:"
    EMAKE_WRAPPER="wrap_ebuild_phase try_enable_distcc :WRAP_END:"
    EINSTALL_WRAPPER="wrap_ebuild_phase try_enable_distcc :WRAP_END:"
fi

## cmake.exlib uses emake, but not econf; need export the distcc environment
##
## the problem is that ecmake doesn't provide a customization point, and hence
## it is not possible to allow net_access in sandboxing
### FIXME think it through
#[[ -n $EXHERES_PHASE ]] && try_enable_distcc
