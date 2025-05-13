import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from lets.abstract_step import AbstractStep
from lets.postag_steps.clean_output import CleanOutput
from lets.postag_steps.crfpp import CRFPP
from lets.postag_steps.feat_vects import FeatVects


class POSTag(AbstractStep):
    def __init__(self, l):
        super().__init__()
        self.feat_vects = FeatVects(l)
        self.crfpp = CRFPP(l)
        self.clean_output = CleanOutput(l)

    def process_line(self, line):
        for fv in self.feat_vects.process_line(line):
            for m in self.crfpp.process_line(fv):
                for co in self.clean_output.process_line(m):
                    yield co


if __name__ == "__main__":
    POSTag.main()
