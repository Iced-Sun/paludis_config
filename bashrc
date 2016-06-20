#!/bin/bash

### default flags
CHOST="x86_64-pc-linux-gnu"
MY_CFLAGS=( -pipe -O3 `${CHOST}-gcc -march=native -E -v - </dev/null 2>&1 | sed -n -e 's/^.*- -/-/p'` )
MY_LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags: applied by setting ECONF_WRAPPER and EXTRA_ECONF
EXTRA_ECONF=( --disable-static )

### special care
## TODO can we put these options to package configs?
case "${PN}" in
    glibc)
	## just don't bother
	MY_CFLAGS=( -march=native -pipe -O3 )
	USE_DISTCC=no
	;;&
    paludis)
	## 'as-needed' corrupts 'print_exports' and 'strip_tar_corruption'
	MY_LDFLAGS=( ${MY_LDFLAGS[@]#-Wl,--as-needed} )
	;;&
    openjdk8|notmuch|db|pinktrace|git|busybox|ocaml)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]#--disable-static} )
	;;&
    *)
	;;
esac    

### host specific flags
## TODO use HOST from myconfig
HOST=`hostname|cut -d. -f1`
case "${HOST}" in
    dc-2|fs-3|gs-5)
	EXJOBS=10
	case "${PN}" in
	    bind-tools)
		EXTRA_ECONF+=(--with-gssapi)
		;;&
	    *)
		;;
	esac
	;;&
esac

### finalize

## note: under the hood of multiarch, the final CFLAGS/CPPFLAGS is computed as
##   computed_CFLAGS=${x86_64_pc_linux_gnu_CFLAGS:=-march=native -O2 -pipe}
##   computed_CPPFLAGS=${x86_64_pc_linux_gnu_CFLAGS} ${x86_64_pc_linux_gnu_CPPFLAGS:-CPPFLAGS}
eval "${CHOST//-/_}_CFLAGS=\${MY_CFLAGS[@]}"
eval "${CHOST//-/_}_CXXFLAGS=\${MY_CFLAGS[@]}"
eval "${CHOST//-/_}_CPPLAGS="
eval "${CHOST//-/_}_LDFLAGS=\${MY_LDFLAGS[@]}"

### Advanced customization
## NOTE: bashrc is sourced once in builtin_init phase only when cave-perform
ECONF_WRAPPER="wrap_ebuild_phase" ## for EXTRA_ECONF

if [[ x${USE_DISTCC} != "xno" ]]; then
    EMAKE_WRAPPER="wrap_ebuild_phase distcc_setup_hosts; distcc_allow_net;"

    ## in the case of cmake.exlib, src_configure will invoke ecmake()
    ## which doesn't provide a customization point, hence it is not
    ## possible to allow net_access in sandboxing. But this is ok, since the only thing
    ##
    ## A side effect of the hack is that distcc will be alway failed in src_configure phase
    source /etc/paludis/myconfig/scripts/utils
    distcc_setup_environ
fi

## FIXME mesa/xorg-server/mpv don't distribute all compiling, need digging
