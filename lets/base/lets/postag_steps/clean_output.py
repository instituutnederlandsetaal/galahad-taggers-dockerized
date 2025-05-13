from lets.abstract_step import AbstractStep
import re


class CleanOutput(AbstractStep):
    def __init__(self, l):
        super().__init__()
        self.written = False

    def process_line(self, line):
        words = re.split(r"[ \t]", line.strip())
        if len(words) == 25:
            splits = words[-1].split("/")
            self.written = True
            yield " ".join([words[0], splits[0], splits[1]])
        else:
            if self.written:
                self.written = False
                yield line.strip()


if __name__ == "__main__":
    CleanOutput.main()
