import unittest

from lemmatizer_steps.adjust_capitalization import AdjustCapitalization


class AdjustCapitalizationTest(unittest.TestCase):
    def tests_simple(self):
        res = AdjustCapitalization('nl').process_lines(["binnenpaneel ADJ(prenom,basis,zonder) 0.351370"])
        self.assertEqual(res[0], ["binnenpaneel binnenpaneel ADJ(basis,zonder)", ""])
