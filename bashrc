#!/bin/bash

### default flags
CHOST="x86_64-pc-linux-gnu"
## TODO support cross compile i686_pc_linux_gnu_CFLAGS
CFLAGS="-pipe -O3 `${CHOST}-gcc -march=native -E -v - </dev/null 2>&1 | sed -n -e 's/^.*- -/-/p'`"
LDFLAGS="-Wl,-O1 -Wl,--as-needed -Wl,--sort-common"
EXJOBS=$((`cat /proc/cpuinfo | grep processor | wc -l`+2))

### default custom flags: applied by setting ECONF_WRAPPER and EXTRA_ECONF
## TODO EXTRA_ECONF is not an array anymore, check if wrap_ebuild_phase is still valid
EXTRA_ECONF="--disable-static"

### special care
## TODO can we put these options to package configs?
case "${PN}" in
    glibc|mupdf)
	## just don't bother
	CFLAGS="-march=native -pipe -O3"
	USE_DISTCC=no
	;;&
    paludis)
	## 'as-needed' corrupts 'print_exports' and 'strip_tar_corruption'
	LDFLAGS=${LDFLAGS#-Wl,--as-needed}
	;;&
    openjdk8|notmuch|db|pinktrace|git|busybox|ocaml)
	EXTRA_ECONF=${EXTRA_ECONF/--disable-static/}
	;;&
    sway)
        EXJOBS=1
        ;;&
    efibootmgr)
	CFLAGS+=" -D_GNU_SOURCE"
	LDFLAGS+=" -Wl,-z,muldefs"
	;;&
    *)
	;;
esac    

### host specific flags
## TODO use HOST from myconfig
HOST=`hostname | cut -d. -f1`
case "${HOST}" in
    dc-2|fs-3|gs-5)
	case "${PN}" in
	    bind-tools)
		EXTRA_ECONF+=" --with-gssapi"
		;;&
	    *)
		;;
	esac
	;;&
esac

### finalize

## TODO the expansion should be in wrapper

## note: under the hood of multiarch, the final CFLAGS/CPPFLAGS is computed as
##   computed_CFLAGS=${x86_64_pc_linux_gnu_CFLAGS:=-march=native -O2 -pipe}
##   computed_CPPFLAGS=${x86_64_pc_linux_gnu_CFLAGS} ${x86_64_pc_linux_gnu_CPPFLAGS:-CPPFLAGS}
eval "${CHOST//-/_}_CFLAGS=\${CFLAGS}"
eval "${CHOST//-/_}_CXXFLAGS=\${CFLAGS}"
eval "${CHOST//-/_}_CPPLAGS="
eval "${CHOST//-/_}_LDFLAGS=\${LDFLAGS}"

### Advanced customization
## NOTE: bashrc is sourced once in builtin_init phase only when
## cave-perform
[[ ${PALUDIS_ACTION} == "sync" ]] && return
source ${PALUDIS_CONFIG_DIR}/myconfig/scripts/utils

## to apply EXTRA_ECONF
ECONF_WRAPPER="wrap_ebuild_phase"

## FIXME we just need another round to make distcc work again.
USE_DISTCC=no
if [[ x${USE_DISTCC} != "xno" ]]; then
    source ${PALUDIS_CONFIG_DIR}/myconfig/scripts/distcc
    
    EMAKE_WRAPPER="wrap_ebuild_phase distcc_setup_hosts; distcc_allow_net;"

    ## in the case of cmake.exlib, src_configure will invoke ecmake()
    ## which doesn't provide a customization point, hence it is not
    ## possible to allow net_access in sandboxing. But this is ok, since the only thing
    ##
    ## A side effect of the hack is that distcc will be alway failed in src_configure phase
    distcc_setup_environ
fi

## FIXME valgrind/lftp/mesa/xorg-server/mpv/boost don't distribute all compiling, need digging
