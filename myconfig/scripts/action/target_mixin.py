import re

class Target_mixin:
    '''depends on Set_files_mixin'''
    @property
    def configured_targets(self):
        if not hasattr(self, '_configured_targets'):
            self._init_configured_targets()
            pass
        return self._configured_targets

    def _init_configured_targets(self):
        self._configured_targets = []

        for section in self.configured_set_files.values():
            for set_path in section:
                m = re.match(r'\d{2}-(?P<target_triple>\w+-\w+-\w+-\w+)', set_path.stem)
                if m is not None:
                    self._configured_targets.append(m.group('target_triple'))
                    pass
                continue
            continue

        return

    ### end of Target_mixin
    pass
