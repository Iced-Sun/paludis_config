import re
from pathlib import Path
from action.action_handler import Action_handler

class Package_mask_handler(Action_handler):
    script_path_pattern = re.compile('^(/etc/paludis/)?package_mask(.bash)?$')

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(spec['spec'] for spec in self._parsed_spec if spec['mark'] == '-' and spec['type'] == 'package')
