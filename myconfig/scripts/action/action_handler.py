from pathlib import Path

class Action_handler:
    def __init__(self, script_path: Path):
        if script_path.is_absolute():
            script_path = script_path.relative_to('/etc/paludis')
            pass

        script_path_parts = script_path.parts
        self._action = Path(script_path_parts[0]).stem
        self._sub_action = Path(script_path_parts[1]).stem if len(script_path_parts) == 2 else None
        pass
    pass
