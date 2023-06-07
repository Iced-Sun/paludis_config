#!/usr/bin/env python3
from action import General_handler

import sys
from pathlib import Path

# the first argument is always the script itself
if len(sys.argv) > 1:
    # <action>.bash or <action>
    action = Path(sys.argv[1]).name
    if (action.endswith('.bash')):
        action = action.split('.')[0]
        pass
    pass

match action:
    case 'general':
        print(General_handler().configuration)
        pass
