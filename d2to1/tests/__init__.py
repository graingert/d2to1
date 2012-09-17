from __future__ import with_statement

import os
import shutil
import subprocess
import sys
import tempfile

from .util import rmtree, open_config

# Determine the d2to1 development version from setup.cfg; note these tests are
# intended to be run from the source
with open_config(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                              'setup.cfg')) as cfg:
    D2TO1_VERSION = cfg.get('metadata', 'version')
del cfg


class D2to1TestCase(object):
    def setup(self):
        self.temp_dir = tempfile.mkdtemp(prefix='d2to1-test-')
        self.package_dir = os.path.join(self.temp_dir, 'testpackage')
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'testpackage'),
                        self.package_dir)
        self.oldcwd = os.getcwd()
        os.chdir(self.package_dir)
        with open(os.path.join(self.package_dir, 'd2to1_testpackage',
                               'version.py'), 'w') as f:
            f.write('D2TO1_VERSION = %r' % D2TO1_VERSION)

    def teardown(self):
        os.chdir(self.oldcwd)
        # Remove d2to1.testpackage from sys.modules so that it can be freshly
        # re-imported by the next test
        for k in list(sys.modules):
            if (k == 'd2to1_testpackage' or
                k.startswith('d2to1_testpackage.')):
                del sys.modules[k]
        rmtree(self.temp_dir)

    def run_setup(self, *args):
        return self._run_cmd(sys.executable, ('setup.py',) + args)

    def run_svn(self, *args):
        return self._run_cmd('svn', args)

    def _run_cmd(self, cmd, args):
        """
        Runs a command, with the given argument list, in the root of the test
        working copy--returns the stdout and stderr streams and the exit code
        from the subprocess.
        """

        os.chdir(self.package_dir)
        p = subprocess.Popen([cmd] + list(args), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        streams = tuple(s.decode('latin1').strip() for s in p.communicate())

        return (streams) + (p.returncode,)
