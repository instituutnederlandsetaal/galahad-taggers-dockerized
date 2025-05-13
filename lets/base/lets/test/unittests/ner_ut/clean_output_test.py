"""
Unit tests for the ner_steps.clean_output package.
Created on 2016/11/18.

"""

import unittest
from io import StringIO

from test.unittests.testutil import CustomStringIO
from ner_steps.clean_output import CleanOutputOld


class TestCleanOutputOld(unittest.TestCase):

    TEST_DATA = (
        ("space    NN    0    1    0    1    0    0    0    0    0    0    0    0    5    spa    ace    spac    pace    allLowercase    0    O/0.999449", "space O 0.999449"),
        ("is    VBZ    0    1    0    1    0    0    0    0    0    0    0    0    2    is    is    is    is    allLowercase    0    O/0.999969", "is O 0.999969"),
        ("that    DT    0    1    0    1    0    0    0    0    0    0    0    0    4    tha    hat    that    that    allLowercase    0    O/0.999997", "that O 0.999997"),
        ("fierce    NN    0    1    0    1    0    0    0    0    0    0    0    0    6    fie    rce    fier    erce    allLowercase    0    O/0.999962", "fierce O 0.999962"),
        (".    .    0    1    0    1    0    0    0    1    1    0    0    0    1    .    .    .    .    onlyPunct    0    O/0.999965", ". O 0.999965"),
        ("",""),
        ("# 0.999089", None),  # a sentence probability line; should be skipped
        ("The    DT    1    0    0    0    0    0    0    0    0    0    0    0    3    The    The    The    The    firstCap    1    O/0.999568", "The O 0.999568"),
        ("female    NN    0    1    0    1    0    0    0    0    0    0    0    0    6    fem    ale    fema    male    allLowercase    0    O/0.999841", "female O 0.999841"),
        ("gives    VBZ    0    1    0    1    0    0    0    0    0    0    0    0    5    giv    ves    give    ives    allLowercase    0    O/0.999984", "gives O 0.999984"),
        ("up    RP    0    1    0    1    0    0    0    0    0    0    0    0    2    up    up    up    up    allLowercase    0    O/0.999933", "up O 0.999933"),
        (",    ,    0    1    0    1    0    0    0    1    1    0    0    0    1    ,    ,    ,    ,    onlyPunct    0    O/0.999993", ", O 0.999993"),
        ("and    CC    0    1    0    1    0    0    0    0    0    0    0    0    3    and    and    and    and    allLowercase    0    O/0.999990", "and O 0.999990"),
        ("leaves    NNS    0    1    0    1    0    0    0    0    0    0    0    0    6    lea    ves    leav    aves    allLowercase    0    O/0.999829", "leaves O 0.999829"),
        (".    .    0    1    0    1    0    0    0    1    1    0    0    0    1    .    .    .    .    onlyPunct    0    O/0.999947", ". O 0.999947"),
        ("",""),
    )

    def test__clean(self):
        in_iter = (item[0].replace("    ", "\t") for item in self.TEST_DATA)
        out_file = CustomStringIO()
        CleanOutputOld._clean(in_iter, out_file)
        exp_iter = (item[1] for item in self.TEST_DATA if item[1] is not None)
        out_iter = (line.rstrip() for line in StringIO(out_file.getvalue()))
        count = 0
        for exp_line, actual_line in zip(exp_iter, out_iter):
            self.assertEqual(exp_line, actual_line,
                             "line #{} differ:\n  expected: {}\n  but was:  {}" \
                             .format(count + 1, exp_line, actual_line))
            count += 1
        skipped = sum(int(item[1] is None) for item in self.TEST_DATA)
        self.assertEqual(len(self.TEST_DATA) - skipped, count)


if __name__ == '__main__':
    unittest.main()
