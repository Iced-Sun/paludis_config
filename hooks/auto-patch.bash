#!/usr/bin/env bash

PATCH_DIR="/etc/paludis/myconfig/patches"

case "${HOOK}" in
    ebuild_prepare_post )
	for PATCH in `find ${PATCH_DIR}/${CATEGORY}/${PN} -type f -iname '*.patch'`; do
	    einfo_unhooked "Applying patch ${PATCH}..."
	    expatch "${PATCH}"
	done
	;;
    *)
	;;
esac   

