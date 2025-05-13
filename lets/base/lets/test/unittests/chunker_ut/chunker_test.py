"""
Chunker unit tests for the Chunker class from the parse module.
Created on 2016/10/31

"""

import unittest
import io
import sys

from test.unittests.testutil import CustomStringIO
from test.unittests.chunker_ut.input_test_data import *
from chunker import Chunker


EOL = "\n"


class TestChunker(unittest.TestCase):

    def test_creation_default(self):
        self.assertEqual('nl', Chunker().language)

    def test_creation_w_lang_ok(self):
        self.assertEqual('en', Chunker('en').language)

    def test_chnker_output_same_as_java_madagascar_en(self):
        chunker = Chunker('en')
        lem_file = io.StringIO(MADAGASCAR_EN_LEM_PART)
        pos_file = io.StringIO(MADAGASCAR_EN_POS_PART)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = MADAGASCAR_EN_CNK_PART_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        ok = True
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            try:
                self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))
            except AssertionError as err:
                print(err, file=sys.stderr)
                ok = False
        self.assertTrue(ok, "same_as_java_madagascar_en check FALED")

    def test_chnker_output_same_as_java_psainputcrosslang_en(self):
        chunker = Chunker('en')
        pos_file = io.StringIO(PSA_INPUT_CROSSLANG_EN_PART_POS)
        lem_file = io.StringIO(PSA_INPUT_CROSSLANG_EN_PART_LEM)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = PSA_INPUT_CROSSLANG_EN_PART_CNK_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))

    def test_chnker_output_same_as_java_jdnjaarinput_en(self):
        chunker = Chunker('en')
        pos_file = io.StringIO(JDN_JAAR_INPUT_EN_POS)
        lem_file = io.StringIO(JDN_JAAR_INPUT_EN_LEM)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = JDN_JAAR_INPUT_EN_CNK_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))

    def test_chnker_output_same_as_java_jdnjaarinput_du_de(self):
        chunker = Chunker('de')
        pos_file = io.StringIO(JDN_JAAR_INPUT_DU_POS_PART)
        lem_file = io.StringIO(JDN_JAAR_INPUT_DU_LEM_PART)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = JDN_JAAR_INPUT_DU_CNK_PART_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            try:
                self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))
            except AssertionError as err:
                print(err, file=sys.stderr)

    def test_chnker_output_same_as_java_riziv_nl(self):
        chunker = Chunker('nl')
        pos_file = io.StringIO(RIZIV_NL_POS_PART)
        lem_file = io.StringIO(RIZIV_NL_LEM_PART)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = RIZIV_NL_CNK_PART_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            try:
                self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))
            except AssertionError as err:
                print(err, file=sys.stderr)

    def test_chnker_output_same_as_java_riziv_nl_part2(self):
        chunker = Chunker('nl')
        pos_file = io.StringIO(RIZIV_NL_POS_PART2)
        lem_file = io.StringIO(RIZIV_NL_LEM_PART2)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = RIZIV_NL_CNK_PART2_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            try:
                self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))
            except AssertionError as err:
                print(err, file=sys.stderr)

    def test_chnker_output_same_as_java_riziv_nl_part3(self):
        chunker = Chunker('nl')
        pos_file = io.StringIO(RIZIV_NL_POS_PART3)
        lem_file = io.StringIO(RIZIV_NL_LEM_PART3)
        cnk_file = CustomStringIO()
        chunker.process_files(lem_file, pos_file, cnk_file)
        expected_sequence = RIZIV_NL_CNK_PART3_EXPECTED.split(EOL)
        actual_sequence = cnk_file.getvalue().split(EOL)
        for lno, (exp_line, true_line) in enumerate(zip(expected_sequence, actual_sequence)):
            exp_line = exp_line.replace("    ", "\t")   # Python IDEs replace tabs w/ spaces, need to reconstruct
            try:
                self.assertEqual(exp_line, true_line, "line {}: differ {!r} != {!r}".format(lno+1, exp_line, true_line))
            except AssertionError as err:
                print(err, file=sys.stderr)


if __name__ == '__main__':
    unittest.main()
