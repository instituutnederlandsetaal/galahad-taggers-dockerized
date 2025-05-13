"""
Unit tests for the cmdline helper class.
"""

import unittest
import subprocess


from ner_steps.cmdline import CommandLineHelper


class TestCommandLineHelper(unittest.TestCase):

    def test_creation_default(self):
        CommandLineHelper()

    def test_creation_command_line_tokens(self):
        cmd = CommandLineHelper(['echo', 'ALPHA-01'])
        self.assertEqual(['echo', 'ALPHA-01'], cmd.get_all_tokens())

    def test_add_args_case1(self):
        cmd = CommandLineHelper(['echo', 'ALPHA-02'])
        cmd.add_args(['BRAVO-02', 'CHARLIE-02'])
        self.assertEqual(['echo', 'ALPHA-02', 'BRAVO-02', 'CHARLIE-02'], cmd.get_all_tokens())

    def test_add_args_case2(self):
        cmdline = CommandLineHelper(['zfs', 'list'])
        cmdline.add_args(['-t', 'snapshot'])
        self.assertEqual(['zfs', 'list', '-t', 'snapshot'], cmdline.get_all_tokens())

    def test_add_args_with_before(self):
        cmdline = CommandLineHelper(['zfs', 'list'])
        cmdline.add_args(['-t', 'snapshot'], before='list')
        self.assertEqual(['zfs', '-t', 'snapshot', 'list'], cmdline.get_all_tokens())

    def test_missing_before_raises_value_erorr(self):
        cmdline = CommandLineHelper(['zfs', 'list'])
        self.assertRaisesRegex(ValueError, 'is not in list', cmdline.add_args, ['-t', 'snapshot'], before='list2')

    def test_execute_simple_case_returncode_zero_and_stdout(self):
        cmdline = CommandLineHelper(['echo', 'ALPHA-BRAVO'])
        cmdline.execute()
        self.assertEqual(0, cmdline.returncode())
        self.assertEqual('ALPHA-BRAVO\n', cmdline.stdout())
        self.assertEqual("", cmdline.stderr())

    def __test_execute_simple_case_returncode_zero_and_stderr(self):
        cmdline = CommandLineHelper(['echo', '--bad-switch'])
        cmdline.execute()
        self.assertEqual(0, cmdline.returncode())
        self.assertEqual("", cmdline.stdout())
        self.assertEqual('ALPHA-BRAVO\n', cmdline.stdout())

    def test_execute_simple_case_returncode_nonzero(self):
        cmdline = CommandLineHelper(['/bin/false'])
        cmdline.execute()
        self.assertNotEqual(0, cmdline.returncode())

    def test_command_times_out(self):
        cmdline = CommandLineHelper(['sleep', '10'])
        self.assertRaises(subprocess.TimeoutExpired, cmdline.execute, timeout=0.5)

    def test_command_doesnt_times_out(self):
        cmdline = CommandLineHelper(['sleep', '0.5'])
        cmdline.execute(timeout=2)
    
    def test_command_with_shell(self):
        cmdline = CommandLineHelper(['ls', '-lah', '|', 'grep', 'total'])
        cmdline.execute(shell=True)
        self.assertTrue("total" in cmdline.stdout())


if __name__ == '__main__':
    unittest.main()
