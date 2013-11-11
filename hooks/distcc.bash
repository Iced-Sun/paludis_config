#!/usr/bin/env bash
shopt -s extglob
export PATH="$(${PALUDIS_EBUILD_DIR}/utils/canonicalise ${PALUDIS_EBUILD_DIR}/utils/ ):${PATH}"
source ${PALUDIS_ECHO_FUNCTIONS_DIR:-${PALUDIS_EBUILD_DIR}}/echo_functions.bash

if [[ -n ${DISTCC_DIR} ]]; then
    case "${HOOK}" in
	ebuild_configure_pre | ebuild_compile_pre | ebuild_install_pre )
	    einfo_unhooked "Allowing net connection for distcc..."
	    edo esandbox allow_net --connect "inet:0.0.0.0/0@3632"
#	    edo esandbox allow_net "unix:/tmp/distcc-pump.*/socket"
	    einfo_unhooked "Allowing net connection for distcc...Done"
	    ;;
	*)
	    ;;
    esac   
fi

true
