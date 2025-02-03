from pathlib import Path
import os, re

class Action_handler:
    arch_target_pattern = re.compile('^(x86_64|i386|i686|arm|mips|aarch64)(.*)-(.+)-(.+)-(.+)$')

    @classmethod
    def match(cls, script_path, action):
        if re.match(cls.script_path_pattern, str(script_path)) is not None:
            return True

        if action is not None and re.match(cls.script_path_pattern, action) is not None:
            return True

        return False

    def __init__(self, script_path: Path):
        ## save the wrapper path
        self._wrapper_path = script_path.resolve()

        ## induce the actions from script name
        paludis_config_dir = os.environ['PALUDIS_CONFIG_DIR'] if 'PALUDIS_CONFIG_DIR' in os.environ else '/etc/paludis'

        if script_path.is_absolute():
            relative_script_path = script_path.relative_to(paludis_config_dir)
            pass
        else:
            relative_script_path = script_path
            pass

        parts = relative_script_path.parts
        self._action = Path(parts[0]).stem
        self._sub_action = Path(parts[1]).stem if len(parts) == 2 else None

        ### end of __init__()
        pass

    ### end of class Action_handler
    pass
