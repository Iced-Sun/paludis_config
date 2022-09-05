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

### import global&per-package bashrc configuration
source <(${PALUDIS_CONFIG_DIR}/myconfig/scripts/wrapper bashrc)

### Advanced customization
## import helper functions
source ${PALUDIS_CONFIG_DIR}/myconfig/scripts/utils.sh

## to apply EXTRA_ECONF
ECONF_WRAPPER="wrap_ebuild_phase"

