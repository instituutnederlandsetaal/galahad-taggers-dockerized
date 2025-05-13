from lets.abstract_step import AbstractStep


class MakeFeaturesForLemmatizing2(AbstractStep):
    def __init__(self, l):
        super().__init__(l)

    def process_line(self, line):
        return self.makeFeatures2(line, 10)

    def makeFeatures2(self, line, n):
        if (line.strip()):
            # creates feature vectors for the words, serving as input for the second CRF++ lemmatization model (only used for German and Dutch)
            items = line.strip().split()
            # MVDK 12-05-2015: changes have been made to the following 3 lines because the format of the file containing the words with adjusted capitalization has changed (it now contains the original word form in the first column and the word form with adjusted capitalization in the second column, instead of the latter in the first column)
            # orgWord = items[0]
            word = items[1]
            pos = items[2]
            # the second lemmatization feature vector consists of the word itself (with adjusted casing), the POS tag, the first 0 up to n letters of the word
            newline = word + ' ' + pos + ' '
            # for i in range(n):
            #     newline += word[:n - i] + ' '
            yield newline + ' '.join([word[:n - i] for i in range(n)]) + ' '
        else:
            yield ''


if __name__ == "__main__":
    MakeFeaturesForLemmatizing2.main()
