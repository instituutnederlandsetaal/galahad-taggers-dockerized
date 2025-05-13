import re

from lets.abstract_step import AbstractStep


class FeatVects(AbstractStep):
    def __init__(self, l=None):
        super().__init__(l)
        self.contains_punct = ['.', '!', '?', ',', ';', ':', '&', '(', ')', '{', '}', '/', '<', '>', '"', '\'', '\\']
        self.is_punct = self.contains_punct + ['^']
        self.first_word = True
        self.lines = []

    def process_line(self, line):
        line = line.strip()
        if (line):
            self.lines.append(line)
        else:
            if (self.lines):
                for r in self.process_sentence(self.lines):
                    yield r
                self.lines = []
            yield ''

    def process_sentence(self, sentence):
        sentence_all_upper = any(w.isalpha() for s in sentence for w in s) and all(w.upper() == w for w in sentence)
        all_first_upper = any(w[0].isalpha() for w in sentence) and not any(w[0].islower() for w in sentence)
        return [self.sentence_detail(s, i == 0, sentence_all_upper, all_first_upper) for i, s in
                enumerate(sentence)]

    def sentence_detail(self, line, is_first, sentence_all_upper, all_first_upper):
        if (line):
            def bool_to_str(bools):
                return ["1" if b else "0" for b in bools]

            def is_initial(line):
                if re.search(r'[A-Z]', line):
                    if re.search(r'[^A-Z\.]', line):
                        return False
                    elif not '.' in line:
                        return False
                    elif re.search(r'([A-Z](\.?)){6,}', line):
                        return False
                    else:
                        return True
                else:
                    return False

            results = [line, line.lower()]

            any_digit = any(x in '0123456789' for x in line)
            any_alpha = any(x.isalpha() for x in line)
            checks = [
                line[0].isupper(),
                line.upper() == line and any_alpha,
                any(x.isupper() for x in line[1:]),
                not any(x.isupper() for x in line),
                any_digit,
                any_digit and any_alpha,
                all(x in '0123456789' for x in line),
                all(x in self.is_punct for x in line),
                any(x in self.contains_punct for x in line),
                '-' in line[1:-1],
                is_initial(line),
                re.search(r'http?[:/]', line) or re.search(r'www.', line)
            ]

            presuf = []
            for i in range(1, 4):
                presuf.append(line[:i].lower())
                presuf.append(line[-i:].lower())

            return " ".join(results + bool_to_str(checks) + [str(len(line))] + presuf + bool_to_str(
                [is_first, sentence_all_upper, all_first_upper]))
        else:
            self.first_word = True
            return ""


if __name__ == "__main__":
    FeatVects.main()
