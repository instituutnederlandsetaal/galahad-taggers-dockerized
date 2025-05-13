import unittest
from postag_steps.feat_vects import FeatVects


class FeatVectsTest(unittest.TestCase):
    def tests_empty(self):
        self.check(["\n"], ["", ""])

    def tests_simple(self):
        self.check(["binnenpaneel\n"],
                   ["binnenpaneel binnenpaneel 0 0 0 1 0 0 0 0 0 0 0 0 12 b l bi el bin eel 1 0 0", ""])

    def tests_special(self):
        self.check(["Kappa²\n"],
                   ["Kappa² kappa² 1 0 0 0 0 0 0 0 0 0 0 0 6 k ² ka a² kap pa² 1 0 1", ""])

    def tests_dots(self):
        self.check(["...U\n"],
                   ["...U ...u 0 1 1 0 0 0 0 0 1 0 1 0 4 . u .. .u ... ..u 1 1 0", ""])

    def tests_abbr(self):
        self.check(["B.S.\n"],
                   ["B.S. b.s. 1 1 1 0 0 0 0 0 1 0 1 0 4 b . b. s. b.s .s. 1 1 1", ""])

    def tests_abbr2(self):
        self.check(["Art.\n"],
                   ["Art. art. 1 0 0 0 0 0 0 0 1 0 0 0 4 a . ar t. art rt. 1 0 1", ""])

    def tests_sentence_all_upper(self):
        self.check(["I.VOORSTELLING\n"],
                   ["I.VOORSTELLING i.voorstelling 1 1 1 0 0 0 0 0 1 0 0 0 14 i g i. ng i.v ing 1 1 1", ""])

    def tests_multiple(self):
        self.check(["binnenpaneel\n", "dakversteviging\n", "\n"],
                   ["binnenpaneel binnenpaneel 0 0 0 1 0 0 0 0 0 0 0 0 12 b l bi el bin eel 1 0 0",
                    "dakversteviging dakversteviging 0 0 0 1 0 0 0 0 0 0 0 0 15 d g da ng dak ing 0 0 0",
                    "", ""])

    def tests_all_caps(self):
        self.check(["WET\n", "BETREFFENDE\n", "\n"],
                   ["WET wet 1 1 1 0 0 0 0 0 0 0 0 0 3 w t we et wet wet 1 1 1",
                    "BETREFFENDE betreffende 1 1 1 0 0 0 0 0 0 0 0 0 11 b e be de bet nde 0 1 1",
                    "", ""])

    def tests_special_chars(self):
        self.check(["WET\n", "{\n", "§(°\n", "\n"],
                   ["WET wet 1 1 1 0 0 0 0 0 0 0 0 0 3 w t we et wet wet 1 1 1",
                    "{ { 0 0 0 1 0 0 0 1 1 0 0 0 1 { { { { { { 0 1 1",
                    "§(° §(° 0 0 0 1 0 0 0 0 1 0 0 0 3 § ° §( (° §(° §(° 0 1 1",
                    "", ""])

    def tests_special_chars2(self):
        self.check(["³\n", ],
                   ["³ ³ 0 0 0 1 0 0 0 0 0 0 0 0 1 ³ ³ ³ ³ ³ ³ 1 0 0", ""])
    def tests_special_chars3(self):
        self.check(["rOX^dar", ],
                   ["rOX^dar rox^dar 0 0 1 0 0 0 0 0 0 0 0 0 7 r r ro ar rox dar 1 0 0", ""])
    def tests_special_chars4(self):
        self.check(["^", ],
                   ["^ ^ 0 0 0 1 0 0 0 1 0 0 0 0 1 ^ ^ ^ ^ ^ ^ 1 0 0", ""])

    def check(self, ins, output):
        result = FeatVects().process_lines(ins)
        self.assertEqual(list(result), output)
