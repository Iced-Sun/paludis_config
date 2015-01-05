#!/bin/bash

cat <<EOF
format = e
location = ${root}/var/db/paludis/repositories/exherbo-binary
sync = git+ssh://git@github.com/sunbing81/subi-bin.git
sync_options = --no-reset
importance = 100
EOF

if [[ `hostname` == "fs-3.bir.pku.edu.cn" ]]; then
    cat <<EOF
binary_destination = true
binary_distdir = /media/btrfs_raid6_MD1000_4_WD1003FBYX/linux/exherbo-binary
binary_keywords_filter = amd64 ~amd64
binary_uri_prefix = mirror://exherbo-binary/
EOF
fi
