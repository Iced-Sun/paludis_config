import re

class Platforms_handler:
    script_path_pattern = re.compile('^(/etc/paludis/)?platforms(.bash)?$')

    def __init__(self, script_path):
        pass

    @property
    def configuration(self) -> str:
        return '*/*             amd64 ~amd64\n*/*[=scm]       ~amd64'
    pass
