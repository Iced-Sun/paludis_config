#!/bin/bash

echo format = exndbam
if [[ `hostname` == "laptop-x61" ]]; then
    echo location = ${root}/var/db/paludis/repositories/installed
else
    echo location = ${root}/var/local/db/paludis/repositories/installed
fi

