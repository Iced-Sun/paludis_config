import re
from pathlib import Path
from action.action_handler import Action_handler

class General_handler(Action_handler):
    script_path_pattern = re.compile('^(/etc/paludis/)?general(.bash)?$')

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return 'world = $root/var/db/paludis/repositories/installed/world'
    pass
