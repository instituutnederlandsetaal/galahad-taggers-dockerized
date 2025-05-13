"""
Created: 2016/10/26
Simple container classes ported from lt3 domein java package

"""

from lets.chunker_steps.jcompat import JList


class Word(object):
    """A word properties container containing monolingual information.
       (In more detail, this is word form (= token), lemma and PoS
       information.)
    """
    __slots__ = ('_position', '_token', '_lemma', '_pos', '_mapped_pos', '_phr', '_morph_ana', '_language')

    def __init__(self, nr, token, lemma, pos, mapped_pos, morph_ana, lang):
        """
        :param nr: int - word number in the sentence
        :param token: string - word number in the sentence
        :param lemma: string - word lemma
        :param pos: string - part-of-speech information
        :param mapped_pos: string - mapped part-of-speech information
        :param morph_ana: string - moprphological analysis
        :param language: string - two-byte language code

        """
        self._position = nr             # int - _position in the sentence
        self._token = token
        self._lemma = lemma
        self._pos = pos                 # string - PoS code (Penn reebank tag set or CGN tag set)
        self._mapped_pos = mapped_pos   # string - mapped PoS codes
        self._phr = None                # string - IOB-phrase types
        self._morph_ana = morph_ana     # string - Morphological analysis
        self._language = lang           # string - language of the sentence

    def __str__(self):
        return "%s %s[%s][%s][%s](%s)\n" % (self._position, self._token, self._lemma, self._pos, self._mapped_pos, self._phr)

    def __repr__(self):
        return "Word(nr=%r, token=%r, lemma=%r, pos=%r, mapped_pos=%r) at 0x%016Xd" \
                % (self._position, self._token, self._lemma, self._pos, self._mapped_pos, id(self))

    def tab_delimited(self):
        return "\t".join((self._token, self._lemma, self._pos, self._phr))

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos

    def setMappedPos(self, pos):
        self._mapped_pos = pos

    def getMappedPos(self):
        return self._mapped_pos

    def getLemma(self):
        return self._lemma

    def setLemma(self, lemma):
        self._lemma = lemma

    def getToken(self):
        return self._token

    def setToken(self, token):
        self._token = token

    def setPosition(self, nr):
        self._position = nr

    def getPosition(self):
        return self._position

    def getLanguage(self):
        return self._language

    def setPhr(self, phr):
        self._phr = phr

    def getPhr(self):
        return self._phr

    def setMorphAna(self, ana):
        self._morph_ana = ana

    def getMorphAna(self):
        return self._morph_ana


class Chunk(object):
    """A chunk of words container."""

    DEFAULT_TYPE = "O"

    def __init__(self, position, sublist, start_idx, end_idx):
        self._chunk = JList(sublist)
        self._start_idx = start_idx
        self._end_idx = end_idx
        self._position = position           # also known as id
        self._tokens = None
        self._mapped_pos_seq = None
        self._set_mapped_pos_sequence()
        self._set_tokens()
        self._type = self.DEFAULT_TYPE

    def __str__(self):
        result = "{:d} {:d}-{:d} {} ".format(self._position, self._start_idx, self._end_idx, self._type)
        for w in self._chunk:
            result += "{} ".format(w._token)
        result += self._mapped_pos_seq
        return result

    __repr__ = __str__

    def _set_tokens(self):
        seq = ""
        prevword_idx = -1
        for word in self._chunk:
            if (prevword_idx > -1) and (word.getPosition() - prevword_idx) > 1:
                seq += "..."
            if not seq:
                seq = word.getToken()
            else:
                seq = "{} {}".format(seq, word.getToken())
            prevword_idx = word.getPosition()
        self._tokens = seq

    def _set_mapped_pos_sequence(self):
        seq = ""
        prevword_idx = -1
        for word in self._chunk:
            if (prevword_idx > -1) and (word.getPosition() - prevword_idx) > 1:
                seq += "..."
            if not seq:
                seq = word.getMappedPos()
            else:
                seq = "{}+{}".format(seq, word.getMappedPos())
            prevword_idx = word.getPosition()
        self._mapped_pos_seq = seq

    def getMappedPosSequence(self):     # need NOT be an attribute
        return self._mapped_pos_seq

    def getPosition(self):
        return self._position

    def getChunk(self):
        return self._chunk

    def getType(self):
        return self._type

    def setType(self, type_):
        self._type = type_

    def getTokens(self):
        return self._tokens

    def getStartIdx(self):
        return self._start_idx

    def getEndIdx(self):
        return self._end_idx
