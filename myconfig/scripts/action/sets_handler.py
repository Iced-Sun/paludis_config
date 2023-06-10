import re
from pathlib import Path
from action.action_handler import Action_handler

class Sets_handler(Action_handler):
    script_path_pattern = re.compile('^(/etc/paludis/)?sets/(.+)(.bash)?$')

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            f'* {config["spec"]}'
            for config in self._spec_config
            if config['type'] == 'package'
            and config['is_dependecy'] is False
            and config['has_wildcard'] is False
        )

    pass
