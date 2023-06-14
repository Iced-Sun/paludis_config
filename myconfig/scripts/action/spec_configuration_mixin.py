import re

class Spec_configuration_mixin:
    @property
    def active_spec_configurations(self):
        if not hasattr(self, '_active_spec'):
            self._init_active_spec_configurations()
            pass
        return self._active_spec_configurations

    def _init_active_spec_configurations(self):
        self._active_spec_configurations = []

        for active_set_file in self.active_set_files:
            with active_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match('^\s*#.*$|^\s*$', line): continue

                    self._active_spec_configurations.append(self._parse_line_as_spec(line))
                    pass
                pass
            pass
        pass

    def _parse_line_as_spec(self, line: str):
        # parse the line
        m = re.match('^(?P<leading_tabs>\t+)?(?P<mark>[~@+-])?(?P<spec>\S+)(?P<config_tabs>\t+)?(?P<config>.+)?$', line)

        line_spec = {
            'spec': m.group('spec'),
            'mark': m.group('mark'),
            'type': 'package' if '/' in m.group('spec') else 'set',
            'is_dependecy': m.group('leading_tabs') is not None,
            'has_wildcard': True if '*' in m.group('spec') else False
        }

        # parse the configuration
        if m.group('config') is None:
            return line_spec

        if line_spec['mark'] == '@':
            return line_spec
        else:
            # the package options
            cm = re.match('^(?P<options>[^&]+)?(\s*)?(?P<suggestions>&.+)?$', m.group('config'))
            line_spec['options'] = cm.group('options')
            line_spec['suggestions'] = cm.group('suggestions')[1:] if cm.group('suggestions') is not None else None
            pass

        return line_spec

    ### end of Spec_configuration_mixin
    pass
