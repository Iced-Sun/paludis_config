from pathlib import Path
import re

class Set_files_mixin:
    @property
    def configured_set_files(self):
        if not hasattr(self, '_configured_set_files'):
            self._init_configured_set_files()
            pass
        return self._configured_set_files

    def _init_configured_set_files(self):
        wrapper_path = self._script_path.resolve()
        config_path = wrapper_path.parents[1]
        set_path = config_path / 'sets'

        self._configured_set_files = {
            'machine-set': list(set_path.glob('@*')),
            'general-set': list(set_path.glob('[0-9][0-9]-*')),
            'weak-set': list(set_path.glob('[?]*'))
        }
        pass

    @property
    def active_set_files(self):
        if not hasattr(self, '_active_set_files'):
            self._init_active_set_files()
            pass
        return self._active_set_files

    def _init_active_set_files(self):
        self._active_set_files = []

        ## initialize active set by looking at the installed world file
        # we have funny dependencies: active set files -> world file ->
        # repositories/installed -> set files; need some sort-out
        world_sets = []
        with Path('/var/db/paludis/repositories/installed/world').open() as f:
            world_sets = [line for line in f.read().splitlines() if '/' not in line]
            pass

        ## find the active sets by matching against the world set
        for world_set in world_sets:
            # uuid introduces a machine set
            if re.match('[0-9a-f]{32}', world_set):
                # fetch the real machine-id
                machine_id = None

                with Path('/etc/machine-id').open() as f:
                    machine_id = f.read().splitlines()[0]
                    pass

                # check if the machine-id matches system setting
                if world_set == machine_id:
                    self._active_set_files.append(
                        next(_ for _ in self.configured_set_files['machine-set'] if _.match(f'*@{machine_id}:*'))
                    )
                    pass
                pass

            # match a general set
            else:
                self._active_set_files.append(
                    next(_ for _ in self.configured_set_files['general-set'] if _.match(f'*/[0-9][0-9]-{world_set}'))
                )
                pass
            pass

        ## gather dependecy set names from seen active world sets
        dependency_set_names = []
        for active_set_file in self._active_set_files:
            with active_set_file.open() as f:
                for line in f.read().splitlines():
                    m = re.match('^(?P<set_name>[-a-zA-Z0-9]+)(\t+.+)?$', line)
                    if m:
                        dependency_set_names.append(m.group('set_name'))
                        pass
                    pass
                pass

            pass

        ## find the declared dependency sets
        for dependency_set_name in dependency_set_names:
            if next((_ for _ in self._active_set_files if _ == dependency_set_name), None) is not None:
                continue

            self._active_set_files.append(
                next(_ for _ in self.configured_set_files['general-set'] if _.match(f'*/[0-9][0-9]-{dependency_set_name}'))
            )
            pass

        # end of self._init_active_set_names()
        pass

    ### end of Set_files_mixin
    pass
