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
## NOTE this is best done in hooks, but ebuild_configure_pre and src_configure
## are executed in different context; we need to inject enable_distcc into
## src_configure directly
wrap_ebuild_phase() {
	einfo_unhooked "Wrapping the ${EXHERES_PHASE} phase..."

	local group=()
	while [[ "$#" -gt 0 ]]; do
		if [[ "$1" == *';' ]]; then
			## pre hook
			group+=( "${1%;}" )
			einfo_unhooked "  Running the pre-${EXHERES_PHASE} hook ${group[@]}..."
			"${group[@]}"
			group=()
		elif [[ "$#" -eq 1 ]]; then
			group+=( "$1" )

			einfo_unhooked "  Entering the ${EXHERES_PHASE} phase..."

			if [[ ${EXHERES_PHASE} == "configure" ]]; then
				einfo_unhooked "  Applying EXTRA_ECONF..."
				edo "${group[@]}" ${MY__EXTRA_ECONF}
			else
				edo "${group[@]}"
			fi
		else
			group+=( "$1" )
		fi

		shift
	done
}

## to apply EXTRA_ECONF
ECONF_WRAPPER="wrap_ebuild_phase"
