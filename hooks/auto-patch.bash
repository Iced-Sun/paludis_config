#!/usr/bin/env bash
shopt -s extglob
export PATH="$(${PALUDIS_EBUILD_DIR}/utils/canonicalise ${PALUDIS_EBUILD_DIR}/utils/ ):${PATH}"
source ${PALUDIS_ECHO_FUNCTIONS_DIR:-${PALUDIS_EBUILD_DIR}}/echo_functions.bash

PATCH_DIR="/etc/paludis/myconfig/patches"

case "${HOOK}" in
    ebuild_prepare_post )
	if [[ "${CATEGORY}/${PN}" == "app-editors/emacs" ]]; then
	    einfo_unhooked "Auto-patching emacs..."
	    expatch "${PATCH_DIR}/emacs-cjk-monospace-v24.patch"
	fi
	;;
    *)
	;;
esac   

