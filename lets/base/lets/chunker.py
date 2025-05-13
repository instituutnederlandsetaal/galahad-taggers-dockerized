import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from lets.abstract_step import DualInputStep
from lets.chunker_steps.pos_lem_joiner import POSLEMJoiner
from lets.chunker_steps.lem_parser import LEMParser
from lets.chunker_steps.pos_parser import POSParser
from lets.chunker_steps.sentence import SentenceProcessor


class Chunker(DualInputStep):
    """Chunker generation step class."""

    def __init__(self, l='nl'):
        DualInputStep.__init__(self, language=l)
        self.lem_parser = LEMParser(l)
        self.pos_parser = POSParser(l)
        self.pos_lem_joiner = POSLEMJoiner(l)
        self.sentence_processor = SentenceProcessor(l)

    def process_dual_line(self, line_one, line_two):
        raise NotImplementedError("process_dual_line() not used in Chunker")

    def process_files(self, lem_file, pos_file, out_file):  # explicitly name the input files args
        super().process_files(lem_file, pos_file, out_file)

    def process_files_by_name(self, lem_file_name, pos_file_name, out_file_name):  # explicitly name input files args
        super().process_files_by_name(lem_file_name, pos_file_name, out_file_name)

    def process_dual_lines(self, lem_lines, pos_lines):
        chunk_gen = self.sentence_processor.process_lines(
            self.pos_lem_joiner.process_dual_lines(
                self.lem_parser.process_lines(lem_lines),
                self.pos_parser.process_lines(pos_lines)))
        return chunk_gen


if __name__ == "__main__":
    Chunker.main()
