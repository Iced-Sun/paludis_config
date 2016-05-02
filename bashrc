#!/bin/bash

### default flags
CHOST="x86_64-pc-linux-gnu"
MY_CFLAGS=(-pipe -O3 `${CHOST}-gcc -march=native -E -v - </dev/null 2>&1 | sed -n -e 's/^.*- -/-/p'`)
MY_LDFLAGS=(-Wl,-O1 -Wl,--as-needed -Wl,--sort-common)
EXJOBS=3

### default custom flags
EXTRA_ECONF=(--disable-static)

### special care
case "${PN}" in
    glibc)
	## 1. it seems that glibc will sort CFLAGS, which just breaks
	## the flags of '--param * --param *' generated by 'gcc
	## -march=native -v'
	##
	## throw '--param *'
	MY_CFLAGS=(`${CHOST}-gcc -march=native -E -v - </dev/null 2>&1 | sed -n -e 's/^.*- -/-/p' | sed -e 's/--param.* //'` -pipe -O3)

	## 2. sysdeps/x86_64/multiarch/str*.c need sse4.2 to compile,
	## and the compiling flags are "${CFLAGS} -msse4
	## ${CPPFLAGS}". If CPPFLAGS contains any of "-mno-sse4
	## -mno-sse4.1 -mno-sse4.2", it won't compile. This happens
	## when ${CHOST//-/_}_CFLAGS is set due to the assembling rule
	## of CPPFLAGS of multiarch (see the notes in section
	## "finalize").
	##
	## for now, we use CFLAGS instead of ${CHOST//-/_}_CFLAGS,
	## which is wrong because CFLAGS is not in the final CPPFLAGS;
	## we'll see if this breaks anything
	;;&
    paludis)
	## 'as-needed' corrupts 'print_exports' and 'strip_tar_corruption'
	MY_LDFLAGS=(${MY_LDFLAGS[@]#-Wl,--as-needed})
	;;&
    openjdk8|notmuch|db|pinktrace|git|busybox|ocaml)
	EXTRA_ECONF=(${EXTRA_ECONF[@]#--disable-static})
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
##   computed_CFLAGS=${x86_64_pc_linux_gnu_CFLAGS:-CFLAGS}
##   computed_CPPFLAGS=${x86_64_pc_linux_gnu_CFLAGS} ${x86_64_pc_linux_gnu_CPPFLAGS:-CPPFLAGS}
#CFLAGS=${MY_CFLAGS[@]}
#CXXFLAGS=${MY_CFLAGS[@]}
#LDFLAGS=${MY_LDFLAGS[@]}

## note 2016-04-11: things changed now
##   computed_CFLAGS=${x86_64_pc_linux_gnu_CFLAGS:=-march=native -O2 -pipe}
eval "${CHOST//-/_}_CFLAGS=\${MY_CFLAGS[@]}"
eval "${CHOST//-/_}_CXXFLAGS=\${MY_CFLAGS[@]}"
eval "${CHOST//-/_}_CPPLAGS="
eval "${CHOST//-/_}_LDFLAGS=\${MY_LDFLAGS[@]}"

### Advanced customization
## NOTE: bashrc is sourced once in builtin_init phase only when cave-perform

if [[ x${USE_DISTCC} != "xno" ]]; then
    #ECONF_WRAPPER="wrap_ebuild_phase distcc_allow_net :WRAP_END:"
    EMAKE_WRAPPER="wrap_ebuild_phase distcc_setup_hosts; distcc_allow_net;"

    ## in the case of cmake.exlib, src_configure will invoke ecmake()
    ## which doesn't provide a customization point, hence it is not
    ## possible to allow net_access in sandboxing. But this is ok, since the only thing
    ##
    ## A side effect of the hack is that distcc will be alway failed in src_configure phase
    source /etc/paludis/myconfig/scripts/utils
    distcc_setup_path
fi
