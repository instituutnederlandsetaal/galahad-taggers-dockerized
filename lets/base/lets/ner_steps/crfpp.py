"""
CRFPP sub-step for the NER processor step.
Created on 2016/12/08.

"""
import os
from lets.abstract_crfpp import AbstractCRFPP


class CRFPP(AbstractCRFPP):
    """CRFPP sub-step for the NER processor step."""

    def __init__(self, l='nl'):
        super(CRFPP, self).__init__(os.path.dirname(os.path.realpath(__file__)) + "/../models/ner/NER.{}".format(l), l)


if __name__ == '__main__':
    CRFPP.main()
