#!/bin/bash

cat <<EOF
format = e
location = ${root}/var/db/paludis/repositories/subi-bin
sync = git+ssh://git@github.com/sunbing81/subi-bin.git
sync_options = --no-reset
importance = 100
EOF

if [[ `hostname` == "fs-3.bir.pku.edu.cn" ]]; then
    cat <<EOF

binary_destination = true
binary_distdir = /srv/subi-bin
binary_keywords_filter = amd64 ~amd64
binary_uri_prefix = mirror://subi-bin/
EOF
fi
