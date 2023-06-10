from pathlib import Path
import os, re

class Action_handler:
    @classmethod
    def match(cls, script_path, action):
        if re.match(cls.script_path_pattern, str(script_path)) is not None:
            return True

        if action is not None and re.match(cls.script_path_pattern, action) is not None:
            return True

        return False

    def __init__(self, script_path: Path):
        ## configure the environment
        # paths and files
        self._paludis_config_dir = os.environ['PALUDIS_CONFIG_DIR'] if 'PALUDIS_CONFIG_DIR' in os.environ else '/etc/paludis'
        self._wrapper_path = script_path.resolve()
        self._config_path = self._wrapper_path.parents[1]
        self._set_path = self._config_path / 'sets'

        # hard-coded, should be consistent with the value in
        # repositories/installed.conf
        self._world_file = '/var/db/paludis/repositories/installed/world'

        # installed specs
        # TODO what is -cross-installed in world file looks like
        with Path(self._world_file).open() as f:
            self._installed_spec = [{
                'name': line,
                'type': 'package' if '/' in line else 'set'
            } for line in f.read().splitlines()]
            pass

        ## induce the action
        if script_path.is_absolute():
            script_path = script_path.relative_to(self._paludis_config_dir)
            pass

        script_path_parts = script_path.parts

        self._action = Path(script_path_parts[0]).stem
        self._sub_action = Path(script_path_parts[1]).stem if len(script_path_parts) == 2 else None

        ## record the set names
        self._machine_sets = sorted(self._set_path.glob('@*'))

        self._general_sets = sorted(self._set_path.glob('[0-9][0-9]-*'))
        self._weak_sets = [{
            'name': re.match('^\?(\d{2}-)?(?P<name>.*)$', path.name).group('name'),
            'path': path,
            'type': 'weak-set'
        } for path in self._set_path.glob('[?]*')]

        ## the active set has detailed set spec
        self._active_sets = []
        self._generate_active_sets()

        ## parse each line in relevant sets
        self._spec_config = []
        self._spec_environ = {}
        self._parse_weak_sets()
        self._parse_active_sets()

        ## finally, find out how many targets we should support
        self._CHOST = next(v[0]['value'] for k, v in self._spec_environ.items() if k == 'CHOST')
        self._TARGETS = [self._CHOST]
        self._parse_build_targets()
        pass

    def _generate_active_sets(self):
        ## find the active sets
        # 1. match against the world file
        for installed in self._installed_spec:
            # we don't care packages in the world file
            if installed['type'] != 'set':
                continue

            # uuid introduces a machine set
            if re.match('[0-9a-f]{32}', installed['name']):
                # fetch the real machine-id
                machine_id = None

                with Path('/etc/machine-id').open() as f:
                    machine_id = f.read().splitlines()[0]
                    pass

                # check if the machine-id matches system setting
                if installed['name'] == machine_id:
                    self._active_sets += [{
                        'name': installed['name'],
                        # use next() to find exactly one set
                        'path': next(s for s in self._machine_sets if s.match(f'*@{machine_id}:*')),
                        'type': 'machine-set',
                        'pulled_by': 'world'
                    }]
                    pass
                pass
            # match a general set
            else:
                self._active_sets += [{
                    'name': installed['name'],
                    # use next() to find exactly one general set
                    'path': next(s for s in self._general_sets if s.match(f'*/[0-9][0-9]-{installed["name"]}')),
                    'type': 'general-set',
                    'pulled_by': 'world'
                }]
                pass
            pass

        # 2. pull dependecy sets by a non-package spec from seen active sets
        sets = []
        # gather dependent sets
        for s in self._active_sets:
            # only world sets can pull inclusion
            if s['pulled_by'] != 'world':
                continue

            with s['path'].open() as f:
                for line in f.read().splitlines():
                    set_inclusion_match = re.match('^([-a-zA-Z0-9]+)(\t+.+)?$', line)
                    if set_inclusion_match:
                        sets.append(set_inclusion_match.group(1))
                        pass
                    pass
                pass

            pass

        # insert the dependecy sets
        for s in sets:
            if next((_ for _ in self._active_sets if _['name'] == s), None) is not None:
                continue

            self._active_sets += [{
                'name': s,
                # use next() to find exactly one general set
                'path': next(_ for _ in self._general_sets if _.match(f'*/[0-9][0-9]-{s}')),
                'type': 'general-set',
                'pulled_by': 'inclusion'
            }]
            pass

        # end of self._generate_active_sets()
        pass

    def _parse_line_spec(self, line: str, context_set_type: str):
        # split the line to parts
        m = re.match('^(?P<leading_tabs>\t+)?(?P<mark>[~@+-])?(?P<spec>\S+)(?P<options_tabs>\t+)?(?P<config>.+)?$', line)

        line_spec = {
            'spec': m.group('spec'),
            'mark': m.group('mark'),
            'type': 'package' if '/' in m.group('spec') else 'set',
            'is_dependecy': m.group('leading_tabs') is not None or context_set_type == 'weak-set',
            'has_wildcard': True if '*' in m.group('spec') else False,
            'config': m.group('config')
        }

        # parse the options
        if line_spec['config'] is not None:
            if line_spec['mark'] == '@':
                # the build options: they are in fact environment variables
                em = re.match('^(?P<key>.+):\s+(?P<value>.+)$', line_spec['config'])
                if em.group('key') not in self._spec_environ:
                    self._spec_environ[em.group('key')] = []
                    pass

                self._spec_environ[em.group('key')].append({
                    'spec': line_spec['spec'],
                    'value': em.group('value')
                })
                pass
            else:
                # the package options
                om = re.match('^(?P<options>[^&]+)?(\s*)?(?P<suggestions>&.+)?$', line_spec['config'])
                line_spec['options'] = om.group('options')
                line_spec['suggestions'] = om.group('suggestions')[1:] if om.group('suggestions') is not None else None

                # insert to the spec config
                self._spec_config.append(line_spec)
                pass
            pass
        pass

    def _parse_weak_sets(self):
        for s in self._weak_sets:
            with s['path'].open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match('^\s*#.*$|^\s*$', line):
                        continue

                    # insert the spec
                    self._parse_line_spec(line, s['type'])
                    pass
                pass
            pass
        pass

    def _parse_active_sets(self):
        for s in self._active_sets:
            with s['path'].open() as f:
                for line in f.read().splitlines():
                    # skip a comment or blank line
                    if re.match('^\s*#.*$|^\s*$', line):
                        continue

                    # insert the spec
                    self._parse_line_spec(line, s['type'])
                    pass
                pass
            pass
        pass

    def _parse_build_targets(self):
        # for now, only 'targets' suboption is needed, hence the parsing is
        # done here
        #
        # if other suboption is needed, it should be parsed in _parse_line_spec
        for conf in self._spec_config:
            if conf['options'] is not None and 'TARGETS:' in conf['options']:
                targets = re.match('^.*TARGETS:\s+(?P<targets>.+)$', conf['options']).group('targets')
                for target in targets.split(' '):
                    if not target.startswith('-') and target not in self._TARGETS:
                        self._TARGETS.append(target)
                        pass
                    pass
                pass
            pass
        pass

    # end of class Action_handler
    pass
