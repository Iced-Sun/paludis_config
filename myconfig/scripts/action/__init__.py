import re

class Action_handler:
    def __init__(self, script_path: str):
        self._suffix = script_path.suffix
        self._action = str(script_path).split('/')[0]
        self._sub_action = '' if script_path.stem == self._action else script_path.stem
        pass

    pass

class General_handler(Action_handler):
    script_path_pattern = re.compile('^general(.bash)?$')

    def __init__(self, script_path):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        return 'world = ${root}/var/db/paludis/repositories/installed/world'

    pass

class Repository_handler(Action_handler):
    script_path_pattern = re.compile('^repositories/(.+)(.bash)?$')

    def __init__(self, script_path: str):
        super().__init__(script_path)
        pass

    @property
    def configuration(self) -> str:
        match self._sub_action:
            case 'installed':
                return '''format = exndbam
location = ${root}/var/db/paludis/repositories/installed
name = installed
split_debug_location = /usr/${CHOST}/lib/debug
tool_prefix = ${CHOST}-
'''
            case _:
                raise Exception('do not support the repository {}'.format(self._sub_action))
        pass

    pass
