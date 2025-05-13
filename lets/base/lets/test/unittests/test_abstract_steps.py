"""
Unit tests for the preporcessor abstract steps.
Created on 2016/11/12

"""

import unittest
import io

from abstract_step import DualInputStep


SAMPLE_LINES_ONE = (
    'lines_one_1',
    'lines_one_2',
    'lines_one_3',
)

SAMPLE_LINES_TWO = (
    'lines_two_1',
    'lines_two_2',
    'lines_two_3',
)

EXPECTED = ['lines_one_1#lines_two_1', 'lines_one_2#lines_two_2', 'lines_one_3#lines_two_3', '#']


class SampleDualInputStep(DualInputStep):

    def process_dual_line(self, line_one, line_two):
        return ["#".join((line_one.rstrip(), line_two.rstrip()))]


class TestDualInputStep(unittest.TestCase):

    def test_creation_default(self):
        step = SampleDualInputStep()
        self.assertEqual('nl', step.language)

    def test_creation_w_language(self):
        step = SampleDualInputStep('en')
        self.assertEqual('en', step.language)

    def test_process_dual_lines(self):
        step = SampleDualInputStep()
        result_list = list(step.process_dual_lines(SAMPLE_LINES_ONE, SAMPLE_LINES_TWO))
        self.assertEqual(EXPECTED, result_list)

    def test_process_files(self):
        f_in_one = io.StringIO("\n".join(SAMPLE_LINES_ONE))
        f_in_two = io.StringIO("\n".join(SAMPLE_LINES_TWO))
        f_out = io.StringIO()
        step = SampleDualInputStep()
        step.process_files(f_in_one, f_in_two, f_out)
        expected = "\n".join(EXPECTED) + "\n"
        result = f_out.getvalue()
        self.assertEqual(expected, result)

    # TODO: provide automated testing of process_files_by_name() and main()


if __name__ == '__main__':
    unittest.main()
