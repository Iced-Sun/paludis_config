#!/usr/bin/env python3
from action import General_handler, Repository_handler

import sys
from pathlib import Path

# the first argument is always the script itself
if len(sys.argv) > 1:
    # <action>.bash or <action>
    script_path = Path(sys.argv[1])
    suffix = script_path.suffix
    action = str(script_path).split('/')[0]
    sub_action = '' if script_path.stem == action else script_path.stem
    pass

match action:
    case 'general':
        print(General_handler().configuration)
        pass
    case 'repositories':
        print(Repository_handler(sub_action).configuration)
