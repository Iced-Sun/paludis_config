from pathlib import Path
from action.action_handler import Action_handler
from action.set_files_mixin import Set_files_mixin
from action.target_mixin import Target_mixin
from action.destination_mixin import Destination_mixin
from action.spec_configuration_mixin import Spec_configuration_mixin

class Sets_handler(Spec_configuration_mixin, Destination_mixin, Target_mixin, Set_files_mixin, Action_handler):
    script_path_pattern = '^(/etc/paludis/)?sets/(.+)(.bash)?$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            f'* {config["spec"]}'
            for config in self.active_spec_configurations
            if config['type'] == 'package'
            and config['is_dependecy'] is False
            and config['has_wildcard'] is False
        )

    pass
