import unittest
from postag_steps.clean_output import CleanOutput


class CleanOutputTests(unittest.TestCase):
    def test_hello(self):
        result = CleanOutput('nl').process_line(
            "binnenpaneel	binnenpaneel	0	0	0	1	0	0	0	0	0	0	0	0	12	b	l	bi	el	bin	eel	1	0	0	ADJ(prenom,basis,zonder)/0.351370")
        result = list(result)
        self.assertEqual(result, ['binnenpaneel ADJ(prenom,basis,zonder) 0.351370'])
