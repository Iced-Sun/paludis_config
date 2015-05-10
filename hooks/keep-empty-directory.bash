#!/usr/bin/env bash

case "${HOOK}" in
    ebuild_install_post )
	einfo "Searching for empty directory to avoid merger failure..."

	pushd ${IMAGE} >/dev/null
	for dir in $(find . -type d -empty); do
            edo keepdir "${dir#.}"
	done
	popd >/dev/null
	;;
    *)
        ;;
esac   
