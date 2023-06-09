import re

class General_handler:
    script_path_pattern = re.compile('^(/etc/paludis/)?general(.bash)?$')

    def __init__(self, script_path):
        pass

    @property
    def configuration(self) -> str:
        return 'world = $root/var/db/paludis/repositories/installed/world'
    pass
