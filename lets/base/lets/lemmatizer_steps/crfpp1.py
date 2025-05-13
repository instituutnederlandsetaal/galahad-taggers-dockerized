import os
from lets.abstract_crfpp import AbstractCRFPP


class CRFPP1(AbstractCRFPP):
    def __init__(self, l):
        super(CRFPP1, self).__init__(os.path.dirname(os.path.realpath(__file__)) + "/../models/lemmatizer/Lemmatizer1.{}".format(l), l)


if __name__ == "__main__":
    CRFPP1.main()
