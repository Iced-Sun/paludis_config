#!/bin/bash

## TODOs
# 1. support alternatives per-package
# 2. redo distcc
# 3. for raspipy/ga

### forget about sync
## cave-perform
## NOTE: bashrc is sourced once in builtin_init phase only when
[[ ${PALUDIS_ACTION} == "sync" ]] && return

### default flags
CHOST="x86_64-pc-linux-gnu"
CROSS_COMPILE_TOOLS+=" AR:gcc-ar RANLIB:gcc-ranlib" # for LTO

### import global&per-package bashrc configuration
source <(${PALUDIS_CONFIG_DIR}/myconfig/scripts/wrapper bashrc)

### Advanced customization
## import helper functions
source ${PALUDIS_CONFIG_DIR}/myconfig/scripts/utils

## to apply EXTRA_ECONF
ECONF_WRAPPER="wrap_ebuild_phase"

## FIXME we just need another round to make distcc work again.
if [[ x${MY__USE_DISTCC} != "xno" ]]; then
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
