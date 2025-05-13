"""
Created: 2016/10/26
Unit tests for the basic containers modle.

"""

import unittest
from chunker_steps.sentence import SentenceProcessor
from test.unittests.testutil import spaces_to_tabs

class TestSentence(unittest.TestCase):

    def test_creation(self):
        SentenceProcessor()
        SentenceProcessor('en')
        SentenceProcessor(l='en')

    def test_process_input(self):
        language = 'en'
        sequence = spaces_to_tabs([
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
        ])
        sentproc = SentenceProcessor(language)
        expected = ['gender\tgender\tNN\tB-NP', 'equality\tequality\tNN\tI-NP', ',\t,\t,\tO', 'empowerment\tempowerment\tNN\tB-NP', 'of\tof\tIN\tB-PP', 'women\twoman\tNNS\tB-NP', 'and\tand\tCC\tO', 'intergenerational\tintergenerational\tJJ\tB-NP', 'equity\tequity\tNN\tI-NP', ',\t,\t,\tO', '']
        result = list(sentproc.process_lines(sequence))
        #print(expected)
        #print(result)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
