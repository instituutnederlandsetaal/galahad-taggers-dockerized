import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from lets.abstract_step import AbstractStep
from lets.lemmatizer_steps.adjust_capitalization import AdjustCapitalization
from lets.lemmatizer_steps.crfpp import CRFPP
from lets.lemmatizer_steps.crfpp1 import CRFPP1
from lets.lemmatizer_steps.crfpp2 import CRFPP2
from lets.lemmatizer_steps.make_features_for_lemmatizing1 import MakeFeaturesForLemmatizing1
from lets.lemmatizer_steps.make_features_for_lemmatizing2 import MakeFeaturesForLemmatizing2
from lets.lemmatizer_steps.make_lemma_output_DEF import MakeLemmaOutputDEF
from itertools import tee


class Lemmatizer(AbstractStep):
    def __init__(self, l):
        """
        Args:
            l: language
        """
        super().__init__()
        language = l
        self.language = language
        self.adjustCapitalization = AdjustCapitalization(language)
        self.makeLemmaOutputDEF = MakeLemmaOutputDEF(language)
        self.makeFeaturesForLemmatizing1 = MakeFeaturesForLemmatizing1(language)
        if language in ['de', 'nl']:
            self.makeFeaturesForLemmatizing2 = MakeFeaturesForLemmatizing2(language)
            self.crfpp1 = CRFPP1(language)
            self.crfpp2 = CRFPP2(language)
        else:
            self.crfpp1 = CRFPP(language)

    def process_line(self, line):
        lemFeat1 = self.adjustCapitalization.process_line(line)
        if self.language in ['de', 'nl']:
            lemFeat1, lemFeat11, lemFeat12 = tee(lemFeat1, 3)
            lemOut2s = (l for a in lemFeat12 for b in self.makeFeaturesForLemmatizing2.process_line(a) for l in
                        self.crfpp2.process_line(b))
        else:
            lemFeat1, lemFeat11 = tee(lemFeat1, 2)
            lemOut2s = None

        lemOut1s = (l for a in lemFeat11 for b in self.makeFeaturesForLemmatizing1.process_line(a) for l in
                    self.crfpp1.process_line(b))
        output = self.makeLemmaOutputDEF.process_dual_lines(lemFeat1, lemOut1s, lemOut2s)
        result = output
        for r in result:
            yield r


if __name__ == "__main__":
    Lemmatizer.main()
