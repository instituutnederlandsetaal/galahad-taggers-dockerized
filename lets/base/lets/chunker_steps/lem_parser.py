"""
Generator-based Reimplementation of the POSParser and LEMParser
from lt3_java/preprocessor_java/Chunker/src/domein Java package.

Created on 2016/10/28

"""

import logging

log = logging.getLogger(__name__)

from lets.chunker_steps import PARSE_DELIM as DELIM
from lets.abstract_step import AbstractStep
from lets.chunker_steps.error import InvalidInputError


class LEMParser(AbstractStep):
    """A processor of lemma text line sequences."""

    def __init__(self, l=None):
        super().__init__(l)

    def _pre_process(self, line):
        record = line.split()
        if not record:  # we allow empty lines
            return None
        if len(record) not in (3, 4):  # we reject wrong number of fields
            raise InvalidInputError("LEM file contains invalid entry: {!r}".format(line))
        return record

    def process_line(self, line):
        """Accepts a record list of three or four items: [ TODO: what are they exactly? ]
           Yields a line of two space-separated elements "{lemma} {prob}"."""
        record = self._pre_process(line)
        if record is None:
            yield ""
        else:
            yield DELIM.join(tuple(record[1:3]))


if __name__ == "__main__":
    LEMParser.main()
