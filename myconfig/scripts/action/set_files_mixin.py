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
        config_path = self._wrapper_path.parents[1]
        set_path = config_path / 'sets'
        self._configured_set_files = {
            'machine-set': sorted(set_path.glob('@*')),
            'general-set': sorted(set_path.glob('[0-9a-z][0-9]-*')),
            'weak-set': sorted(set_path.glob('[?][0-9][0-9]-*')),
            'feature-set': sorted(set_path.glob('[?][!0-9]*'))
        }

        ## feature-set could be deactivated by the machine-set
        self._init_active_set_files()
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
            world_sets = [line for line in f.read().splitlines() if line]
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
                    next(_ for _ in self.configured_set_files['general-set'] if _.match(f'*/[0-9a-z][0-9]-{world_set}'))
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
            ## the set is already handled
            if next((_ for _ in self._active_set_files if _.match(f'*-{dependency_set_name}')), None) is not None:
                continue

            next_is_general_set = next((_ for _ in self.configured_set_files['general-set'] if _.match(f'*/[0-9a-z][0-9]-{dependency_set_name}')), None)
            ## the dependency is a general set, mark it an active_set_files set
            if next_is_general_set:
                self._active_set_files.append(next_is_general_set)
                pass
            ## the dependency is a deactivated feature set
            else:
                next_is_feature_set = next((_ for _ in self.configured_set_files['feature-set'] if _.match(f'*/[?]{dependency_set_name[1:]}')), None)
                if next_is_feature_set:
                    self._configured_set_files['feature-set'].remove(next_is_feature_set)
                    pass
            pass

        ## sort active sets
        self._active_set_files.sort(key = lambda path: '~~~~' if path.name.startswith('@') else path.name)
        # end of self._init_active_set_names()
        pass

    ### end of Set_files_mixin
    pass
