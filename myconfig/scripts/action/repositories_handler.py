import re
from pathlib import Path
from action.action_handler import Action_handler

class Repository_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?repositories/(.+)(.bash)?$'

    def __init__(self, script_path: Path):
        super().__init__(script_path)

        if self._sub_action == 'installed':
            arch_target_pattern_match = Action_handler.arch_target_pattern.match('x86_64-pc-linux-gnu')
            self._format = 'exndbam'
            self._target_triple = {
                'target': arch_target_pattern_match.group(0),
                'arch': arch_target_pattern_match.group(1),
                'sub': arch_target_pattern_match.group(2),
                'vendor': arch_target_pattern_match.group(3),
                'sys': arch_target_pattern_match.group(4),
                'env': arch_target_pattern_match.group(5)
            }
            pass

        elif Repository_handler.arch_target_pattern.match(self._sub_action):
            arch_target_pattern_match = Repository_handler.arch_target_pattern.match(self._sub_action)
            self._format = 'exndbam'
            self._target_triple = {
                'target': arch_target_pattern_match.group(0),
                'arch': arch_target_pattern_match.group(1),
                'sub': arch_target_pattern_match.group(2),
                'vendor': arch_target_pattern_match.group(3),
                'sys': arch_target_pattern_match.group(4),
                'env': arch_target_pattern_match.group(5)
            }
            pass

        pass

    @property
    def configuration(self) -> str:
        match self._format:
            case 'exndbam':
                return f'''format = exndbam
location = $root/var/db/paludis/repositories/{'installed' if self._sub_action == 'installed' else f'cross-installed/{self._target_triple["target"]}'}
name = {self._sub_action}
split_debug_location = /usr/{self._target_triple['target']}/lib/debug
tool_prefix = {self._target_triple['target']}-
{'' if self._sub_action == 'installed' else f'cross_compile_host = {self._target_triple["target"]}'}
'''
            case _:
                raise Exception('do not support the repository {}'.format(self._sub_action))
        pass

    pass
