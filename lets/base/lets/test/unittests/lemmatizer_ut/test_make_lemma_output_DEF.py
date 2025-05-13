import unittest

from lemmatizer_steps.make_lemma_output_DEF import MakeLemmaOutputDEF


class MakeLemmaOutputDEFTest(unittest.TestCase):
    def tests_simple(self):
        res = MakeLemmaOutputDEF('nl').process_line(
            ["Op op VZ(init)", "", "de de LID()"],
            iter(["# 0.651872", "op	VZ(init)	p	op	op	op	op	op	op	op	+Ipen/0.651872", "",
                  "# 0.282879", "de	LID()	e	de	de	de	de	de	de	de	//0.282879", ""]),
            iter(["# 0.620413",
                  "op	VZ(init)	op	op	op	op	op	op	op	op	op	o	2ge/0.620413",
                  "",
                  "# 0.177209",
                  "de	LID()	de	de	de	de	de	de	de	de	de	d	4ge/0.177209", ""])
        )
        self.assertEqual(res[0], "Op op /")
        self.assertEqual(res[1], "de de 0.282879")
