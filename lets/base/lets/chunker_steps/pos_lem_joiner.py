"""
Generator-based Reimplementation of the POSParser and LEMParser
from lt3_java/preprocessor_java/Chunker/src/domein Java package.

Created on 2016/10/28

"""

import logging

log = logging.getLogger(__name__)

from lets.chunker_steps import PARSE_DELIM as DELIM
from lets.abstract_step import DualInputStep
from lets.chunker_steps.error import InvalidInputError


class POSLEMJoiner(DualInputStep):
    """A processor that joins POS + LEM input sequences to produce combined output."""

    def __init__(self, l=None):
        super().__init__(l)

    def process_dual_line(self, lem_line, pos_line):
        """Yields a joint POS + LEM token attribute line build out of the two given synchronized
           sequences of input lines. lem_line and pos_line are text lines as outputed by LEMParser
           and POSParser respectively. Yields an empty string if both input lines are empty. Raises
           InvalidInputError if the two lines are not in synch. (Currently only checking if both are
           empty at the same time.)"""
        # We allow either both present or both not:
        if bool(lem_line) != bool(pos_line):
            raise InvalidInputError("LEM and POS sequences not in synch:"
                                    " lem={!r}, pos={!r}".format(lem_line, pos_line))
        if not lem_line.strip():  # means both lines are empty
            yield ""
        else:
            token, lemma, pos, pos_mapped = pos_line.strip().split(DELIM)
            if lemma == "":
                lemma = lem_line.strip().split()[0]  # lemma is first element from LEMParser record:
            if lemma == "<unknown>":
                lemma = token
            yield DELIM.join((token, lemma, pos, pos_mapped))


if __name__ == "__main__":
    POSLEMJoiner.main()
