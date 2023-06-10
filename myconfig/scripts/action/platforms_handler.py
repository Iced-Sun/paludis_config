from action.action_handler import Action_handler

class Platforms_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?platforms(.bash)?$'

    @property
    def configuration(self) -> str:
        return '*/*             amd64 ~amd64\n*/*[=scm]       ~amd64'
    pass
