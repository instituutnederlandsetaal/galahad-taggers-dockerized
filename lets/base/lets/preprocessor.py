import os
import sys
from itertools import tee

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from lets.abstract_step import AbstractStep
from lets.tokenizer import Tokenizer
from lets.postag import POSTag
from lets.lemmatizer import Lemmatizer
from lets.chunker import Chunker
from lets.ner import NER


class PreProcessor(AbstractStep):
    def __init__(self, l):
        super().__init__()
        self.tokenizer = Tokenizer(l)
        self.postag = POSTag(l)
        self.lemmatizer = Lemmatizer(l)
        self.chunker = Chunker(l)
        self.ner = NER(l)

    def process_line(self, line):
        toks = self.tokenizer.process_line(line)
        poss, poss_for_cnk, poss_for_lem, poss_for_ner = tee((p for t in toks for p in self.postag.process_line(t)), 4)
        lems, lems_for_cnk = tee((lem for pos in poss_for_lem for lem in self.lemmatizer.process_line(pos)), 2)
        cnks = self.chunker.process_dual_lines(lems_for_cnk, poss_for_cnk)
        ners = self.ner.process_lines(poss_for_ner)
        for fields in zip(toks, poss, lems, cnks, ners):
            tok = fields[0]
            pos = fields[1].split(' ')[1] if fields[1].strip() else ''
            lem = fields[2].split(' ')[1] if fields[2].strip() else ''
            cnk = fields[3].split('\t')[3] if fields[3].strip() else ''
            ner = fields[4].split(' ')[1] if fields[2].strip() else ''
            yield ('\t'.join([tok, lem, pos, cnk, ner]))


if __name__ == "__main__":
    PreProcessor.main()