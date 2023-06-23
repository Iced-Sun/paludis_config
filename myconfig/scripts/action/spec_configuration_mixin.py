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

        # push active spec from active set
        for active_set_file in self.active_set_files:
            targetSets = [
                target
                for target in self.configured_targets
                if active_set_file.stem.endswith(target)
            ]
            setTarget = targetSets[0] if len(targetSets) == 1 else None

            with active_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match('^\s*#.*$|^\s*$', line): continue

                    line_spec = self._parse_line_as_spec(line)
                    #if line_spec['mark'] == '@':
                    #    self._add_to_spec_environment(line_spec)
                    #    pass
                    #else:
                    #    self._active_spec_configurations.append(line_spec)
                    #    pass
                    if self.destination != 'installed': # cross compiling
                        # parse only the destination-named set
                        if setTarget == self.destination:
                            if line_spec['mark'] == '@':
                                self._add_to_spec_environment(line_spec, setTarget)
                                pass
                            else:
                                self._active_spec_configurations.append(line_spec)
                                pass
                            pass
                        pass
                    else: # native compiling
                        if setTarget is None: # a regular set
                            if line_spec['mark'] == '@':
                                self._add_to_spec_environment(line_spec)
                                pass
                            else:
                                self._active_spec_configurations.append(line_spec)
                                pass
                            pass
                        else: # a target set
                            if line_spec['mark'] == '@' and line_spec['spec'] == '*/*' and (
                                line_spec['config'].startswith('CHOST')
                                or line_spec['config'].startswith('CFLAGS')
                                or line_spec['config'].startswith('CXXFLAGS')
                                or line_spec['config'].startswith('LDFLAGS')
                            ):
                                self._add_to_spec_environment(line_spec, setTarget)
                            pass
                        pass

                    continue
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

                    if self.destination != 'installed': # cross compiling
                        if line_spec['mark'] == '@' and line_spec['spec'] == '*/*' and (
                                line_spec['config'].startswith('CHOST')
                                or line_spec['config'].startswith('CFLAGS')
                                or line_spec['config'].startswith('CXXFLAGS')
                                or line_spec['config'].startswith('LDFLAGS')
                        ):
                            self._add_to_spec_environment(line_spec)
                            pass
                        pass
                    else:
                        if line_spec['mark'] == '@':
                            self._add_to_spec_environment(line_spec)
                            pass
                        else:
                            self._active_spec_configurations.append(line_spec)
                            pass
                        pass

                    #if line_spec['mark'] == '@':
                    #    self._add_to_spec_environment(line_spec)
                    #    pass
                    #else:
                    #    self._active_spec_configurations.append(line_spec)
                    #    pass
                    continue
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

    def _add_to_spec_environment(self, line_spec, target=None):
        # the build options: they are in fact environment variables
        m = re.match('^(?P<key>.+):\s+(?P<value>.+)$', line_spec['config'])
        if m is None:
            return

        key = m.group('key')
        if key in ['CHOST', 'CFLAGS', 'CXXFLAGS', 'LDFLAGS']:
            key = key if target is None else f'{target.replace("-", "_")}_{key}'
            pass

        if key not in self._spec_environment:
            self._spec_environment[key] = []
            pass

        self._spec_environment[key].append({
            'spec': line_spec['spec'],
            'value': m.group('value')
        })
        return

    ### end of Spec_configuration_mixin
    pass
