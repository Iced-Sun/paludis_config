from pathlib import Path

class Set_files_mixin:
    def __init__(self, script_path: Path):
        super().__init__(script_path)

        wrapper_path = script_path.resolve()
        config_path = wrapper_path.parents[1]
        set_path = config_path / 'sets'

        self._configured_set_paths = {
            'machine-set': set_path.glob('@*'),
            'general-set': set_path.glob('[0-9][0-9]-*'),
            'weak-set': set_path.glob('[?]*')
        }

        ### end of __init__()
        pass

    ### end of Set_files_mixin
