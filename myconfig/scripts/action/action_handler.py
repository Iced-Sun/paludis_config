from pathlib import Path
import os

class Action_handler:
    def __init__(self, script_path: Path):
        ## configure the environment
        self._paludis_config_dir = os.environ['PALUDIS_CONFIG_DIR'] if 'PALUDIS_CONFIG_DIR' in os.environ else '/etc/paludis'
        self._wrapper_path = script_path.resolve()
        self._config_path = self._wrapper_path.parents[1]
        self._set_path = self._config_path / 'sets'

        ## induce the action
        if script_path.is_absolute():
            script_path = script_path.relative_to(self._paludis_config_dir)
            pass

        script_path_parts = script_path.parts

        self._action = Path(script_path_parts[0]).stem
        self._sub_action = Path(script_path_parts[1]).stem if len(script_path_parts) == 2 else None

        ## parse our own set spec
        self._parse_sets()
        pass

    def _parse_sets(self):
        pass
    pass
