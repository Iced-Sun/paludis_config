import os
from pathlib import Path
from action.action_handler import Action_handler
from action.set_files_mixin import Set_files_mixin
from action.host_mixin import Host_mixin
from action.target_mixin import Target_mixin
from action.destination_mixin import Destination_mixin
from action.spec_configuration_mixin import Spec_configuration_mixin

class Bashrc_handler(Spec_configuration_mixin, Destination_mixin, Target_mixin, Host_mixin, Set_files_mixin, Action_handler):
    script_path_pattern = '^(/etc/paludis/)?bashrc$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        category = os.environ['CATEGORY'] if 'CATEGORY' in os.environ else None
        pn = os.environ['PN'] if 'PN' in os.environ else None

        ## TODO this is total mess!
        # assemble environment variables
        if category is None or pn is None:
            # no package set: output wildcards only
            env = { key: ' '.join(v['value'] for v in values if v['spec'] == '*/*') for key, values in self.spec_environment.items() }
            pass
        else:
            env = {}
            # key:    environment variable name
            # values: { spec: package spec; value: environment variable value }[]
            for key, values in self.spec_environment.items():
                # sort by spec to support overriding wildcard values
                values.sort(key=lambda v: v['spec'])

                # search for verbatim value (no modification will be applied)
                value = next((v
                              for v in values
                              if v['spec'].startswith(f'{category}/{pn}')
                              and (
                                  not v['value'].startswith('^-') and not v['value'].startswith('$-')
                              )), None)

                if value is not None:
                    # found verbatim value, save them in values
                    values = [
                        value['value'].split(' ')
                        for value in values
                        # ignore wildcard values
                        if value['spec'].startswith(f'{category}/{pn}')
                    ]
                    pass
                else:
                    # extract the verbatim value of wildcard packages as the base value)
                    value = next((v
                                  for v in values
                                  if v['spec'] == '*/*'
                                  and (
                                      not v['value'].startswith('^-') and not v['value'].startswith('$-')
                                  )), {'value': ''})
                    # save all other complementary values
                    values = [
                        value['value'].split(' ')
                        for value in values
                        if value['spec'].startswith(f'{category}/{pn}')
                        or (
                            value['spec'] == '*/*'
                            # exclude the wildcard verbatim values
                            and (
                                value['value'].startswith('^-') or value['value'].startswith('$-')
                            )
                        )
                    ]
                    pass

                value = value['value'].split(' ')

                # append or delete modifications
                for v in values:
                    for vv in v:
                        if vv.startswith('^-'):
                            value.append(vv[1:])
                            pass
                        elif vv.startswith('$-'):
                            value.remove(vv[1:]) if vv[1:] in value else None
                            pass
                        continue
                    continue

                # set the value
                env[key] = ' '.join(value)
                pass
            pass

        # complete unprefixed host flags
        if 'CXXFLAGS' not in env: env['CXXFLAGS'] = env['CFLAGS']

        # complete prefixed host flags
        _host = self.host.replace('-', '_')
        env[f'{_host}_CFLAGS'] = env['CFLAGS']
        env[f'{_host}_CXXFLAGS'] = env['CXXFLAGS']
        env[f'{_host}_LDFLAGS'] = env['LDFLAGS']

        # complete target flags
        for target in self.configured_targets:
            _target = target.replace('-', '_')
            if _target is not None:
                if f'{_target}_CFLAGS' in env and f'{_target}_CXXFLAGS' not in env:
                    env[f'{_target}_CXXFLAGS'] = env[f'{_target}_CFLAGS']
                    pass
                pass
            continue

        # clean up the unprefixed host flags
        if 'CFLAGS' in env: del env['CFLAGS']
        if 'CPPFLAGS' in env: del env['CPPFLAGS']
        if 'CXXFLAGS' in env: del env['CXXFLAGS']
        if 'CXXCPPFLAGS' in env: del env['CXXCPPFLAGS']
        if 'LDFLAGS' in env: del env['LDFLAGS']

        return '\n'.join(f'{k}="{v}"' for k, v in env.items())

    pass
