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
            format = 'exndbam'
            arch_target_pattern_match = Action_handler.arch_target_pattern.match(self.host)
            pass
        elif Action_handler.arch_target_pattern.match(self._sub_action):
            format = 'exndbam'
            arch_target_pattern_match = Action_handler.arch_target_pattern.match(self._sub_action)
            pass
        elif self._sub_action.startswith('unavailable'):
            format = 'unavailable'
            pass

        configurations = [
            f'format = {format}',
            f'name = {self._sub_action}'
        ]
        location = self._sub_action

        if format == 'exndbam':
            target_triple = {
                'target': arch_target_pattern_match.group(0),
                'arch': arch_target_pattern_match.group(1),
                'sub': arch_target_pattern_match.group(2),
                'vendor': arch_target_pattern_match.group(3),
                'sys': arch_target_pattern_match.group(4),
                'env': arch_target_pattern_match.group(5)
            }

            if self._sub_action != 'installed':
                location = f'cross-installed/{target_triple["target"]}'
                configurations.append(f'cross_compile_host = {target_triple["target"]}')
                pass

            configurations += [
                f'location = $root/var/db/paludis/repositories/{location}',
                f'name = {self._sub_action}',
                f'split_debug_location = /usr/{target_triple["target"]}/lib/debug',
                f'tool_prefix = {target_triple["target"]}-'
            ]

            pass

        elif format == 'unavailable':
            if self._sub_action == 'unavailable':
                tar = 'exherbo_repositories.tar.bz2'
                pass
            elif self._sub_action == 'unavailable-unofficial':
                tar = 'exherbo_unofficial_repositories.tar.bz2'
                pass

            configurations += [
                f'location = $root/var/db/paludis/repositories/{location}',
                f'sync = tar+https://unavailable.exherbolinux.org/{tar}',
                'importance = -100'
            ]
            pass

        return '\n'.join(configurations)

    pass
