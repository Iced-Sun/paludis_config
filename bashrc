#!/bin/bash
source /etc/paludis/myconfig/scripts/utils

### default flags
CHOST="x86_64-pc-linux-gnu"
CFLAGS=( -O3 -pipe )
LDFLAGS=( -Wl,-O1 -Wl,--as-needed -Wl,--sort-common )
EXJOBS=3

### default custom flags
EXTRA_ECONF=( --disable-static )
CLANG=true
LTO=true

### default host specific flags
[[ -f /etc/paludis/myconfig/host/`hostname`/bashrc ]] && source /etc/paludis/myconfig/host/`hostname`/bashrc

### special care
case "${PN}" in
#    xulrunner)
#	EXTRA_ECONF+=( --disable-elf-hack )
#	EXJOBS=5
#	;;&
#    ocaml|notmuch)
#	LDFLAGS=()
#	;;&
    db)
	EXTRA_ECONF=( ${EXTRA_ECONF[@]/--disable-static/} )
	;;&
    libxkbui|TeXmacs|db)
    	CLANG=false
	;;&
    gcc|db)
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
    CFLAGS+=( -flto )
    LDFLAGS+=( -flto )
fi
    
### finalize
CFLAGS="${CFLAGS[@]}"
CXXFLAGS="${CFLAGS}"
LDFLAGS="${LDFLAGS[@]}"

# extra econf
ECONF_WRAPPER="append_configure_option ${#EXTRA_ECONF[@]} ${EXTRA_ECONF[@]}"
