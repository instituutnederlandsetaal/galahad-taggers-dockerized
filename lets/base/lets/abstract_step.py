import sys
import argparse
from abc import ABC


class AbstractStep(ABC):
    def __init__(self, language='nl'):
        self.language = language

    def process_lines(self, lines):
        """Processes a list of lines

        Args:
            lines: iterator of strings, each representing a line
        Returns:
            iterator of strings, containing the processed lines
        """
        for line in lines:
            for out_item in self.process_line(line):
                yield out_item
        for out_item in self.process_line(''):
            yield out_item

    def process_line(self, line):
        raise NotImplementedError

    def process_file(self, f_in, f_out):
        """Processes a file
        Args:
            f_in: python file object containing input
            f_out: python file object where output will be written
        """
        for l in self.process_lines(f_in):
            f_out.write(l + '\n')

    def process_file_by_name(self, f_in_name, f_out_name):
        """Processes a file
        Args:
            f_in_name: full name of input file
            f_out_name: full name of output file
        """
        with open(f_in_name, 'r') as f_in, open(f_out_name, 'w') as f_out:
            self.process_file(f_in, f_out)

    @classmethod
    def add_arguments(cls, parser):
        return parser

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(description=cls.__name__)
        parser.add_argument("l", help="language", choices=["de", "en", "fr", "nl"])
        parser.add_argument('i', help="input file name", type=argparse.FileType('r', encoding='UTF-8'))
        parser.add_argument('o', help="output file name", type=argparse.FileType('w', encoding='UTF-8'))
        parser = cls.add_arguments(parser)

        args = parser.parse_args()
        i = args.i
        o = args.o
        optional_args = vars(args)
        del optional_args['i']
        del optional_args['o']
        cls(**optional_args).process_file(i, o)


class DualInputStep(ABC):
    """An abstract parent for dual input line processing steps."""

    def __init__(self, language='nl'):
        self.language = language

    def process_dual_line(self, line_one, line_two):
        raise NotImplementedError

    def process_dual_lines(self, lines_one, lines_two):
        """Processes two iterators of input lines. Expects (and may check)
           that the two line sequences are in synch with each other.

           Args: lines_one, lines_two: iterators of strings, each representing a line
           Returns: iterator of strings, containing the processed lines
        """
        for line_one, line_two in zip(lines_one, lines_two):
            for out_line in self.process_dual_line(line_one, line_two):
                yield out_line
        for out_line in self.process_dual_line("", ""):
            yield out_line

    def process_files(self, f_in_one, f_in_two, f_out):
        """Processes input file objects.

        Args:
            f_in_one, f_in_two: python file object containing input
            f_out: python file object where output will be written
        """
        for f_out_line in self.process_dual_lines(f_in_one, f_in_two):
            f_out.write(f_out_line + '\n')

    def process_files_by_name(self, f_in_name_one, f_in_name_two, f_out_name):
        """Processes input file names.

        Args:
            f_in_name_one, f_in_name_two: full name of the two input files
            f_out_name: full name of output file
        """
        with open(f_out_name, 'w') as f_out, \
                open(f_in_name_one, 'r') as f_in_one, \
                open(f_in_name_two, 'r') as f_in_two:
            self.process_files(f_in_one, f_in_two, f_out)

    @classmethod
    def add_arguments(cls, parser):
        """Add non-standard arguments. (Defaults to doing nothing, override
           in subclasses.)"""
        return parser

    @classmethod
    def _parse_args(cls, argv):
        parser = argparse.ArgumentParser(description=cls.__name__)
        parser.add_argument("l", help="language", choices=["de", "en", "fr", "nl"])
        parser.add_argument('f', help="first input file name", type=argparse.FileType('r'))
        parser.add_argument('s', help="second input file name", type=argparse.FileType('r'))
        parser.add_argument('o', help="output file name", type=argparse.FileType('w'))
        parser = cls.add_arguments(parser)
        return parser.parse_args(argv)

    @classmethod
    def main(cls, argv=None):
        parser = argparse.ArgumentParser(description=cls.__name__)
        parser.add_argument("l", help="language", choices=["de", "en", "fr", "nl"])
        parser.add_argument('f', help="first input file name", type=argparse.FileType('r'))
        parser.add_argument('s', help="second input file name", type=argparse.FileType('r'))
        parser.add_argument('o', help="output file name", type=argparse.FileType('w'))
        parser = cls.add_arguments(parser)

        args = parser.parse_args()
        in_first = args.f
        in_second = args.s
        f_out = args.o
        optional_args = vars(args)
        del optional_args['f']
        del optional_args['s']
        del optional_args['o']
        cls(**optional_args).process_files(in_first, in_second, f_out)
