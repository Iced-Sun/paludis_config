add_mirror()
{
    url_base=$1
    set -- $2
    
    url="$url_base/${2:-$1}"
    name=$1

    num=${#MIRRORS[@]}
    for ((i=0; i<$num; i++)); do
	set -- ${MIRRORS[i]}
	if [[ $name == $1 ]]; then
	    MIRRORS[i]+=" $url"
	    return 0
	fi
    done
    MIRRORS+=( "$name $url" )
    return 0
}

add_site()
{
    url_base=$1; shift
    while [[ $# -gt 0 ]]; do
	add_mirror "$url_base" "$1"
	shift
    done
}

MIRRORS=()

## IPv4/v6 mirrors
BJTU=( http://debian.bjtu.edu.cn
    apache cpan cran 'ctan CTAN' debian freebsd 'gentoo gentoo/distfiles' gimp gnome gnu kde 'kernel kernel/pub' 'libreoffice tdf/libreoffice' )
TSU=( http://mirrors.tuna.tsinghua.edu.cn
    apache 'ctan CTAN' 'cran CRAN' 'ctan CTAN' debian freebsd 'gentoo gentoo/distfiles' gnu 'kernel kernel/pub' opensuse )
USTC=( http://mirrors.ustc.edu.cn
    'cpan CPAN' 'cran CRAN' 'ctan CTAN' debian freebsd 'gentoo gentoo/distfiles' gnome gnu kde 'kernel linux-kernel' opensuse )
HEANET=( http://heanet.dl.sourceforge.net sourceforge )

## IPv4 only mirrors
NETEASE=( http://mirrors.163.com
    cpan debian 'freebsd FreeBSD' 'gentoo gentoo/distfiles' 'opensuse openSUSE')

add_site "${BJTU[@]}"
add_site "${TSU[@]}"
add_site "${USTC[@]}"
add_site "${HEANET[@]}"
#if ( ifconfig | grep 'inet6 2001:' ) >/dev/null 2>&1; then
#fi
add_site "${NETEASE[@]}"

## echo mirrors
for m in "${MIRRORS[@]}"; do
    echo ${m}
done
