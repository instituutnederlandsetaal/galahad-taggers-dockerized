import unittest

from tokenizer import Tokenizer

e = ''
tokenizer = Tokenizer('en', e=True)
t_de = Tokenizer('De', e=True)
t_nl = Tokenizer('Nl', e=True)


class TokenizerTest(unittest.TestCase):
    def tests_params(self):
        ins = ["Test. Test2.", "Test3.Test4.", "Test5", "Test6"]
        self.process_lines_check(ins,
                                 [["Test", ".", "", "Test2", ".", "", ""], ["Test3.Test4", ".", "", ""], ["Test5", ""],
                                  ["Test6", ""]],
                                 Tokenizer('en'))
        self.process_lines_check(ins,
                                 [["Test", ".", "", "Test2", ".", ""], ["Test3.Test4", ".", ""], ["Test5"], ["Test6"]],
                                 Tokenizer('en', r=False))
        self.process_lines_check(ins, [["Test", ".", "Test2", "."], ["Test3.Test4", "."], ["Test5"], ["Test6"]],
                                 Tokenizer('en', r=False, e=None))

    def tests_nosplit(self):
        self.process_lines_check([";-)"], [[";-)", ""]])

    def tests_simple(self):
        self.process_lines_check(["een test"], [["een", "test", ""]])

    def tests_points_without_space_lower(self):
        self.process_lines_check(["1.test"], [["1.test", ""]])

    def tests_points_without_space_upper(self):
        self.process_lines_check(["1.Test"], [["1.Test", ""]])

    def tests_points_with_space_lower(self):
        self.process_lines_check(["1. test"], [["1.", "test", ""]])

    def tests_points_with_space_upper(self):
        self.process_lines_check(["1. Test"], [["1", ".", e, "Test", ""]])

    def tests_split_special_characters(self):
        self.process_lines_check(["2008-2009"], [["2008", "-", "2009", ""]])
        self.process_lines_check(["2008-2009,"], [["2008", "-", "2009", ",", ""]])

    def tests_comma(self):
        self.process_lines_check(["test,test2"], [["test", ",", "test2", ""]])
        self.process_lines_check(["test, test2"], [["test", ",", "test2", ""]])

    def tests_slash(self):
        self.process_lines_check(["test/test2"], [["test", "/", "test2", ""]])
        self.process_lines_check(["test/ test2"], [["test", "/", "test2", ""]])
        self.process_lines_check(["test/test2/test3"], [["test", "/", "test2", "/", "test3", ""]])

    def tests_apply_files_suffixes(self):
        self.process_lines_check(["test's"], [["test", "'s", ""]])

    def tests_apply_files_meas_money(self):
        self.process_lines_check(["41km"], [["41", "km", ""]])

    def tests_punct_at_beginning_except_numbers(self):
        self.process_lines_check([".2"], [[".2", ""]])

    def tests_specialwords(self):
        self.process_lines_check(["cannot"], [["can", "not", ""]])

    def tests_quotes_around_number(self):
        self.process_lines_check(["\"1\""], [["\"", "1\"", ""]])

    def tests_punct_at_beginning(self):
        self.process_lines_check(["test(-test2)"], [["test(-test2)", ""]])
        self.process_lines_check(["\"F9\""], [["\"", "F9\"", ""]])
        self.process_lines_check(["(-30"], [["(", "-", "30", ""]])
        self.process_lines_check(["test(test2)"], [["test", "(", "test2", ")", ""]])
        self.process_lines_check(["I."], [["I.", ""]])
        self.process_lines_check(["'01"], [["'01", ""]])
        self.process_lines_check(["(test)"], [["(", "test", ")", ""]])
        self.process_lines_check(["(lpi)-or"], [["(lpi)-or", ""]])

    def tests_missing_space(self):
        self.process_lines_check(["test?)Test"], [["test", "?", ")", "Test", ""]])

    def tests_punct_at_end(self):
        self.process_lines_check(["test?) Test"], [["test", "?", ")", "Test", ""]])
        self.process_lines_check(["test?)test"], [["test", "?", ")", "test", ""]])
        self.process_lines_check(["test?) test"], [["test", "?", ")", "test", ""]])
        self.process_lines_check(["m.A"], [["m", ".", e, "A", ""]])
        self.process_lines_check(["test?Test"], [["test", "?", e, "Test", ""]])
        self.process_lines_check(["test? Test"], [["test", "?", e, "Test", ""]])
        self.process_lines_check(["test?test"], [["test", "?", "test", ""]])
        self.process_lines_check(["test? test"], [["test", "?", "test", ""]])
        self.process_lines_check(["test."], [["test", ".", e, ""]])
        self.process_lines_check(["sensors). test"], [["sensors", ")", ".", e, "test", ""]])
        self.process_lines_check(["CO32-,"], [["CO32-", ",", ""]])
        self.process_lines_check(["J.C."], [["J.C.", ""]])

    def tests_tags(self):
        self.process_lines_check(["test<http://www.unfccc.int/5900>test2"], [["testtest2", ""]])

    def tests_special_characters(self):
        self.process_lines_check(["---"], [["---", ""]])
        self.process_lines_check(["Wet(div)(I)(1)"], [['Wet(div)(I)', '(', '1', ')', '']])
        self.process_lines_check(["W(div)(I)"], [['W(div)', '(', 'I', ')', '']])
        self.process_lines_check(["test)(°"], [['test', ')', '(', '°', '']])
        self.process_lines_check(["5ter,§1"], [['5ter', ',', '§1', '']])
        self.process_lines_check(["test(ën)"], [['test', '(', 'ën', ')', '']])
        self.process_lines_check(["test.Ó"], [['test', '.', e, 'Ó', '']])
        self.process_lines_check(["test.ï"], [['test', '.', e, 'ï', '']])
        self.process_lines_check(["wonï?1/2t"], [['wonï?1', '/', '2t', '']])
        self.process_lines_check(["test.Ó"], [['test', '.', e, 'Ó', '']])
        self.process_lines_check(["It;s"], [['It', ';', 's', '']])
        self.process_lines_check(["\"test?\" test2"], [['"', 'test', '?', '"', 'test2', '']])
        self.process_lines_check(["like 'em big"], [["like", "'em", "big", ""]])
        self.process_lines_check(["test!! takes"], [["test", "!", "!", e, "takes", ""]])
        self.process_lines_check(["test!!! takes"], [["test", "!", "!", "!", e, "takes", ""]])
        self.process_lines_check(["test! takes"], [["test", "!", "takes", ""]])
        self.process_lines_check(["test! Takes"], [["test", "!", e, "Takes", ""]])
        self.process_lines_check(["test!! Takes"], [["test", "!", "!", e, "Takes", ""]])
        self.process_lines_check(["test!!! Takes"], [["test", "!", "!", "!", e, "Takes", ""]])
        self.process_lines_check(["test &amp; test2"], [["test", "&", "test2", ""]])


    def tests_sgml(self):
        self.process_lines_check(["&lt;Ziekenhuis&gt;"], [["", ""]])

        self.process_lines_check(["&lt;test&gt; &lt;test&gt;", "&lt;test&gt; &lt;test&gt;", "Test"],
                                 [["", "", ""], ["", "", ""], ["Test", ""]])
        self.process_lines_check(["&lt;b&gt;&lt;i&gt;"], [["", ""]])
        self.process_lines_check(["http://test?test2"], [["http://test", "?", "test2", ""]])
        self.process_lines_check(["http://ec"], [["http://ec", ""]])
        self.process_lines_check(["&lt;"], [["<", ""]])
        self.process_lines_check(["&lt;test&gt;"], [["", ""]])
        self.process_lines_check(["&lt;i&gt;"], [["", ""]])
        self.process_lines_check(["Ä(C)"], [["Ä(C", ")", ""]])

    def tests_blank_lines(self):
        self.process_lines_check(["test", "", "Test2"], [["test", e, ""], ["Test2", ""]])
        self.process_lines_check(["test", "", "test2"], [["test", e, ""], ["test2", ""]])
        self.process_lines_check([""], [])
        self.process_lines_check([" ", " ", " ", " ", " ", " ", "test2"], [["test2", ""]])
        self.process_lines_check(["test.", "test2"], [["test", ".", e, ""], ["test2", ""]])
        self.process_lines_check(["test:", "test2"], [["test", ":", ""], ["test2", ""]])
        self.process_lines_check([" ", " ", "test2"], [["test2", ""]])
        self.process_lines_check(["test.", "", "test2"], [["test", ".", e, ""], ["test2", ""]])
        self.process_lines_check(["brie.y"], [['brie.y', '']])

    def tests_hyphen(self):
        self.process_lines_check(["DEA-", "invloed"], [[''], ['DEA-invloed', '']],
                                 tokenizer=t_nl)
        self.process_lines_check(["Test", "", "Test2-", "test3"], [['Test', e, ''], [''], ['Test2test3', '']],
                                 tokenizer=t_de)
        self.process_lines_check(["avond-", "of zaterdagcursus"], [['avond-', ''], ['of', 'zaterdagcursus', '']],
                                 tokenizer=t_nl)
        self.process_lines_check(["schiet-", "en-vechtgeval"], [['schiet-', ''], ['en-vechtgeval', '']],
                                 tokenizer=t_nl)
        self.process_lines_check(["avond- of zaterdagcursus"], [['avond-', 'of', 'zaterdagcursus', '']], tokenizer=t_nl)
        self.process_lines_check(["test-", "", "test2"], [['test -', e, ''], ['test2', '']])
        self.process_lines_check(["test-", "test2"], [[''], ["testtest2", ""]])
        self.process_lines_check(["Test", "", "Test2"], [['Test', e, ''], ['Test2', '']], tokenizer=t_de)
        self.process_lines_check(["Test- und test2"], [['Test-', 'und', 'test2', '']], tokenizer=t_de)
        self.process_lines_check(["test? -test2"], [['test', '?', e, '-', 'test2', '']])
        # self.process_lines_check(["test. 1-2-"], [["test", ".", "", "1 -", ""]])
        self.process_lines_check(["1-2-", "Test"], [["1", "-", ""], ['1-2-Test', '']])
        self.process_lines_check(["test-"], [["test -", ""]])
        self.process_lines_check(["test-", "Test2"], [[''], ["test-Test2", ""]])

    def tests_ordinals(self):
        self.process_lines_check(["2. Test"], [['2', '.', e, 'Test', '']])
        self.process_lines_check(["2. Test"], [['2.', 'Test', '']], tokenizer=Tokenizer('De'))

    def tests_not_in_test_files(self):
        self.process_lines_check(["hfl=0.5012"], [['hfl', '=0.5012', '']])
        self.process_lines_check(["f5,-"], [['f', '5,-', '']])
        self.process_lines_check(["hfl50"], [['hfl', '50', '']])
        self.process_lines_check(["DM0,50"], [['DM', '0,50', '']])
        self.process_lines_check(["BEF7,50"], [['BEF', '7,50', '']])
        self.process_lines_check(["10.-"], [['10.-', '']])
        self.process_lines_check(["10,-"], [['10,-', '']])
        self.process_lines_check(["10.="], [['10.=', '']])
        self.process_lines_check(["10,="], [['10,=', '']])
        self.process_lines_check(["&dummy;"], [['&dummy;', '']])
        self.process_lines_check(["H&M"], [['H', '&', 'M', '']])
        self.process_lines_check(["i&gt;10"], [['i', '>', '10', '']])
        self.process_lines_check(["abc.--."], [['abc', '.', e, '--', '.', e, '']])
        self.process_lines_check(["abc.--"], [['abc', '.', '--', e, '']])
        self.process_lines_check(["zegt-ie"], [['zegt', '-ie', '']], tokenizer=t_nl)


    def process_lines_check(self, lines, expected, tokenizer=tokenizer):
        for r, e in zip(tokenizer.process_lines(iter(lines)), [e for es in expected for e in es]):
            # print('r', r)
            # print('e', e)
            self.assertEqual(r, e)
