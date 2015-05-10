#!/usr/bin/env bash

[[ "${CATEGORY}/${PN}" != "sys-libs/glibc" ]] && return 0

case "${HOOK}" in
    ebuild_install_post )
	local LOCALE_GEN=( "zh_CN.UTF-8 UTF-8" )

	local localedef=${IMAGE}/usr/$(exhost --target)/bin/localedef

	local locale
	for locale in "${LOCALE_GEN[@]}"; do
            local name="${locale% *}"
            local input="${name%.*}"
            local charmap="${locale#* }"
 
            if [[ -z "${name}" ]]; then
		ewarn "failed to grab locale name from \"${locale}\" in LOCALE_GEN"
		continue
            elif [[ -z "${input}" ]]; then
		ewarn "failed to grab input name from \"${locale}\" in LOCALE_GEN"
		continue
            elif [[ -z "${charmap}" ]]; then
		ewarn "failed to grab charmap name from \"${locale}\" in LOCALE_GEN"
		continue
            fi
 
            einfo "Generating locale ${name}"
	    mkdir -p ${IMAGE}/usr/$(exhost --target)/lib/locale
            ${localedef} --prefix=${IMAGE} -i "${input}" -f "${charmap}" "${name}"
	done
	;;
    *)
        ;;
esac   

