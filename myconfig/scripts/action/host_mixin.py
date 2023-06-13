import re

class Host_mixin:
    @property
    def host(self):
        for section in self._configured_set_paths.values():
            for set_path in section:
                with set_path.open() as f:
                    for line in f.read().splitlines():
                        if re.match('^\s*#.*$|^\s*$', line): continue

                        m = re.match('^(?P<leading_tabs>\t+)?(?P<mark>[~@+-])?(?P<spec>\S+)(?P<configs_tabs>\t+)?(?P<config>.+)?$', line)
                        if m.group('mark') == '@':
                            em = re.match('^(?P<key>.+):\s+(?P<value>.+)$', m.group('config'))
                            if em.group('key') == 'CHOST' and m.group('spec') == '*/*':
                                return em.group('value')
                            pass
                        pass
                    pass
                pass
            pass

        ### end of host
        pass

    ### end of Host_mixin
    pass
