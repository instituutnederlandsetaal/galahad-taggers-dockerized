"""
Ported from lt3_java/preprocessor_java/ChunkGenerator/src/domein Java package.
Created on 2016/10/31

"""

import unittest
import io

from chunker_steps.lem_parser import LEMParser
from chunker_steps.pos_parser import POSParser
from chunker_steps.pos_lem_joiner import POSLEMJoiner
from chunker_steps.pos_maps import *
from test.unittests.chunker_ut.input_test_data import MADAGASCAR_EN_POS_PART, MADAGASCAR_EN_LEM_PART
from test.unittests.testutil import spaces_to_tabs


LEM_SAMPLE_INPUT = """\
gender gender /
equality equality /
, , /
empowerment empowerment /
of of /
women woman 0.995159
and and /
intergenerational intergenerational /
equity equity /
, , /

Also also 0.996421
acknowledging acknowledge 0.988454
"""

POS_SAMPLE_INPUT = """\
gender NN 0.626069
equality NN 0.998706
, , 0.999920
empowerment NN 0.977016
of IN 0.999959
women NNS 0.997074
and CC 0.999887
intergenerational JJ 0.992280
equity NN 0.999885
, , 0.999644

Also RB 0.998660
acknowledging VBG 0.995488
"""


class TestLEMSeqParser(unittest.TestCase):

    def test_creation(self):
        LEMParser()
        LEMParser('en')

    def test_process_lines(self):
        input_iter = io.StringIO(LEM_SAMPLE_INPUT)
        lemproc = LEMParser('en')
        expected = [
            'gender /',
            'equality /',
            ', /',
            'empowerment /',
            'of /',
            'woman 0.995159',
            'and /',
            'intergenerational /',
            'equity /',
            ', /',
            "",
            'also 0.996421',
            'acknowledge 0.988454',
            "",
        ]
        result = list(lemproc.process_lines(input_iter))
        self.assertEqual(spaces_to_tabs(expected), result)

    def test_process_lines_w_madagascar_en(self):
        input_iter = io.StringIO(MADAGASCAR_EN_LEM_PART)
        lemparser = LEMParser('en')
        expected = [
            '60 /',
            'million /',
            'year 0.998357',
            'ago 0.996526',
            ', /',
            'on /',
            'the /',
            'shore 0.993417',
            'of /',
            'this /',
            'tropical /',
            'island /',
            ', /',
            'an /',
            'extraordinary /',
            'story /',
            'begin 0.777042',
            '. /',
            "",
            'the /',
            'wave 0.973181',
            'bring 0.799948',
            'ashore 0.997623',
            'an /',
            'odd /',
            'band /',
            'of /',
            'survivor 0.998137',
            '- /',
            'a /',
            'few /',
            'ancient /',
            'creature 0.998548',
            'that /',
            'have 0.848421',
            'be 0.809043',
            'accidentally 0.999873',
            'sweep 0.939658',
            'across /',
            'hundred 0.997541',
            'of /',
            'kilometre 0.996640',
            'of /',
            'ocean /',
            'from /',
            'a /',
            'distant /',
            'land /',
            '. /',
            "",
            "",
        ]
        result = list(lemparser.process_lines(input_iter))
        #print(expected)
        #print(result)
        self.assertEqual(spaces_to_tabs(expected), result)

class TestPOSInputProcessor(unittest.TestCase):

    def test_creation(self):
        POSParser()
        POSParser('en')

    def test_process_lines(self):
        input_iter = io.StringIO(POS_SAMPLE_INPUT)
        posproc = POSParser('en')
        expected = [
            'gender  NN N',
            'equality  NN N',
            ',  , PCT',
            'empowerment  NN N',
            'of  IN PREP',
            'women  NNS N',
            'and  CC CONJ-coord',
            'intergenerational  JJ ADJ',
            'equity  NN N',
            ',  , PCT',
            "",
            'Also  RB ADV',
            'acknowledging  VBG V-prpa',
            "",
        ]
        result = list(posproc.process_lines(input_iter))
        #print(result)
        self.assertEqual(spaces_to_tabs(expected), result)

#         import sys
#         print("\n" + repr(expected), file=sys.stderr)
#         print(result, file=sys.stderr)
#         for idx, (elem1, elem2) in enumerate(zip(expected, result)):
#             if elem1 != elem2:
#                 print(elem1, "!=", elem2, "at", idx)
#         self.assertEqual(len(expected), len(result))


    def test_process_lines_w_madagascar_en(self):
        input_iter = io.StringIO(MADAGASCAR_EN_POS_PART)
        posproc = POSParser('en')
        expected = [
            '60  CD NUM',
            'million  CD NUM',
            'years  NNS N',
            'ago  RB ADV',
            ',  , PCT',
            'on  IN PREP',
            'the  DT DET',
            'shores  NNS N',
            'of  IN PREP',
            'this  DT DET',
            'tropical  JJ ADJ',
            'island  NN N',
            ',  , PCT',
            'an  DT DET',
            'extraordinary  JJ ADJ',
            'story  NN N',
            'began  VBD V-fin',
            '.  . PCT',
            "", #'   PCT',
            'The  DT DET',
            'waves  NNS N',
            'brought  VBD V-fin',
            'ashore  RB ADV',
            'an  DT DET',
            'odd  JJ ADJ',
            'band  NN N',
            'of  IN PREP',
            'survivors  NNS N',
            '-  : PCT',
            'a  DT DET',
            'few  JJ ADJ',
            'ancient  JJ ADJ',
            'creatures  NNS N',
            'that  WDT PRON-rel',
            'had  VBD V-fin',
            'been  VBN V-papa',
            'accidentally  RB ADV',
            'swept  VBN V-papa',
            'across  IN PREP',
            'hundreds  NNS N',
            'of  IN PREP',
            'kilometres  NNS N',
            'of  IN PREP',
            'ocean  NN N',
            'from  IN PREP',
            'a  DT DET',
            'distant  JJ ADJ',
            'land  NN N',
            '.  . PCT',
            "", #'   PCT',
            "",
        ]
        result = list(posproc.process_lines(input_iter))
        self.assertEqual(spaces_to_tabs(expected), result)


class TestPOSLEMJoiner(unittest.TestCase):

    def test_creation(self):
        POSLEMJoiner()
        POSLEMJoiner('en')

    def test_process_dual_lines(self):
        language = 'en'
        lem_input = io.StringIO(LEM_SAMPLE_INPUT)
        pos_input = io.StringIO(POS_SAMPLE_INPUT)
        lemproc = LEMParser(language)
        posproc = POSParser(language)
        poslemproc = POSLEMJoiner(language)
        expected = [
            'gender gender NN N',
            'equality equality NN N',
            ', , , PCT',
            'empowerment empowerment NN N',
            'of of IN PREP',
            'women woman NNS N',
            'and and CC CONJ-coord',
            'intergenerational intergenerational JJ ADJ',
            'equity equity NN N',
            ', , , PCT',
            "",
            'Also also RB ADV',
            'acknowledging acknowledge VBG V-prpa',
            "",
            "",
        ]
        result = list(poslemproc.process_dual_lines(lemproc.process_lines(lem_input), posproc.process_lines(pos_input)))
        #print(result)
        self.assertEqual(spaces_to_tabs(expected), result)

    def test_process_dual_lines_w_madagascar_en(self):
        language = 'en'
        lem_input = io.StringIO(MADAGASCAR_EN_LEM_PART)
        pos_input = io.StringIO(MADAGASCAR_EN_POS_PART)
        lemproc = LEMParser(language)
        posproc = POSParser(language)
        poslemproc = POSLEMJoiner(language)
        expected = [
            '60 60 CD NUM',
            'million million CD NUM',
            'years year NNS N',
            'ago ago RB ADV',
            ', , , PCT',
            'on on IN PREP',
            'the the DT DET',
            'shores shore NNS N',
            'of of IN PREP',
            'this this DT DET',
            'tropical tropical JJ ADJ',
            'island island NN N',
            ', , , PCT',
            'an an DT DET',
            'extraordinary extraordinary JJ ADJ',
            'story story NN N',
            'began begin VBD V-fin',
            '. . . PCT',
            "",
            'The the DT DET',
            'waves wave NNS N',
            'brought bring VBD V-fin',
            'ashore ashore RB ADV',
            'an an DT DET',
            'odd odd JJ ADJ',
            'band band NN N',
            'of of IN PREP',
            'survivors survivor NNS N',
            '- - : PCT',
            'a a DT DET',
            'few few JJ ADJ',
            'ancient ancient JJ ADJ',
            'creatures creature NNS N',
            'that that WDT PRON-rel',
            'had have VBD V-fin',
            'been be VBN V-papa',
            'accidentally accidentally RB ADV',
            'swept sweep VBN V-papa',
            'across across IN PREP',
            'hundreds hundred NNS N',
            'of of IN PREP',
            'kilometres kilometre NNS N',
            'of of IN PREP',
            'ocean ocean NN N',
            'from from IN PREP',
            'a a DT DET',
            'distant distant JJ ADJ',
            'land land NN N',
            '. . . PCT',
            "",
        ]
        expected = spaces_to_tabs(expected)
        result = list(poslemproc.process_dual_lines(lemproc.process_lines(lem_input), posproc.process_lines(pos_input)))
        ok = True
        for idx, (exp_elm, res_elm) in enumerate(zip(expected, result)):
            if exp_elm != res_elm:
                print("Differ:", idx, repr(exp_elm) + "\t" + repr(res_elm))
                ok = False
        self.assertTrue(ok, "POSLEMJoiner: Lines differ, comparison FAILED")


class TestMapsCreation(unittest.TestCase):
    """
    Test creation and sizes of all POS maps.

    Sizes of pos maps as reported from Java code:
        En - 45
        Fr - 34
        It - 52
        Es - 75
        De - 54
        Pt - 24
        Da - 50
        Sv - 152
    """

    def test_fill_pos_maps_english(self):
        hashmap = fill_pos_maps_english()
        self.assertEqual(45, len(hashmap))

    def test_fill_pos_maps_french(self):
        hashmap = fill_pos_maps_french()
        self.assertEqual(34, len(hashmap))

    def test_fill_pos_maps_german(self):
        hashmap = fill_pos_maps_german()
        self.assertEqual(54, len(hashmap))


if __name__ == '__main__':
    unittest.main()
