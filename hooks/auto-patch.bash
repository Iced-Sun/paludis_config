#!/usr/bin/env bash

PATCH_DIR="/etc/paludis/myconfig/patches"

case "${HOOK}" in
    ebuild_prepare_post )
	if [[ -d ${PATCH_DIR}/${CATEGORY}/${PN} ]]; then
	    for PATCH in `find ${PATCH_DIR}/${CATEGORY}/${PN} -type f -iname '*.patch'`; do
		einfo "Applying patch ${PATCH}..."
		expatch "${PATCH}"
	    done
	fi
	;;
    *)
	;;
esac   

