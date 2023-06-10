from pathlib import Path
from action.action_handler import Action_handler

class Bashrc_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?bashrc$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            f'''{key}="{value[0]['value']}"'''
            for key, value in self._spec_environ.items()
        )

    pass
