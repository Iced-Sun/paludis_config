class General_handler:
    @property
    def configuration(self) -> str:
        return 'world = ${root}/var/db/paludis/repositories/installed/world'

    pass

class Repository_handler:
    _repository_name: str

    def __init__(self, repository_name: str):
        self._repository_name = repository_name

    @property
    def configuration(self) -> str:
        match self._repository_name:
            case 'installed':
                return '''format = exndbam
location = ${root}/var/db/paludis/repositories/installed
name = installed
split_debug_location = /usr/${CHOST}/lib/debug
tool_prefix = ${CHOST}-
'''
            case _:
                return 'ttt'
                #raise new Exception('do not support the repo')
        pass

    pass
