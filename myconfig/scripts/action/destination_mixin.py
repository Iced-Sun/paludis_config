import os, re
from pathlib import Path
from subprocess import run

class Destination_mixin:
    @property
    def destination(self) -> str:
        if not hasattr(self, '_destination'):
            self._init_destination()
            pass
        return self._destination

    def _init_destination(self):
        self._destination = None

        ## self-invoke doesn't require the destination
        if '_SELF_INVOKE' in os.environ:
            return

        ## we have find a destination
        if 'CAVE_PERFORM_CMDLINE_destination' in os.environ:
            self._destination = os.environ['CAVE_PERFORM_CMDLINE_destination']
            pass
        else:
            destination_file_path = Path(f'/tmp/cave.{os.getppid()}')
            if destination_file_path.exists():
                with destination_file_path.open() as f:
                    self._destination = f.read()
                    pass
                pass
            else:
                if '_SELF_INVOKE' not in os.environ:
                    os.environ['_SELF_INVOKE'] = 'true'
                    p = run([
                        os.environ['CAVE'],
                        *os.environ['CAVE_CMDLINE_PARAMS'].split(),
                        '-0',
                        '*/*',
                        '--dump',
                        '--show-option-descriptions',
                        'none',
                        '--show-descriptions',
                        'none',
                        '--abort-at-phase',
                        'pretend'
                    ], capture_output = True, encoding = 'utf8')
                    if p.stdout is not None:
                        m = re.search('^.*true destination: Destination\((?P<destination>\S+) .*$', p.stdout, re.MULTILINE)
                        if m is not None:
                            self._destination = m.group('destination')
                            with Path(f'/tmp/cave.{os.getppid()}').open('w') as f:
                                f.write(self._destination)
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass

    ### end of Destination_mixin
    pass
