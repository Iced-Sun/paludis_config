#!/bin/bash

echo format = exndbam

if [[ `hostname` == "laptop-x61" ]]; then
#    echo location = ${root}/var/db/paludis/repositories/installed
    echo "error"
else
    chroot=/media/btrfs_raid6_MD1000_4_WD1003FBYX/linux/os/base/exherbo
    echo root = ${chroot}
    echo name = installed-base
    echo location = ${chroot}/var/db/paludis/repositories/installed
fi

