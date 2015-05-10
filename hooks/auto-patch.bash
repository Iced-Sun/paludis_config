#!/usr/bin/env bash

PATCH_DIR="/etc/paludis/myconfig/patches"

case "${HOOK}" in
    ebuild_prepare_post )
	pushd ${PATCH_DIR} >/dev/null
	PATCHES=( `find . -type f -iname '*.patch'` )
	INSTALL_PATCHES=()
	for PATCH in "${PATCHES[@]}"; do
	    SPLITS=( ${PATCH//\// } )
	    if [[ "${SPLITS[1]}/${SPLITS[2]}" = "${CATEGORY}/${PN}" ]]; then
		INSTALL_PATCHES+=( "${SPLITS[3]}" )
	    fi
	done
	popd >/dev/null

	for patch in ${INSTALL_PATCHES[@]}; do
	    einfo_unhooked "Patching ${patch}..."
	    expatch "${PATCH_DIR}/${CATEGORY}/${PN}/${patch}"
	done
	;;
    *)
	;;
esac   

