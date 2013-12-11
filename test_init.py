#!/usr/bin/env python
# pylint: disable-msg=R0904,C0103,W0201

""" Test the init subcommand """
from scripttest import TestFileEnvironment
import unittest, os

PPM = '../ppm'
TEST_ENV = './test-output'

class TestInit(unittest.TestCase):
    """ Test the init subcommand """

    def setUp(self):
        self.env = TestFileEnvironment(TEST_ENV)

    def test_creates_default(self):
        'it creates the virtualenv'
        out = self.env.run(PPM, 'init')
        self.assertIn('ppm_env', out.files_created)

    def test_creates_customenv(self):
        'it creates the virtualenv (--env set)'
        out = self.env.run(PPM, 'init', '--env', 'othername')
        self.assertIn('othername', out.files_created)

    def test_already_exists_default(self):
        'It fails when virtual environment already exists'
        self.env.run(PPM, 'init') # Create a virtual environment
        out = self.env.run(PPM, 'init', expect_error=True)
        self.assertNotEquals(out.returncode, 0)
        self.assertNotEquals(out.stderr, '')

    def test_already_exists_customenv(self):
        'It fails when the virtualenv already exists (--env set)'
        self.env.run(PPM, 'init', '--env', 'othername')
        out = self.env.run(PPM, 'init', '--env', 'othername', expect_error=True)
        self.assertNotEquals(out.returncode, 0)
        self.assertNotEquals(out.stderr, '')


REQUIREMENTS_TXT = """
# PYTHON=3
pep8==1.4.6
"""

FILE_PY = """
import pep8

print('Success!')
"""

class TestRun(unittest.TestCase):
    'Test the run subcommand'

    @classmethod
    def setUpClass(cls):
        cls.env = TestFileEnvironment(TEST_ENV)
        with open(os.path.join(TEST_ENV, 'file.py'), 'w') as file_py:
            file_py.write(FILE_PY)
        with open(os.path.join(TEST_ENV, 'requirements.txt'), 'w') as requirements_txt:
            requirements_txt.write(REQUIREMENTS_TXT)
        os.mkdir(os.path.join(TEST_ENV, 'subdir'))
        with open(os.path.join(TEST_ENV, 'subdir', 'file.py'), 'w') as file_py:
            file_py.write(FILE_PY)
        cls.env.run(PPM, 'init')

    def test_file_runs(self):
        'It successfully runs a simple python script in the virtualenv'
        out = self.env.run(PPM, 'run', 'file.py')
        self.assertEquals(out.stdout, 'Success!\n')

    def test_run_subfolder(self):
        'It runs a file in a subdirectory'
        out = self.env.run(PPM, 'run', 'file.py',
                cwd=os.path.join(TEST_ENV, 'subdir'))
        self.assertEquals(out.stdout, 'Success!\n')


class TestShell(unittest.TestCase):
    'Test `ppm shell`'

    @classmethod
    def setUpClass(cls):
        # These tests can share a single virtualenv
        # They will not need to replace it every time
        # as the commands should be nondestructive
        cls.env = TestFileEnvironment(TEST_ENV)
        with open(os.path.join(TEST_ENV, 'requirements.txt'), 'w') as requirements_txt:
            requirements_txt.write(REQUIREMENTS_TXT)
        os.mkdir(os.path.join(TEST_ENV, 'subdir'))

        cls.env.run(PPM, 'init')

    def test_shell_launches(self):
        'It runs a shell'
        out = self.env.run(PPM, 'shell', stdin="import pep8\nprint('Success!')")
        self.assertEquals(out.stdout, 'Success!\n')

    def test_shell_subfolder(self):
        'It runs a shell in a subdirectory'
        out = self.env.run(PPM, 'shell',
                cwd=os.path.join(TEST_ENV, 'subdir'),
                stdin="import pep8\nprint('Success!')")
        self.assertEquals(out.stdout, 'Success!\n')

    def test_shell_nofile(self):
        'It does not run a file'
        out = self.env.run(PPM, 'shell', 'file.py', expect_error=True)
        self.assertNotEquals(out.returncode, 0)
        self.assertNotEquals(out.stderr, '')


if __name__ == '__main__':
    unittest.main()
