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
    libXxf86misc|db)
	LTO=fix
	;;&
    iputils|sysfsutils|file)
	LTO=hack
	;;&
    test-gcc)
	LTO=false
	;;&
    *)
	;;
esac    

### combination of compiler and lto
if [[ ${CLANG}x = truex ]]; then
    CC="clang"
    CXX="clang++"
    # clang-lto need special setting
    if [[ ${LTO}x != falsex ]]; then
	PATH="/etc/paludis/myconfig/scripts:${PATH}"
	AR="clang-ar"
	NM="nm --plugin /usr/lib64/LLVMgold.so"
	RANLIB=/bin/true
    fi
fi

if [[ ${LTO}x != falsex ]]; then
    CFLAGS+=( -flto )
    if [[ ${LTO} = fix ]]; then
	if [[ ${CLANG} = true ]]; then
	    LDFLAGS+=( -Wc,-flto ) # for clang (libXxf86misc)
	else
	    LDFLAGS+=( -Wl,-flto ) # for gcc (db)
	fi
    elif [[ ${LTO} = hack ]]; then
	CC+=" -flto"
	CXX+=" -flto"
    else
	LDFLAGS+=( -flto ) # for normal one
    fi
fi
    
### finalize
CFLAGS="${CFLAGS[@]}"
CXXFLAGS="${CFLAGS}"
LDFLAGS="${LDFLAGS[@]}"

# extra econf
ECONF_WRAPPER="append_configure_option ${#EXTRA_ECONF[@]} ${EXTRA_ECONF[@]}"
