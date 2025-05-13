"""
Character scanning utils unit tests.

"""

import unittest
from random import randint
import time

from lt3_tools import scanutil


@unittest.skip("time consuming")
class TestPerformance(unittest.TestCase):

    DATA_SIZE = 50000
    LEN_RANGE = 5, 16
    CHAR_RANGE = 23, 127 # ascii printable characters

    def setUp(self):
        """ Generates a list of DATA_SIZE random strings to test with."""
        self.data = ["".join(chr(code) for code in (randint(*self.CHAR_RANGE)
                        for _ in range(randint(*self.LEN_RANGE))))
                            for _ in range(self.DATA_SIZE)]

    def test_ascii_scan(self):
        """Enable this to see how much time it takes to scan DATA_SIZE strings
           with chars having random ascii codes (within CHAR_RANGE) and length
           within the LEN_RANGE."""
        char_scan = scanutil.lookup_scan
        start_clock, start_time = time.clock(), time.time()
        [char_scan(token) for token in self.data]
        elapsed_clock, elpases_time = time.clock() - start_clock, time.time() - start_time
        print("test_ascii_scan:", elapsed_clock, elpases_time)


class TestLookupScan(unittest.TestCase):

    _char_scan = staticmethod(scanutil.lookup_scan)

    def test_char_scan_case_00000(self):
        self.assertEqual((False, False, False, False, False), self._char_scan(""))

    def test_char_scan_case_00001(self):
        self.assertEqual((False, False, False, False, True), self._char_scan("#"))
        self.assertEqual((False, False, False, False, True), self._char_scan("~"))
        self.assertEqual((False, False, False, False, True), self._char_scan("+-_"))
        self.assertEqual((False, False, False, False, True), self._char_scan("#$%|~"))
        self.assertEqual((False, False, False, False, True), self._char_scan("#$%*+-=@[]_`|~"))

    def test_char_scan_case_00010(self):
        self.assertEqual((False, False, False, True, False), self._char_scan("!"))
        self.assertEqual((False, False, False, True, False), self._char_scan("}"))
        self.assertEqual((False, False, False, True, False), self._char_scan("\\{:)&/"))
        self.assertEqual((False, False, False, True, False), self._char_scan("<'\".,>"))
        self.assertEqual((False, False, False, True, False), self._char_scan("!\"&'(),./:<>?\\{}"))

    def test_char_scan_case_00011(self):
        self.assertEqual((False, False, False, True, True), self._char_scan("!#"))
        self.assertEqual((False, False, False, True, True), self._char_scan("+}"))
        self.assertEqual((False, False, False, True, True), self._char_scan("\\-*%{:=*~`&/"))
        self.assertEqual((False, False, False, True, True), self._char_scan("<'\"(._.)^,>"))
        self.assertEqual((False, False, False, True, True), self._char_scan("#$%*+-;=@[]_`|~!\"&'(),./:<>?\\^{}"))

    def test_char_scan_case_00100(self):
        self.assertEqual((False, False, True, False, False), self._char_scan("0"))
        self.assertEqual((False, False, True, False, False), self._char_scan("9"))
        self.assertEqual((False, False, True, False, False), self._char_scan("06548"))
        self.assertEqual((False, False, True, False, False), self._char_scan("12972"))
        self.assertEqual((False, False, True, False, False), self._char_scan("0123456789"))

    def test_char_scan_case_00101(self):
        self.assertEqual((False, False, True, False, True), self._char_scan("0-"))
        self.assertEqual((False, False, True, False, True), self._char_scan("_#9"))
        self.assertEqual((False, False, True, False, True), self._char_scan("0=*654+$8"))
        self.assertEqual((False, False, True, False, True), self._char_scan("12#9%7@[_]2"))
        self.assertEqual((False, False, True, False, True), self._char_scan("#$%*+-=@[]_`|~0123456789"))

    def test_char_scan_case_00110(self):
        self.assertEqual((False, False, True, True, False), self._char_scan("0}"))
        self.assertEqual((False, False, True, True, False), self._char_scan("{9"))
        self.assertEqual((False, False, True, True, False), self._char_scan("(0!6<5>4?8)"))
        self.assertEqual((False, False, True, True, False), self._char_scan("1\"29\\&7'2"))
        self.assertEqual((False, False, True, True, False), self._char_scan("0123456789!\"&'(),./:<>?\\{}"))

    def test_char_scan_case_00111(self):
        self.assertEqual((False, False, True, True, True), self._char_scan("[0}"))
        self.assertEqual((False, False, True, True, True), self._char_scan("{9]"))
        self.assertEqual((False, False, True, True, True), self._char_scan("(0!=6<5>4+?8)"))
        self.assertEqual((False, False, True, True, True), self._char_scan("1\"-29\\&7@'_`2"))
        self.assertEqual((False, False, True, True, True), self._char_scan("0123456789#$%*+-;=@[]_`|~!\"&'(),./:<>?\\^{}"))

    def test_char_scan_case_01000(self):
        self.assertEqual((False, True, False, False, False), self._char_scan("u"))
        self.assertEqual((False, True, False, False, False), self._char_scan("o"))
        self.assertEqual((False, True, False, False, False), self._char_scan("ace"))
        self.assertEqual((False, True, False, False, False), self._char_scan("aceuio"))
        self.assertEqual((False, True, False, False, False), self._char_scan("euuiio"))

    def test_char_scan_case_01001(self):
        self.assertEqual((False, True, False, False, True), self._char_scan("u#$%*+"))
        self.assertEqual((False, True, False, False, True), self._char_scan("o]"))
        self.assertEqual((False, True, False, False, True), self._char_scan("ace$%"))
        self.assertEqual((False, True, False, False, True), self._char_scan("aceuio#$%*+-=@[]_`|~"))
        self.assertEqual((False, True, False, False, True), self._char_scan("euuiio+-="))

    def test_char_scan_case_01010(self):
        self.assertEqual((False, True, False, True, False), self._char_scan('u"&'))
        self.assertEqual((False, True, False, True, False), self._char_scan("o>?\\;{"))
        self.assertEqual((False, True, False, True, False), self._char_scan("ace{}"))
        self.assertEqual((False, True, False, True, False), self._char_scan("aceuio!\"&\'(),./:<>?\\{}"))
        self.assertEqual((False, True, False, True, False), self._char_scan("euuiio),./:<>"))

    def test_char_scan_case_01011(self):
        self.assertEqual((False, True, False, True, True), self._char_scan("u/:<$%*"))
        self.assertEqual((False, True, False, True, True), self._char_scan("o!\"&'()\-;=@[]"))
        self.assertEqual((False, True, False, True, True), self._char_scan("ace\\^{#$%*+"))
        self.assertEqual((False, True, False, True, True), self._char_scan('aceuio!"&\'(),./:<>?\\^{}#$%*+-;=@[]_`|~'))
        self.assertEqual((False, True, False, True, True), self._char_scan("euuiio\\^{]_`"))

    def test_char_scan_case_01100(self):
        self.assertEqual((False, True, True, False, False), self._char_scan("u0123"))
        self.assertEqual((False, True, True, False, False), self._char_scan("o67"))
        self.assertEqual((False, True, True, False, False), self._char_scan("ace23456789"))
        self.assertEqual((False, True, True, False, False), self._char_scan("aceuio0123456789"))
        self.assertEqual((False, True, True, False, False), self._char_scan("euuiio234"))

    def test_char_scan_case_01101(self):
        self.assertEqual((False, True, True, False, True), self._char_scan("u678$%*+"))
        self.assertEqual((False, True, True, False, True), self._char_scan("o0123*+-"))
        self.assertEqual((False, True, True, False, True), self._char_scan("ace6[]_`|"))
        self.assertEqual((False, True, True, False, True), self._char_scan("aceuio0123456789#$%*+-=@[]_`|~"))
        self.assertEqual((False, True, True, False, True), self._char_scan("euuiio012=@[]"))

    def test_char_scan_case_01110(self):
        self.assertEqual((False, True, True, True, False), self._char_scan("a5."))
        self.assertEqual((False, True, True, True, False), self._char_scan("uae29.,"))
        self.assertEqual((False, True, True, True, False), self._char_scan("io18621()"))
        self.assertEqual((False, True, True, True, False), self._char_scan("c33.,028"))
        self.assertEqual((False, True, True, True, False), self._char_scan("uco232!"))

    def test_char_scan_case_01111(self):
        self.assertEqual((False, True, True, True, True), self._char_scan("u54.;_#"))
        self.assertEqual((False, True, True, True, True), self._char_scan("aeu92,@"))
        self.assertEqual((False, True, True, True, True), self._char_scan("oi261()_"))
        self.assertEqual((False, True, True, True, True), self._char_scan("ac388}~"))
        self.assertEqual((False, True, True, True, True), self._char_scan("uce595?]"))

    def test_char_scan_case_10000(self):
        self.assertEqual((True, False, False, False, False), self._char_scan("E"))
        self.assertEqual((True, False, False, False, False), self._char_scan("AOA"))
        self.assertEqual((True, False, False, False, False), self._char_scan("UIIO"))
        self.assertEqual((True, False, False, False, False), self._char_scan("CO"))
        self.assertEqual((True, False, False, False, False), self._char_scan("IAOAE"))

    def test_char_scan_case_10001(self):
        self.assertEqual((True, False, False, False, True), self._char_scan("UUAE_"))
        self.assertEqual((True, False, False, False, True), self._char_scan("OI@%"))
        self.assertEqual((True, False, False, False, True), self._char_scan("II*~*"))
        self.assertEqual((True, False, False, False, True), self._char_scan("C++"))
        self.assertEqual((True, False, False, False, True), self._char_scan("EO$"))

    def test_char_scan_case_10010(self):
        self.assertEqual((True, False, False, True, False), self._char_scan("UUAE(!)?"))
        self.assertEqual((True, False, False, True, False), self._char_scan("OI,"))
        self.assertEqual((True, False, False, True, False), self._char_scan("II.)"))
        self.assertEqual((True, False, False, True, False), self._char_scan("C)("))
        self.assertEqual((True, False, False, True, False), self._char_scan("EO.:"))

    def test_char_scan_case_10011(self):
        self.assertEqual((True, False, False, True, True), self._char_scan("IO,._"))
        self.assertEqual((True, False, False, True, True), self._char_scan("CUE(!)?#"))
        self.assertEqual((True, False, False, True, True), self._char_scan("AOE/-"))
        self.assertEqual((True, False, False, True, True), self._char_scan("OI,?*"))
        self.assertEqual((True, False, False, True, True), self._char_scan("ACC(.&)$*"))

    def test_char_scan_case_10100(self):
        self.assertEqual((True, False, True, False, False), self._char_scan("C1"))
        self.assertEqual((True, False, True, False, False), self._char_scan("5A"))
        self.assertEqual((True, False, True, False, False), self._char_scan("AUOE58CA6"))
        self.assertEqual((True, False, True, False, False), self._char_scan("168AE71CU"))
        self.assertEqual((True, False, True, False, False), self._char_scan("ACEUIO0123456789"))

    def test_char_scan_case_10101(self):
        self.assertEqual((True, False, True, False, True), self._char_scan("C1*"))
        self.assertEqual((True, False, True, False, True), self._char_scan("5+A"))
        self.assertEqual((True, False, True, False, True), self._char_scan("AUOE+[@58]`CA6"))
        self.assertEqual((True, False, True, False, True), self._char_scan("16=E8AE-7$%1CU"))
        self.assertEqual((True, False, True, False, True), self._char_scan("ACEUIO0123456789#$%*+-=@[]_`|~"))

    def test_char_scan_case_10110(self):
        self.assertEqual((True, False, True, True, False), self._char_scan("C{1"))
        self.assertEqual((True, False, True, True, False), self._char_scan("5?A"))
        self.assertEqual((True, False, True, True, False), self._char_scan("AUO!\"E5/.,8CA&6"))
        self.assertEqual((True, False, True, True, False), self._char_scan("1)68(AE7'1C><U"))
        self.assertEqual((True, False, True, True, False), self._char_scan("!\"&'(),./:<>?\\{}ACEUIO0123456789"))

    def test_char_scan_case_10111(self):
        self.assertEqual((True, False, True, True, True), self._char_scan("C{$1"))
        self.assertEqual((True, False, True, True, True), self._char_scan("5?A~"))
        self.assertEqual((True, False, True, True, True), self._char_scan("A`%UO!\"E[@5/.=,8C#A&6"))
        self.assertEqual((True, False, True, True, True), self._char_scan("1_)6-8;(AE7'1C*+>^<$U"))
        self.assertEqual((True, False, True, True, True), self._char_scan("!\"&'(),./:<>?\\^{}ACEUIO0123456789#$%*+-;=@[]_`|~"))

    def test_char_scan_case_11000(self):
        self.assertEqual((True, True, False, False, False), self._char_scan("eC"))
        self.assertEqual((True, True, False, False, False), self._char_scan("Uo"))
        self.assertEqual((True, True, False, False, False), self._char_scan("AuCEIoa"))
        self.assertEqual((True, True, False, False, False), self._char_scan("ciOaUAO"))
        self.assertEqual((True, True, False, False, False), self._char_scan("aceuioACEUIO"))

    def test_char_scan_case_11001(self):
        self.assertEqual((True, True, False, False, True), self._char_scan("eC="))
        self.assertEqual((True, True, False, False, True), self._char_scan("@Uo"))
        self.assertEqual((True, True, False, False, True), self._char_scan("A#`uCEI$~oa"))
        self.assertEqual((True, True, False, False, True), self._char_scan("]ciO|_aUA[O"))
        self.assertEqual((True, True, False, False, True), self._char_scan("aceuio#$%*+-=@[]_`|~ACEUIO"))

    def test_char_scan_case_11010(self):
        self.assertEqual((True, True, False, True, False), self._char_scan("e<C"))
        self.assertEqual((True, True, False, True, False), self._char_scan(">Uo"))
        self.assertEqual((True, True, False, True, False), self._char_scan("Au/!.CE\\Io{a"))
        self.assertEqual((True, True, False, True, False), self._char_scan("c},iOa)?(UA\"O"))
        self.assertEqual((True, True, False, True, False), self._char_scan("aceuioACEUIO!\"&'(),./:<>?\\{}"))

    def test_char_scan_case_11011(self):
        self.assertEqual((True, True, False, True, True), self._char_scan("Ca<$"))
        self.assertEqual((True, True, False, True, True), self._char_scan("ACeu,.+-"))
        self.assertEqual((True, True, False, True, True), self._char_scan("UIOuio!?()@[]"))
        self.assertEqual((True, True, False, True, True), self._char_scan("oiuACE[]()"))
        self.assertEqual((True, True, False, True, True), self._char_scan("#$%*+-;=@[]_`|~Ac!"))

    def test_char_scan_case_11100(self):
        self.assertEqual((True, True, True, False, False), self._char_scan("Ca5"))
        self.assertEqual((True, True, True, False, False), self._char_scan("ACeu89"))
        self.assertEqual((True, True, True, False, False), self._char_scan("UIOuio237"))
        self.assertEqual((True, True, True, False, False), self._char_scan("oiuACE120"))
        self.assertEqual((True, True, True, False, False), self._char_scan("98ac67UIOe"))

    def test_char_scan_case_11101(self):
        self.assertEqual((True, True, True, False, True), self._char_scan("Ca5#"))
        self.assertEqual((True, True, True, False, True), self._char_scan("ACeu89$"))
        self.assertEqual((True, True, True, False, True), self._char_scan("UIOuio237+-@"))
        self.assertEqual((True, True, True, False, True), self._char_scan("oi~uAC[]E120"))
        self.assertEqual((True, True, True, False, True), self._char_scan("9@8ac67UI=Oe"))

    def test_char_scan_case_11110(self):
        self.assertEqual((True, True, True, True, False), self._char_scan("Ca5,"))
        self.assertEqual((True, True, True, True, False), self._char_scan("ACeu89!?"))
        self.assertEqual((True, True, True, True, False), self._char_scan("UIOuio237(){}"))
        self.assertEqual((True, True, True, True, False), self._char_scan("oi:uAC,.E120"))
        self.assertEqual((True, True, True, True, False), self._char_scan("9?8ac67UI?Oe"))

    def test_char_scan_case_11111(self):
        self.assertEqual((True, True, True, True, True), self._char_scan("Ca5,@"))
        self.assertEqual((True, True, True, True, True), self._char_scan("ACeu89!?#$"))
        self.assertEqual((True, True, True, True, True), self._char_scan("UIOuio237(){}[]+-"))
        self.assertEqual((True, True, True, True, True), self._char_scan("oi:uA@C,.E1^20"))
        self.assertEqual((True, True, True, True, True), self._char_scan("9?8ac67UI;,Oe_#"))


class TestTrueScan(TestLookupScan):
    _char_scan = staticmethod(scanutil.true_scan)


class TestAsciiScan(TestLookupScan):
    _char_scan = staticmethod(scanutil.ascii_scan)


if __name__ == '__main__':
    unittest.main()
