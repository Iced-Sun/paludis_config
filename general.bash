#!/bin/bash

echo root = /
if [[ `hostname` == "laptop-x61" ]]; then
    echo world = ${root}/var/db/paludis/repositories/installed/world
else
    echo world = ${root}/var/local/db/paludis/repositories/installed/world
fi
