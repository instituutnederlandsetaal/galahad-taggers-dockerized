"""
Unit tests for the ner_steps.feat_vect package.
Created on 2016/11/18.

"""

import unittest
from io import StringIO

from ner_steps import PARSE_DELIM
from ner_steps.feat_vect import FeatVectProcessor


class TestFeatVectProcessor(unittest.TestCase):

    def test_creation_default(self):
        FeatVectProcessor()

    def test_creation_w_language(self):
        fvproc = FeatVectProcessor('en')
        self.assertEqual('en', fvproc.language)

    TEST_DATA = (
        # (source_line, isfirst, result)
        ('Agreement NNP 0.888591', True, ['Agreement NNP 1 0 0 0 0 0 0 0 0 0 0 0 9 Agr ent Agre ment firstCap 1']),
        ('without IN 0.999275', False, ['without IN 0 1 0 1 0 0 0 0 0 0 0 0 7 wit out with hout allLowercase 0']),
        ('any DT 0.996723', False, ['any DT 0 1 0 1 0 0 0 0 0 0 0 0 3 any any any any allLowercase 0']),
    )

    def test__split_line(self):
        fvproc = FeatVectProcessor('en')
        self.assertEqual(('1', 'Agreement', 'NNP'), fvproc._split_line("1\tAgreement NNP 0.888591"))
        self.assertEqual(('0', 'without', 'IN'), fvproc._split_line("0\twithout IN 0.999275"))
        self.assertEqual(('0', 'any', 'DT'), fvproc._split_line("0\tany DT 0.996723"))

    def test__split_line_on_error(self):
        fvproc = FeatVectProcessor('en')
        expected = (None, None, r"!!ERROR: cannot process line '1\tSomeGarbage': not enough values to unpack (expected at least 2, got 1)")
        errfile = StringIO()
        self.assertEqual(expected, fvproc._split_line("1\tSomeGarbage", errfile=errfile))
        expected = "FeatVectProcessor: cannot process line '1\\tSomeGarbage': not enough values to unpack (expected at least 2, got 1)\n"
        self.assertEqual(expected, errfile.getvalue())

    def test_process_item(self):
        fvproc = FeatVectProcessor('en')
        for source_line, isfirst, result in self.TEST_DATA:
            line = "{}{}{}".format(int(isfirst), PARSE_DELIM, source_line)
            self.assertEqual(result, [elm for elm in fvproc.process_line(line)])

    def test_process(self):
        fvproc = FeatVectProcessor('en')
        expected = [rec[2][0] for rec in self.TEST_DATA] + [""]
        #line_iter = (rec[0] for rec in self.TEST_DATA)
        line_iter = list()
        for rec in self.TEST_DATA:
            line_iter.append(rec[0])
        result = [elm for elm in fvproc.process_lines(line_iter)]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
