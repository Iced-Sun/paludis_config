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

## IPv6 mirrors
BJTU6=( http://mirror6.bjtu.edu.cn
    apache cpan cran 'ctan CTAN' debian fedora freebsd 'gentoo gentoo/distfiles' gimp gnome gnu gnu-alpha gnupg kde 'kernel kernel/pub' openbsd sourceforge )
TSU6=( http://mirrors.6.tuna.tsinghua.edu.cn
    'ctan CTAN' debian fedora freebsd 'gentoo gentoo/distfiles' gnu 'kernel kernel/pub' opensuse sourceforge )
USTC6=( http://mirrors.ustc.edu.cn
    'cpan CPAN' 'cran CRAN' 'ctan CTAN' debian fedora freebsd 'gentoo gentoo/distfiles' gnome gnu kde opensuse )
FUNET=( ftp://ftp.funet.fi/pub/mirrors 'gnu-alpha alpha.gnu.org' )
HEANET=( ftp://ftp.heanet.ie/mirrors gnupg 'openbsd OpenBSD' )
HEANET1=( http://heanet.dl.sourceforge.net sourceforge )

## IPv4 mirrors
BJTU=( http://mirror.bjtu.edu.cn
    apache cpan cran 'ctan CTAN' debian fedora freebsd 'gentoo gentoo/distfiles' gimp gnome gnu gnu-alpha gnupg kde 'kernel kernel/pub' openbsd sourceforge )
NETEASE=( http://mirrors.163.com
    cpan debian fedora 'freebsd FreeBSD' 'gentoo gentoo/distfiles' 'opensuse openSUSE')

if ( ifconfig | grep 'inet6 2001:' ) >/dev/null 2>&1; then
    add_site "${BJTU6[@]}"
    add_site "${TSU6[@]}"
    add_site "${USTC6[@]}"
    add_site "${FUNET[@]}"
    add_site "${HEANET[@]}"
    add_site "${HEANET1[@]}"
fi
add_site "${NETEASE[@]}"
add_site "${BJTU[@]}"

## echo mirrors
for m in "${MIRRORS[@]}"; do
    echo ${m}
done
