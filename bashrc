#!/bin/bash

### default flags
CHOST="x86_64-pc-linux-gnu"
## TODO support cross compile i686_pc_linux_gnu_CFLAGS
CFLAGS="-pipe -O3 `${CHOST}-gcc -march=native -E -v - </dev/null 2>&1 | sed -n -e 's/^.*- -/-/p'`"
EXJOBS=$((`cat /proc/cpuinfo | grep processor | wc -l`+2))

### default custom flags: applied by setting ECONF_WRAPPER and EXTRA_ECONF
EXTRA_ECONF="--disable-static"

## import per-package bashrc configuration
source <(${PALUDIS_CONFIG_DIR}/myconfig/scripts/wrapper bashrc)

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
