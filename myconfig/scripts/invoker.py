#!/usr/bin/env python3
from action.general_handler import General_handler
from action.platforms_handler import Platforms_handler
from action.mirrors_handler import Mirrors_handler

from action.repositories_handler import Repository_handler
from action.sets_handler import Sets_handler

from action.package_mask_handler import Package_mask_handler
from action.package_unmask_handler import Package_unmask_handler

from action.suggestions_handler import Suggestions_handler
from action.options_handler import Options_handler

import sys
from pathlib import Path

# the first argument is always the script itself
if len(sys.argv) > 1:
    # <action>.bash or <action>
    script_path = Path(sys.argv[1])
    pass

handled = False
for Handler in Platforms_handler, General_handler, Mirrors_handler, Repository_handler, Sets_handler, Package_mask_handler, Package_unmask_handler, Suggestions_handler, Options_handler:
    if Handler.script_path_pattern.match(str(script_path)):
        print(Handler(script_path).configuration)
        handled = True
        pass
    pass

if not handled:
    raise Exception(f'unhandled script <{script_path}>')
