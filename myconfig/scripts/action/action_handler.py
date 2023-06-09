from pathlib import Path
import os, re

class Action_handler:
    def __init__(self, script_path: Path):
        ## configure the environment
        # paths and files
        self._paludis_config_dir = os.environ['PALUDIS_CONFIG_DIR'] if 'PALUDIS_CONFIG_DIR' in os.environ else '/etc/paludis'
        self._wrapper_path = script_path.resolve()
        self._config_path = self._wrapper_path.parents[1]
        self._set_path = self._config_path / 'sets'
        # hard-coded, should be consistent with the value in
        # repositories/installed.conf
        self._world_file = '/var/db/paludis/repositories/installed/world'

        # installed specs
        # TODO what is -cross-installed in world file looks like
        with Path(self._world_file).open() as f:
            self._installed_spec = [{
                'name': line,
                'type': 'package' if '/' in line else 'set'
            } for line in f.read().splitlines()]
            pass

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
        self._machine_sets = sorted(self._set_path.glob('@*'))
        self._general_sets = sorted(self._set_path.glob('[0-9][0-9]-*'))
        self._weak_sets = sorted(self._set_path.glob('[?]*'))
        self._active_sets = []

        ## find the active sets
        # 1. match against the world file
        for installed in self._installed_spec:
            # we don't care packages in the world file
            if installed['type'] != 'set':
                continue

            # uuid introduces a machine set
            if re.match('[0-9a-f]{32}', installed['name']):
                # fetch the real machine-id
                machine_id = None

                with Path('/etc/machine-id').open() as f:
                    machine_id = f.read().splitlines()[0]
                    pass

                # check if the machine-id matches system setting
                if installed['name'] == machine_id:
                    self._active_sets += [{
                        'name': installed['name'],
                        # use next() to find exactly one set
                        'path': next(s for s in self._machine_sets if s.match(f'*@{machine_id}:*')),
                        'type': 'machine-set',
                        'pulled_by': 'world'
                    }]
                    pass
                pass
            # match a general set
            else:
                self._active_sets += [{
                    'name': installed['name'],
                    # use next() to find exactly one general set
                    'path': next(s for s in self._general_sets if s.match(f'*/[0-9][0-9]-{installed["name"]}')),
                    'type': 'general-set',
                    'pulled_by': 'world'
                }]
                pass
            pass

        # 2.
        print(self._active_sets)
        pass

    # end of class Action_handler
    pass
