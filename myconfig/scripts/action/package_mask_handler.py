from pathlib import Path
from action.action_handler import Action_handler
from action.set_files_mixin import Set_files_mixin
from action.destination_mixin import Destination_mixin
from action.spec_configuration_mixin import Spec_configuration_mixin

class Package_mask_handler(Spec_configuration_mixin, Destination_mixin, Set_files_mixin, Action_handler):
    script_path_pattern = '^(/etc/paludis/)?package_mask(.bash)?$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return '\n'.join(
            config['spec']
            for config in self.active_spec_configurations
            if config['mark'] == '-' and config['type'] == 'package'
        )

    pass
