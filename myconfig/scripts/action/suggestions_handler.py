from pathlib import Path
from action.action_handler import Action_handler

class Suggestions_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?suggestions(.bash)?$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            f'{config["spec"]:<{16}}\t{config["suggestions"]}'
            for config in self._spec_config
            if config['mark'] != '@' and config['type'] == 'package'
            and config['suggestions'] is not None
        )

    pass
