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

        ## order matters
        # push active spec from weak set as dependecy
        for weak_set_file in self.configured_set_files['weak-set']:
            self._active_spec_configurations.append({'type': 'comment', 'comment': f'# {weak_set_file.name}'})
            with weak_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match(r'^\s*#.*$|^\s*$', line): continue

                    # parse the configuration line, generate the intermediate
                    # spec for later generation
                    self._pickup_spec(self._parse_line_as_spec(line, { 'is_dependecy': True }))

                    continue
                pass
            pass

        # push active spec from active set, except the machine set
        for active_set_file in self.active_set_files:
            # the machine set will be parsed at last
            if active_set_file.name.startswith('@'): continue

            targetSets = [
                target
                for target in self.configured_targets
                if active_set_file.stem.endswith(target)
            ]
            setTarget = targetSets[0] if len(targetSets) == 1 else None

            self._active_spec_configurations.append({'type': 'comment', 'comment': f'# {active_set_file.name}'})
            with active_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match(r'^\s*#.*$|^\s*$', line): continue

                    # parse the configuration line, generate the intermediate
                    # spec for later generation
                    self._pickup_spec(self._parse_line_as_spec(line), setTarget)

                    continue
                pass
            continue

        # push activated feature set
        for feature_set_file in self.configured_set_files['feature-set']:
            self._active_spec_configurations.append({'type': 'comment', 'comment': f'# {feature_set_file.name}'})
            with feature_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match(r'^\s*#.*$|^\s*$', line): continue

                    # parse the configuration line, generate the intermediate
                    # spec for later generation
                    self._pickup_spec(self._parse_line_as_spec(line, { 'is_dependecy': True }))

                    continue
                pass
            continue

        # push machine set
        for machine_set_file in self.active_set_files:
            if not machine_set_file.name.startswith('@'): continue

            self._active_spec_configurations.append({'type': 'comment', 'comment': f'# {machine_set_file.name}'})
            with machine_set_file.open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match(r'^\s*#.*$|^\s*$', line): continue

                    # parse the configuration line, generate the intermediate
                    # spec for later generation
                    self._pickup_spec(self._parse_line_as_spec(line))

                    continue
                pass
            continue

        return

    def _pickup_spec(self, line_spec, target=None):
        is_env_general_and_buildflags = (
            line_spec['mark'] == '@'
            and line_spec['spec'] == '*/*'
            and line_spec['config'].startswith(('CHOST', 'CFLAGS', 'CXXFLAGS', 'LDFLAGS'))
        )

        # cross compiling
        if self.destination != 'installed':
            if is_env_general_and_buildflags:
                self._add_to_spec_environment(line_spec)
                pass

            # pick up only destination matching the target
            if target == self.destination:
                if line_spec['mark'] == '@':
                    self._add_to_spec_environment(line_spec, target)
                    pass
                else:
                    self._active_spec_configurations.append(line_spec)
                    pass
                pass

            pass
        # native compiling
        else:
            # toolchain
            if target:
                if is_env_general_and_buildflags:
                    self._add_to_spec_environment(line_spec, target)
                    pass
                pass
            # host packages
            else:
                if line_spec['mark'] == '@':
                    self._add_to_spec_environment(line_spec)
                    pass
                else:
                    self._active_spec_configurations.append(line_spec)
                    pass
                pass
            pass
        return

    def _parse_line_as_spec(self, line: str, advice={}):
        # parse the line
        m = re.match(r'^(?P<leading_tabs>\t+)?(?P<mark>[~@+-])?(?P<spec>\S+)(?P<config_tabs>\t+)?(?P<config>.+)?$', line)

        line_spec = {
            'spec': m.group('spec'),
            'mark': m.group('mark'),
            'type': 'package' if '/' in m.group('spec') else 'set',
            'is_dependecy': m.group('leading_tabs') is not None,
            'has_wildcard': True if '*' in m.group('spec') else False,
            **advice
        }

        # parse the configuration
        if m.group('config') is None:
            return line_spec

        if line_spec['mark'] == '@':
            line_spec['config'] = m.group('config')
            return line_spec
        else:
            # the package options
            cm = re.match(r'^(?P<options>[^&]+)?(\s*)?(?P<suggestions>&.+)?$', m.group('config'))
            line_spec['options'] = cm.group('options')
            line_spec['suggestions'] = cm.group('suggestions')[1:] if cm.group('suggestions') is not None else None
            pass

        return line_spec

    def _add_to_spec_environment(self, line_spec, target=None):
        # the build options: they are in fact environment variables
        m = re.match(r'^(?P<key>.+):\s+(?P<value>.+)$', line_spec['config'])
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
