from lets.abstract_step import AbstractStep


# TODO duplicate code could be removed
class MakeFeaturesForLemmatizing1(AbstractStep):
    def __init__(self, l):
        super().__init__(l)

    def process_line(self, line):
        return self.makeFeatures1(line, 8)

    def makeFeatures1(self, line, n):
        if (line.strip()):
            # creates feature vectors for the words, serving as input for the (first) CRF++ lemmatization model
            items = line.strip().split()
            # MVDK 12-05-2015: changes have been made to the following 3 lines because the format of the file containing the words with adjusted capitalization has changed (it now contains the original word form in the first column and the word form with adjusted capitalization in the second column, instead of the latter in the first column)
            # orgWord = items[0]
            word = items[1]
            pos = items[2]
            # the (first) lemmatization feature vector consists of the word itself (with adjusted casing), the POS tag, the last 0 up to n letters of the word
            newline = word + ' ' + pos + ' '
            # for i in range(n):
            #     newline += word[=-(i + 1):] + ' '
            yield newline + ' '.join([word[-(i + 1):] for i in range(n)]) + ' '
        else:
            yield ''


if __name__ == "__main__":
    MakeFeaturesForLemmatizing1.main()
