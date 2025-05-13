import CRFPP

from lets.abstract_step import AbstractStep


class AbstractCRFPP(AbstractStep):
    def __init__(self, model, language='nl'):
        super().__init__(language)
        self.tagger = CRFPP.Tagger("-v1 -m {} ".format(model))

    def process_line(self, line):
        if (line.strip()):
            self.tagger.add(line.strip())
        else:
            if (not self.tagger.empty()):
                self.tagger.parse()
                yield '# {:.6f}'.format(self.tagger.prob())
                for i in range(self.tagger.size()):
                    input_fields = [self.tagger.x(i, j).strip() for j in range(self.tagger.xsize())]
                    result = self.tagger.yname(self.tagger.y(i))
                    probability = self.tagger.prob(i)
                    yield '\t'.join(input_fields + ["{}/{:.6f}".format(result, probability)])
                self.tagger.clear()
                yield ''
