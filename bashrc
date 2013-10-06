#!/bin/bash

## functions
has_ipv6()
{
    {
	which ifconfig && ifconfig | grep '2001:da8' && return 0 || return 1
    } >/dev/null 2>&1
}

is_in_2112()
{
    {
	which ifconfig && ifconfig | grep '10.2.112' && return 0 || return 1
    } >/dev/null 2>&1
}

append_configure_option()
{
    n="$1"
    shift

    opts=()
    for ((i=0; i<n; ++i)); do
	opts+=( "$1" )
	shift
    done

    edo "$@" "${opts[@]}"
}

### default flags
CHOST="x86_64-pc-linux-gnu"
CFLAGS=( -O3 -pipe )
LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags
EXTRA_ECONF=( --disable-static )
CLANG=true
LTO=true

### special care
case "${PN}" in
    xulrunner)
	EXTRA_ECONF+=( --disable-elf-hack )
	EXJOBS=5
	;;&
    ocaml|notmuch)
#	LDFLAGS=()
	;;&
    notmuch|db|nettle)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]/--disable-static/} )
	;;&
    luatex|glib|schroot|xulrunner|firefox)
	CLANG=false
	;;&
    rxvt-unicode|gcc) # urxvt compiles with -flto, but not execute correctly
	LTO=false
	;;&
    *)
	;;
esac    

### combination of compiler and lto
if [[ ${CLANG}x == truex ]]; then
    CC="clang"
    CXX="clang++"
    # clang-lto need special setting
    if [[ ${LTO}x == truex ]]; then
	PATH="/etc/paludis/myconfig/scripts:${PATH}"
	AR="clang-ar"
	NM="nm --plugin /usr/lib64/LLVMgold.so"
	RANLIB=/bin/true
    fi
fi

if [[ ${LTO}x == truex ]]; then
    # libtool and a lot of compiling logic filter out -flto, so hack CC and CXX to enable lto unconditionally
#	CC="clang -flto"
#	CXX="clang++ -flto"
#    CFLAGS+=( -flto )
#    LDFLAGS+=( -flto )
    CC="${CC} -flto"
    CXX="${CXX} -flto"
fi
    
### finalize
[[ -f /etc/paludis/myconfig/bashrc.`hostname` ]] && source /etc/paludis/myconfig/bashrc.`hostname`

CFLAGS="${CFLAGS[@]}"
CXXFLAGS="${CFLAGS}"
LDFLAGS="${LDFLAGS[@]}"
ECONF_WRAPPER="append_configure_option ${#EXTRA_ECONF[@]} ${EXTRA_ECONF[@]}"
