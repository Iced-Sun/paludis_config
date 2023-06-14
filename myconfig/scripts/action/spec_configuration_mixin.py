import re

class Spec_configuration_mixin:
    '''depends on Destination_mixin, Set_files_mixin'''
    @property
    def active_spec_configurations(self):
        if not hasattr(self, '_active_spec_configurations'):
            self._init_active_spec_configurations()
            pass
        return self._active_spec_configurations

    @property
    def spec_environment(self):
        if not hasattr(self, '_spec_environment'):
            self._init_active_spec_configurations()
            pass
        return self._spec_environment

    def _init_active_spec_configurations(self):
        self._active_spec_configurations = []
        self._spec_environment = {}

        # if the destination is cross-compile target, only the matched set is
        # considered active
        if self.destination != 'installed':
            for active_set_file in self.active_set_files:
                if not active_set_file.stem.endswith(self.destination):
                    continue

                with active_set_file.open() as f:
                    for line in f.read().splitlines():
                        # skip a comment or blank line
                        if re.match('^\s*#.*$|^\s*$', line): continue

                        line_spec = self._parse_line_as_spec(line)
                        if line_spec['mark'] == '@':
                            self._add_to_spec_environment(line_spec)
                            pass
                        else:
                            self._active_spec_configurations.append(line_spec)
                            pass
                        pass
                    pass
                continue
            return

        # push active spec from active set
        for active_set_file in self.active_set_files:
            # skip any set matches to a specific target
            if len([target for target in self.configured_targets if active_set_file.stem.endswith(target)]) > 0:
                continue

            with active_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match('^\s*#.*$|^\s*$', line): continue

                    line_spec = self._parse_line_as_spec(line)
                    if line_spec['mark'] == '@':
                        self._add_to_spec_environment(line_spec)
                        pass
                    else:
                        self._active_spec_configurations.append(line_spec)
                        pass
                    pass
                pass
            pass

        # push active spec from weak set as dependecy
        for weak_set_file in self.configured_set_files['weak-set']:
            with weak_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match('^\s*#.*$|^\s*$', line): continue

                    line_spec = self._parse_line_as_spec(line)
                    line_spec['is_dependecy'] = True

                    if line_spec['mark'] == '@':
                        self._add_to_spec_environment(line_spec)
                        pass
                    else:
                        self._active_spec_configurations.append(line_spec)
                        pass
                    pass
                pass
            pass

        return

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
            line_spec['config'] = m.group('config')
            return line_spec
        else:
            # the package options
            cm = re.match('^(?P<options>[^&]+)?(\s*)?(?P<suggestions>&.+)?$', m.group('config'))
            line_spec['options'] = cm.group('options')
            line_spec['suggestions'] = cm.group('suggestions')[1:] if cm.group('suggestions') is not None else None
            pass

        return line_spec

    def _add_to_spec_environment(self, line_spec):
        # the build options: they are in fact environment variables
        m = re.match('^(?P<key>.+):\s+(?P<value>.+)$', line_spec['config'])
        if m is None:
            return

        if m.group('key') not in self._spec_environment:
            self._spec_environment[m.group('key')] = []
            pass

        self._spec_environment[m.group('key')].append({
            'spec': line_spec['spec'],
            'value': m.group('value')
        })
        return

    ### end of Spec_configuration_mixin
    pass
