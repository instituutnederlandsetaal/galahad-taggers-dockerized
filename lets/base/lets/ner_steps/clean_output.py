"""
Ported from lt3_java/preprocessor_java/NER/src/ner Java package.
Created: 2016/11/18.

"""

from lets.abstract_step import AbstractStep


class CleanOutput(AbstractStep):
    """
    A cleanup step that reads the output of the CRF based Named Entity Recognizer
    and generates a clean output file (containing only the word, NER tag and its
    probability).
    """
    def __init__(self, l=None):
        super().__init__(l)


    def process_line(self, line):
        raise NotImplementedError("process_line() not used in CleanOutput")

    def process_lines(self, lines):
        written = False
        previous_tag = ""
        previous_type = ""
        current_tag = ""
        current_type = ""
        output_label = ""

        for line in lines:
            if not line.strip():
                if written:
                    yield ""
                written = False
                continue

            # else:
            s = line.split()
            if len(s) < 3:
                continue

            word = s[0]
            s = s[-1].split("/")

            if len(s) != 2:
                print("ERROR --- CleanOutputOld: invalid TAG for line {!r}".format(line))
                continue

            dash_idx = s[0].find('-')
            if dash_idx != -1:
                current_tag = s[0][:dash_idx]  # s[0].substring(0, s[0].indexOf("-"))
                current_type = s[0][dash_idx+1:]  # s[0].substring(s[0].indexOf("-") + 1, len(s[0]))
            else:
                current_tag = "0"
                current_type = "NoType"

            if current_tag == "0":
                output_label = s[0]

            elif current_tag == "B":
                output_label = s[0]

            else:
                if previous_tag == "":
                    output_label = "B-" + current_type
                elif previous_tag == "0":
                    output_label = "B-" + current_type
                elif previous_tag == "B":
                    if previous_type == current_type:
                        output_label = s[0]
                    else:
                        output_label = "B-" + current_type
                else:
                    if previous_type == current_type:
                        output_label = s[0]
                    else:
                        output_label = "B-" + current_type
            previous_tag = current_tag
            previous_type = current_type
            yield word + " " + output_label + " " + s[1]
            written = True


if __name__ == '__main__':
    CleanOutput.main()
