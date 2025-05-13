import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from lets.abstract_step import AbstractStep
from lets.ner_steps.feat_vect import FeatVectProcessor
from lets.ner_steps.crfpp import CRFPP
from lets.ner_steps.clean_output import CleanOutput


class NER(AbstractStep):
    """NER generation step class."""

    def __init__(self, l='nl'):
        super().__init__(l)
        self._featvect = FeatVectProcessor(l)
        self._crfpp = CRFPP(l)
        self._clean_output = CleanOutput(l)

    def process_lines(self, pos_lines):
        ner_generator = self._clean_output.process_lines(
            self._crfpp.process_lines(
                self._featvect.process_lines(pos_lines)))
        return ner_generator


if __name__ == '__main__':
    NER.main()
