from pathlib import Path
from action.action_handler import Action_handler

class Package_unmask_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?package_unmask(.bash)?$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            config['spec']
            for config in self._spec_config
            if config['mark'] == '+' and config['type'] == 'package'
        )

    pass
