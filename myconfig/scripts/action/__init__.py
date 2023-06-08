import os, re
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

class General_handler(Action_handler):
    script_path_pattern = re.compile('^(/etc/paludis/)?general(.bash)?$')

    def __init__(self, script_path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return 'world = $root/var/db/paludis/repositories/installed/world'
    pass

class Repository_handler(Action_handler):
    script_path_pattern = re.compile('^(/etc/paludis/)?repositories/(.+)(.bash)?$')
    arch_target_pattern = re.compile('^(x86_64|i386|i686|arm|mips)(.*)-(.+)-(.+)-(.+)$')

    def __init__(self, script_path: str):
        super().__init__(script_path)

        #CHOST
        #print(os.environ)
        if self._sub_action == 'installed':
            arch_target_pattern_match = Repository_handler.arch_target_pattern.match('x86_64-pc-linux-gnu')
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
'''
            case _:
                raise Exception('do not support the repository {}'.format(self._sub_action))
        pass

    pass
