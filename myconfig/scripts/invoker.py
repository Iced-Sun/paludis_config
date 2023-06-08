#!/usr/bin/env python3
from action import General_handler, Repository_handler

import sys
from pathlib import Path

# the first argument is always the script itself
if len(sys.argv) > 1:
    # <action>.bash or <action>
    script_path = Path(sys.argv[1])
    pass

for Handler in General_handler, Repository_handler:
    if Handler.script_path_pattern.match(str(script_path)):
        print(Handler(script_path).configuration)
        pass
    pass
