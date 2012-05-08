#!/usr/bin/env bash
if [[ -n ${DISTCC_DIR} ]]; then
    mkdir -p ${DISTCC_DIR}
    case "${HOOK}" in
	ebuild_compile_pre|ebuild_install_pre)
	    edo esandbox allow_net --connect "inet:0.0.0.0/0@3632"
	    edo esandbox allow_net "unix:/tmp/distcc-pump.*/socket"
	    ;;
	*)
	    ;;
    esac   
fi
