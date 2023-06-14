from pathlib import Path
from action.action_handler import Action_handler
from action.set_files_mixin import Set_files_mixin
from action.spec_configuration_mixin import Spec_configuration_mixin

class Suggestions_handler(Spec_configuration_mixin, Set_files_mixin, Action_handler):
    script_path_pattern = '^(/etc/paludis/)?suggestions(.bash)?$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            f'{config["spec"]:<{16}}\t{config["suggestions"]}'
            for config in self.active_spec_configurations
            if config['type'] == 'package'
            and 'suggestions' in config
            and config['suggestions'] is not None
        )

    pass
