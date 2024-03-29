class Host_mixin:
    '''depends on Set_file_mixin'''
    @property
    def host(self) -> str:
        if not hasattr(self, '_host'):
            self._init_host()
            pass
        return self._host

    def _init_host(self):
        self._host = None

        import re
        for section in self.configured_set_files.values():
            for set_path in section:
                with set_path.open() as f:
                    for line in f.read().splitlines():
                        if re.match('^\s*#.*$|^\s*$', line): continue

                        m = re.match('^(?P<leading_tabs>\t+)?(?P<mark>[~@+-])?(?P<spec>\S+)(?P<configs_tabs>\t+)?(?P<config>.+)?$', line)
                        if m.group('mark') == '@':
                            em = re.match('^(?P<key>.+):\s+(?P<value>.+)$', m.group('config'))
                            if em.group('key') == 'CHOST' and m.group('spec') == '*/*':
                                self._host = em.group('value')
                            pass
                        pass
                    pass
                pass
            pass

        ### end of host
        pass


    ### end of Host_mixin
    pass
