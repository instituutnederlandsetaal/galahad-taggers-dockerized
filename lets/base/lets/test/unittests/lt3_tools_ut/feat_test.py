"""
Test cases for the feats_new module.
These are manually added (in contrast to feat_test_auto.py).

Created on 2016/12/08.

"""

import unittest
from lt3_tools.feats import ScannedToken


class TestScannedToken(unittest.TestCase):

    def test_creation_default_fails(self):
        self.assertRaises(TypeError, ScannedToken)

    def test_creation_w_nonempty_token(self):
        ScannedToken("abracadabra")

    def test_creation_w_empty_token_fails(self):
        self.assertRaises(ValueError, ScannedToken, "")
        self.assertRaises(ValueError, ScannedToken, " \t ")

    def test_hasupper(self):
        self.assertTrue(ScannedToken("ACE11++").hasupper)
        self.assertFalse(ScannedToken("ace11++").hasupper)

    def test_haslower(self):
        self.assertTrue(ScannedToken("ace11++").haslower)
        self.assertFalse(ScannedToken("ACE11++").haslower)

    def test_hasdigit(self):
        self.assertTrue(ScannedToken("ace33++").hasdigit)
        self.assertFalse(ScannedToken("ACEace++").hasdigit)

    def test_haspunct(self):
        self.assertTrue(ScannedToken("ace33!?").haspunct)
        self.assertFalse(ScannedToken("ACEace44").haspunct)

    def test_hasother(self):
        self.assertTrue(ScannedToken("ace33_+").hasother)
        self.assertFalse(ScannedToken("ACEace44").hasother)

    def test_isupper(self):
        self.assertTrue(ScannedToken("ACEUIO").isupper)
        self.assertFalse(ScannedToken("ACEUIo").isupper)
        self.assertFalse(ScannedToken("aCEUIO").isupper)
        self.assertFalse(ScannedToken("ACEUIO11").isupper)

    def test_islower(self):
        self.assertTrue(ScannedToken("aceuio").islower)
        self.assertFalse(ScannedToken("aceuiO").islower)
        self.assertFalse(ScannedToken("Aceuio").islower)
        self.assertFalse(ScannedToken("11aceuio").islower)

    def test_isalpha(self):
        self.assertTrue(ScannedToken("aceuio").isalpha)
        self.assertTrue(ScannedToken("aceuiO").isalpha)
        self.assertTrue(ScannedToken("Aceuio").isalpha)
        self.assertFalse(ScannedToken("11AceuiO").isalpha)
        self.assertFalse(ScannedToken("AceuiO!").isalpha)

    def test_isdigit(self):
        self.assertTrue(ScannedToken("1237890").isdigit)
        self.assertFalse(ScannedToken("1237890a").isdigit)
        self.assertFalse(ScannedToken("A1237890").isdigit)
        self.assertFalse(ScannedToken("12378,90").isdigit)

    def test_ispunct(self):
        self.assertTrue(ScannedToken(".,;!?").ispunct)
        self.assertFalse(ScannedToken(".,;!?1").ispunct)
        self.assertFalse(ScannedToken("A.,;!?").ispunct)
        self.assertFalse(ScannedToken(".,;!?_").ispunct)

    def test_isother(self):
        self.assertTrue(ScannedToken("_@#@_").isother)
        self.assertFalse(ScannedToken("_@#@_?").isother)
        self.assertFalse(ScannedToken("A_@#@_").isother)
        self.assertFalse(ScannedToken("_@#@_5").isother)


if __name__ == '__main__':
    unittest.main()
