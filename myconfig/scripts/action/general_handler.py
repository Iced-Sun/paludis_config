from action.action_handler import Action_handler

class General_handler(Action_handler):
    script_path_pattern = '^(/etc/paludis/)?general(.bash)?$'

    @property
    def configuration(self) -> str:
        return 'world = $root/var/db/paludis/repositories/installed/world'
    pass
