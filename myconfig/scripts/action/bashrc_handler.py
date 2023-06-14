import os
from pathlib import Path
from action.action_handler import Action_handler
from action.set_files_mixin import Set_files_mixin
from action.target_mixin import Target_mixin
from action.destination_mixin import Destination_mixin
from action.spec_configuration_mixin import Spec_configuration_mixin

class Bashrc_handler(Spec_configuration_mixin, Destination_mixin, Target_mixin, Set_files_mixin, Action_handler):
    script_path_pattern = '^(/etc/paludis/)?bashrc$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        category = os.environ['CATEGORY'] if 'CATEGORY' in os.environ else None
        pn = os.environ['PN'] if 'PN' in os.environ else None

        # no package set: print wildcards only
        if category is None or pn is None:
            env = { key: ' '.join(v['value'] for v in values if v['spec'] == '*/*') for key, values in self.spec_environment.items() }
            pass
        else:
            env = {}
            for key, values in self.spec_environment.items():
                # filter matching values
                values = [
                    value['value'].split(' ') for value in values
                    if value['spec'] == f'{category}/{pn}'
                    or value['spec'] == f'{category}/*'
                    or value['spec'] == '*/*'
                ]
                if len(values) == 0:
                    continue

                # search for the value base
                value = next(v for v in values if not v[0].startswith('^') or not v[0].startswith('$'))

                # append or delete modifications
                for v in values:
                    for vv in v:
                        if vv.startswith('^'):
                            value.append(vv[1:])
                            pass
                        elif vv.startswith('$'):
                            value.remove(vv[1:]) if vv[1:] in value else None
                            pass
                        pass
                    pass

                # set the value
                env[key] = ' '.join(value)
                pass
            pass

        # target fixes: CFLAGS, LDFLAGS will be never used for building
        for target in self.configured_targets:
            _target = target.replace("-", "_")
            if f'{_target}_CFLAGS' not in env:
                env[f'{_target}_CFLAGS'] = env['CFLAGS']
                pass
            if f'{_target}_LDFLAGS' not in env and 'LDFLAGS' in env:
                env[f'{_target}_LDFLAGS'] = env['LDFLAGS']
                pass

            env[f'{_target}_CXXFLAGS'] = env[f'{_target}_CFLAGS']
            pass

        return '\n'.join(f'{k}="{v}"' for k, v in env.items())

    pass
