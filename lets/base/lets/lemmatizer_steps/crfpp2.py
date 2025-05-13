import os
from lets.abstract_crfpp import AbstractCRFPP


class CRFPP2(AbstractCRFPP):
    def __init__(self, l):
        super(CRFPP2, self).__init__(os.path.dirname(os.path.realpath(__file__)) + "/../models/lemmatizer/Lemmatizer2.{}".format(l), l)


if __name__ == "__main__":
    CRFPP2.main()
