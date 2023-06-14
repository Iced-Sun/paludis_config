import os

class Destination_mixin:
    '''depends on Target_mixin'''
    @property
    def destination(self) -> str:
        if not hasattr(self, '_destination'):
            self._init_destination()
            pass
        return self._destination

    def _init_destination(self):
        self._destination = 'installed'

        ## not in cave environment
        if 'CAVE' not in os.environ:
            return

        ## find a destination
        if 'CAVE_PERFORM_CMDLINE_destination' in os.environ:
            self._destination = os.environ['CAVE_PERFORM_CMDLINE_destination']
            pass
        else:
            ## parse CAVE_CMDLINE_PARAMS to infer the destination
            params = ' '.join(os.environ['CAVE_CMDLINE_PARAMS'].split())
            if '-mx' in params or '-m x' in params or '--make cross-compile' in params:
                import re
                m = re.match('.*(-4|--cross-host) (?P<cross_host>[-\w]+).*', params)
                if m is not None:
                    self._destination = m.group('cross_host')
                    pass
                else:
                    if len(self.configured_targets) == 1:
                        self._destination = self.configured_targets[0]
                        pass
                    pass
                pass
            pass
        pass

    ### end of Destination_mixin
    pass
