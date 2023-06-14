import re
from pathlib import Path
from action.action_handler import Action_handler
from action.set_files_mixin import Set_files_mixin
from action.host_mixin import Host_mixin

class Repository_handler(Host_mixin, Set_files_mixin, Action_handler):
    script_path_pattern = '^(/etc/paludis/)?repositories/(.+)(.bash)?$'

    @property
    def configuration(self) -> str:
        if self._sub_action == 'installed':
            arch_target_pattern_match = Action_handler.arch_target_pattern.match(self.host)
            format = 'exndbam'
            pass

        elif Action_handler.arch_target_pattern.match(self._sub_action):
            arch_target_pattern_match = Action_handler.arch_target_pattern.match(self._sub_action)
            format = 'exndbam'
            pass

        if format == 'exndbam':
            target_triple = {
                'target': arch_target_pattern_match.group(0),
                'arch': arch_target_pattern_match.group(1),
                'sub': arch_target_pattern_match.group(2),
                'vendor': arch_target_pattern_match.group(3),
                'sys': arch_target_pattern_match.group(4),
                'env': arch_target_pattern_match.group(5)
            }

            if self._sub_action == 'installed':
                location = 'installed'
                pass
            else:
                location = f'cross-installed/{target_triple["target"]}'
                pass

            configurations = [
                'format = exndbam',
                f'location = $root/var/db/paludis/repositories/{location}',
                f'name = {self._sub_action}',
                f'split_debug_location = /usr/{target_triple["target"]}/lib/debug',
                f'tool_prefix = {target_triple["target"]}-'
            ]

            if self._sub_action != 'installed':
                configurations.append(f'cross_compile_host = {target_triple["target"]}')
                pass
            pass

        return '\n'.join(configurations)

    pass
