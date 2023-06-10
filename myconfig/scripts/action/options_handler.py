import re
from pathlib import Path
from action.action_handler import Action_handler

class Options_handler(Action_handler):
    script_path_pattern = re.compile('^(/etc/paludis/)?options(.bash)?$')

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            f'{config["spec"]:<{24}}\t{config["options"]}'
            for config in self._spec_config
            if config['type'] == 'package' and config['options'] is not None
        )

    pass
