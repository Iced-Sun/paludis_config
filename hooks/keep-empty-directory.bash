#!/usr/bin/env bash

case "${HOOK}" in
    ebuild_install_post )
	pushd ${IMAGE} >/dev/null
	for DIR in $(find . -type d -empty); do
	    einfo_unhooked "Keep empty directory of ${DIR} to avoid merger failure..."

            edo keepdir "${DIR#.}"
	done
	popd >/dev/null
	;;
    *)
        ;;
esac   
