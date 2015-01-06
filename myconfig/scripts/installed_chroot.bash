#!/bin/bash

echo format = exndbam

if [[ `hostname` == "fs-3.bir.pku.edu.cn" ]]; then
    chroot=/media/btrfs_raid6_MD1000_4_WD1003FBYX/linux/os/base/exherbo
    echo root = ${chroot}
    echo name = installed-base
    echo location = /var/db/paludis/repositories/installed/chroot/minimal
else
    echo root = should-not-exist
    echo name = should-not-exist
    echo location = /var/empty
fi

