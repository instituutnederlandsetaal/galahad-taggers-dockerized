import os
from lets.abstract_crfpp import AbstractCRFPP


class CRFPP(AbstractCRFPP):
    def __init__(self, l):
        super(CRFPP, self).__init__(os.path.dirname(os.path.realpath(__file__)) + "/../models/lemmatizer/Lemmatizer.{}".format(l), l)


if __name__ == "__main__":
    CRFPP.main()
