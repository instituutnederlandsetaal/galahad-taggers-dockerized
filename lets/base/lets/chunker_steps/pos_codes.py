"""
Ported from lt3_java/preprocessor_java/Chunker/src/domein Java package.
Created on 2016/10/28

"""

from lets.chunker_steps.jcompat import HashSet


class PoSCodes(object):
    ENGLISH_CONTENT_WORDS = HashSet(("CD", "EX", "FW", "JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS", "RB", "RBR", "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP"))
    ENGLISH_FW_WORDS = HashSet(("CC", "DT", "IN", "MD", "PDT", "PRP", "PRP$", "TO", "WDT", "WP", "WP$", "WRB"))
    ENGLISH_PUNCT = HashSet(("(", ")", ",", ".", ":", "LS", "''", "\""))
    ENGLISH_SUBORD = HashSet(("if", "as", "that", "whether", "while", "although", "because", "so", "unless"))
    DUTCH_CONTENT_WORDS = HashSet(("N", "ADJ", "WW", "TW", "BW"))
    DUTCH_FW_WORDS = HashSet(("VNW", "LID", "VZ", "VG"))
    DUTCH_PUNCT = HashSet(("(", ")", ".", ",", "<", ">", "?", ";", ":", "-", "--", "!", "'", "`", "\""))
    DUTCH_PART = HashSet(("nu", "nou", "toch", "ook", "eens", "even", "maar", "wel", "dan"))
    DUTCH_ZINSBIJW = HashSet(("misschien", "wellicht", "allicht", "weliswaar", "inderdaad", "bovendien", "daarenboven", "eveneens", "evenmin", "tevens", "zelfs", "desalniettemin", "desondanks", "nochtans", "bijgevolg", "derhalve", "deswege", "dus", "dientengevolge", "althans", "immers", "overigens", "trouwens", "echter", "eindelijk", "allemaal", "reeds", "voorheen", "momenteel", "thans", "onlangs"))
    DET_PREP_CONJ_PCT_PRONPOS = HashSet(("DET", "PREP", "CONJ", "CONJ-coord", "CONJ-subord", "PCT", "PRON-pos", "TO"))
    DET_PREP = HashSet(("DET", "PREP", "PREP-det", "PRON-pos"))
    PRONOUNS = HashSet(("PRON-dem", "PRON-ind", "PRON-per", "PRON-pos", "PRON-rel"))

    @classmethod
    def matchPoS(cls, pos1, pos2):
        """Checks whether two PoS codes match."""
        match = False
        if pos1 == pos2:
            return True
        elif pos1.startsWith("N") and pos2.startsWith("N"):
            return True
        elif pos1.startsWith("V-fin") and pos2.startsWith("V-fin"):
            return True
        elif pos1.startsWith("CONJ") and pos2.startsWith("CONJ"):
            return True
        elif pos1 == "DET" and (pos2 == "PRON-ind" or pos2 == "PRON-dem"):
            return True
        elif pos2 == "DET" and (pos1 == "PRON-ind" or pos1 == "PRON-dem"):
            return True
        elif pos1 == "TO" and pos2 == "PREP":
            return True
        elif pos2 == "TO" and pos1 == "PREP":
            return True
        else:
            pass
        return match

    @classmethod
    def incompatiblePoS(cls, pos1, pos2):
        if pos1.startsWith("V") and pos2.startsWith("PRON"):
            return True
        if pos2.startsWith("V") and pos1.startsWith("PRON"):
            return True
        else:
            return False

    @classmethod
    def mainCategory(cls, posCode):
        """Return only main Pos Code for nouns and verbs."""
        if posCode.startsWith("N-gen"):
            return "N-gen"
        elif posCode.startsWith("N-"):
            return "N"
        elif posCode.startsWith("WW-pv"):
            return "WW"
        elif posCode.startsWith("WW-inf"):
            return "WW"
        else:
            return posCode
