import os
from pathlib import Path
from action.action_handler import Action_handler

class Bashrc_handler(Action_handler):
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
            env = { key: ' '.join(v['value'] for v in values if v['spec'] == '*/*') for key, values in self._spec_environ.items() }
            pass
        else:
            env = {}
            for key, values in self._spec_environ.items():
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
        for target in self._TARGETS:
            env[f'{target.replace("-", "_")}_CFLAGS'] = env['CFLAGS']
            env[f'{target.replace("-", "_")}_CXXFLAGS'] = env['CFLAGS']
            env[f'{target.replace("-", "_")}_LDFLAGS'] = env['LDFLAGS']
            pass

        return '\n'.join(f'{k}="{v}"' for k, v in env.items())

    pass
