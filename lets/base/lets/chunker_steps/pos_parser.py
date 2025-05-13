"""
Generator-based Reimplementation of the POSParser and LEMParser
from lt3_java/preprocessor_java/Chunker/src/domein Java package.

Created on 2016/10/28

"""

import logging

log = logging.getLogger(__name__)

from lets.chunker_steps.pos_maps import *
from lets.chunker_steps.chunker_util import matches
from lets.chunker_steps import PARSE_DELIM as DELIM
from lets.abstract_step import AbstractStep
from lets.chunker_steps.error import InvalidInputError


class POSParser(AbstractStep):
    """A processor of POS text line sequences."""
    def __init__(self, l=None):
        super().__init__(l)
        self.language = l


    pos_map_en = fill_pos_maps_english()
    pos_map_fr = fill_pos_maps_french()
    pos_map_de = fill_pos_maps_german()

    def _correct_english(self, token, lemma, pos):
        if pos == "IN/that":
            pos = "WDT"
        elif pos == "VH":
            pos = "VB"
        elif pos == "VHD":
            pos = "VBD"
        elif pos == "VHG":
            pos = "VBG"
        elif pos == "VHN":
            pos = "VBN"
        elif pos == "VHP":
            pos = "VBP"
        elif pos == "VHZ":
            pos = "VBZ"
        elif token == "console":
            lemma = "console"
            pos = "NN"
        elif matches("shaft[s]?", token):
            pos = "NN"
        elif token == "warning":
            lemma = "warning"
            pos = "NN"
        elif token == "steering":
            lemma = "steering"
            pos = "JJ"
        elif token == "hinged":
            lemma = "hinged"
            pos = "JJ"
        elif token == "control":
            lemma = "control"
            pos = "NN"
        elif token == "controls":
            lemma = "control"
            pos = "NN"
        return token, lemma, pos

    def _correct_french(self, token, lemma, pos):
        assert self.language == "fr"
        if token == "droit":
            lemma = "droit"
            pos = "ADJ"
        return token, lemma, pos

    def map_pos_nl(self, pos):
        mappedPos = pos
        if mappedPos.startswith("VG(neven"):
            mappedPos = "CONJ-coord"
        elif mappedPos.startswith("VG(onder"):
            mappedPos = "CONJ-subord"
        elif mappedPos.startswith("LET"):
            mappedPos = "PCT"
        elif mappedPos.startswith("LID"):
            mappedPos = "DET"
        elif mappedPos.startswith("VZ"):
            mappedPos = "PREP"
        elif mappedPos.startswith("ADJ(nom,"):
            mappedPos = "N"
        elif mappedPos.startswith("ADJ"):
            mappedPos = "ADJ"
        elif mappedPos.startswith("WW(vd,prenom"):
            mappedPos = "ADJ"
        elif mappedPos.startswith("WW(od,prenom"):
            mappedPos = "ADJ"
        elif mappedPos.startswith("WW(vd,nom"):
            mappedPos = "N"
        elif mappedPos.startswith("WW(od,nom"):
            mappedPos = "N"
        elif mappedPos.startswith("TW(rang,prenom"):
            mappedPos = "ADJ"
        elif mappedPos.startswith("TW(hoofd,prenom"):
            mappedPos = "ADJ"
        elif mappedPos.startswith("TW(rang,nom"):
            mappedPos = "N"
        elif mappedPos.startswith("TW(hoofd,nom"):
            mappedPos = "N"
        elif mappedPos.startswith("TW(hoofd"):
            mappedPos = "NUM"
        elif mappedPos.startswith("TW(rang"):
            mappedPos = "NUM"
        elif mappedPos.startswith("N") and ",gen" in mappedPos:
            mappedPos = "N-gen"
        elif mappedPos.startswith("N(soort"):
            mappedPos = "N"
        elif mappedPos.startswith("N(eigen"):
            mappedPos = "N-prop"
        elif mappedPos.startswith("VNW(pers"):
            mappedPos = "PRON-per"
        elif mappedPos.startswith("VNW(bez"):
            mappedPos = "PRON-pos"
        elif mappedPos.startswith("VNW(onbep"):
            mappedPos = "PRON-ind"
        elif mappedPos.startswith("VNW(aanw"):
            mappedPos = "PRON-dem"
        elif mappedPos.startswith("VNW(betr"):
            mappedPos = "PRON-rel"
        elif mappedPos.startswith("VNW(vb"):
            mappedPos = "PRON-int"
        elif mappedPos.startswith("VNW"):
            mappedPos = "PRON"
        elif mappedPos.startswith("BW"):
            mappedPos = "ADV"
        elif mappedPos.startswith("SPEC(vreemd"):
            mappedPos = "FW"
        elif mappedPos.startswith("SPEC(symb"):
            mappedPos = "SYM"
        elif mappedPos.startswith("SPEC(deeleigen"):
            mappedPos = "N-prop"
        elif mappedPos.startswith("SPEC"):
            mappedPos = "PCT"
        elif mappedPos.startswith("TSW"):
            mappedPos = "INT"
        elif mappedPos.startswith("WW(inf"):
            mappedPos = "V-inf"
        elif mappedPos.startswith("WW(pv"):
            mappedPos = "V-fin"
        elif mappedPos.startswith("WW(od"):
            mappedPos = "V-prpa"
        elif mappedPos.startswith("WW(vd"):
            mappedPos = "V-papa"
        return mappedPos

    def _map_pos_correct(self, pos):
        """Returns mapped pos corresponding to given pos."""
        mapped = pos
        if self.language == 'nl':
            mapped = self.map_pos_nl(pos)
        elif self.language == 'en':
            if self.pos_map_en.containsKey(pos):
                mapped = self.pos_map_en.get(pos)
        elif self.language == 'fr':
            if self.pos_map_fr.containsKey(pos):
                mapped = self.pos_map_fr.get(pos)
        elif self.language == 'de':
            if self.pos_map_de.containsKey(pos):
                mapped = self.pos_map_de.get(pos)
        return mapped

    def _map_pos_emulating_java_bug(self, pos):
        """Returns mapped pos corresponding to given pos, INCORRECTLY simulating
           the Java switch statement bug."""
        mapped = pos
        if self.language == 'nl':
            mapped = self.map_pos_nl(pos)
            if self.pos_map_en.containsKey(pos):
                mapped = self.pos_map_en.get(pos)
            if self.pos_map_fr.containsKey(pos):
                mapped = self.pos_map_fr.get(pos)
            if self.pos_map_de.containsKey(pos):
                mapped = self.pos_map_de.get(pos)

        elif self.language == 'en':
            if self.pos_map_en.containsKey(pos):
                mapped = self.pos_map_en.get(pos)
            if self.pos_map_fr.containsKey(pos):
                mapped = self.pos_map_fr.get(pos)
            if self.pos_map_de.containsKey(pos):
                mapped = self.pos_map_de.get(pos)

        elif self.language == 'fr':
            if self.pos_map_fr.containsKey(pos):
                mapped = self.pos_map_fr.get(pos)
            if self.pos_map_de.containsKey(pos):
                mapped = self.pos_map_de.get(pos)

        elif self.language == 'it':
            if self.pos_map_de.containsKey(pos):
                mapped = self.pos_map_de.get(pos)

        elif self.language == 'de':
            if self.pos_map_de.containsKey(pos):
                mapped = self.pos_map_de.get(pos)

        return mapped

    # FIXME: revert to the correct map_pos impl. (now doing this breaks acceptance tests)
    # _map_pos = _map_pos_correct
    _map_pos = _map_pos_emulating_java_bug

    def _pre_process(self, line):
        """Splits the input line and does some sanity checking. (See
           POSParser.process_line() for details.)"""
        record = line.split()
        if not record:  # we allow empty lines
            return None
        if len(record) not in (2, 3):  # we reject wrong number of fields
            raise InvalidInputError("POS file contains invalid entry: {!r}".format(line))
        return record

    def process_line(self, line):
        """Processes an input line [ TODO: what exactly? ] and yields a TAB-delimited
           joint text line of form "{token}\t{lemma}\t{pos}\t{pos_mapped}" from given
           line which is as outputed by the POS step. Yields an empty string if input
           line is empty."""
        record = self._pre_process(line)
        if record is None:
            yield ""
        else:
            token, pos = record[0:2]
            lemma = ""
            if self.language == 'en':
                token, lemma, pos = self._correct_english(token, lemma, pos)
            elif self.language == 'fr':
                token, lemma, pos = self._correct_french(token, lemma, pos)
            pos_mapped = self._map_pos(pos)
            yield DELIM.join((token, lemma, pos, pos_mapped))


if __name__ == "__main__":
    POSParser.main()
