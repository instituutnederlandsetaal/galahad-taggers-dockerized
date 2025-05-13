"""
Ported from lt3_java/preprocessor_java/NER/src/features Java package.
Created on 2016/11/18.

 * Takes the output of the POS tagger and transforms it to input features for
 * the Named Entity Recognizer (NER).
 *
 * Makes NER feature vectors for each token in the output of the CRF++ POS
 * tagger (word in 1st column, POS tag in 2nd column, probability in 3rd column
 * (this last column is not used here))
 * The resulting file is the input for the CRF++ model for named entity recognition
 *
 * Note: numerous features are shared between POS tagging and NER.

"""

import sys
import re

from lets.abstract_step import AbstractStep
from lets.ner_steps import PARSE_DELIM
from lets.lt3_tools.feats import ScannedToken
from lets.lt3_tools.scanutil import ch_isupper, ch_islower, lookup_scan, true_scan


_NER_TAGS = {
    "\"", "$", "'", "(", ")", ",", ".", ":", "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS",
    "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO",
    "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB",
}


def map_pos_ner(pos, language):
    """Maps POS tags to tagset used in the NER training data."""
    if language == "en":
        return pos if pos in _NER_TAGS else 'SYM'

    if language == "nl":
        if "SPEC(deeleigen)" == pos:
            return "NP"
        elif "SPEC(vreemd)" == pos:
            return "FW"
        elif pos.startswith("N(eigen"):
            return "NP"
        else:
            endIdx = pos.find("(")
            return pos[:endIdx if endIdx != -1 else len(pos)] #(pos.substring(0, pos.indexOf("(")))

    elif language == "fr":
        if "ADJ" == pos:
            return "A"
        elif "ADV" == pos:
            return "ADV"
        elif "ABR" == pos:
            return "N"
        elif pos.startswith("DET"):
            return "D"
        elif "INT" == pos:
            return "I"
        elif "KON" == pos:
            return "C"
        elif "NAM" == pos:
            return "NP"
        elif "NOM" == pos:
            return "N"
        elif "NUM" == pos:
            return "CHIF"
        elif pos.startswith("PRO"):
            return "PRO"
        elif pos.startswith("PRP"):
            return "P"
        elif pos.startswith("VER"):
            return "V"
        else:
            return "PONCT"
    else:
        return pos      # German, etc.


class ScannedTokenNER(ScannedToken):
    """A scanned token exposing NER-related features."""

    def __init__(self, token):
        super().__init__(token)
        self._tlength = len(token)
        #: a scan of the internal part of the token (everything but the first char)
        self._internal_flags = lookup_scan(token[1:])

    @property
    def first_capital(self):
        return ch_isupper(self._token[0])

    re_caps = re.compile("^[A-Z]")

    @property
    def all_capitals(self):
        #return self.isupper
        return not bool(self.re_caps.search(self._token))  # hack! mimic the Java impl.

    @property
    def internal_caps(self):
        return self._internal_flags[0]

    @property
    def all_lower_case(self):
        return not self.hasupper and (self.haslower or self.hasdigit or self.haspunct or self.hasother)

    @property
    def contains_digit(self):
        return self.hasdigit

    @property
    def contains_digit_and_alpha(self):
        hasupper, haslower, hasdigit, *_ = true_scan(self._token)
        return hasdigit and (hasupper or haslower)

    @property
    def only_digits(self):
        return self.hasdigit and not(self.hasupper or self.haslower or self.haspunct or self.hasother)

    @property
    def is_punctuation(self):
        hascaret = '^' in self._token  # hack! isPunctuation() regards '^', containsPunctuation() does NOT!
        *alphanum, haspunct, hasother = true_scan(self._token)    # alphanum does not contain hasundersc?
        return (haspunct or hascaret) and not any((*alphanum, (hasother and not hascaret)))

    @property
    def contains_punctuation(self):
        return self.haspunct

    @property
    def is_hyphenated(self):
        if self._tlength < 3:
            return False
        return bool(self._token[1:-1].count("-"))

    re_cap = re.compile("[A-Z]")
    re_no_cap_no_dot = re.compile("[^A-Z\\.]")
    re_cap_or_dot_6 = re.compile("([A-Z](\\.?)){6,}")

    @property
    def is_initial(self):
        """Returns True if the token is an initial of some sort (feature 11)."""
        if not self.hasupper: # self.re_cap.search(self._token):
            return False
        if self._token.find(".") == -1:
            return False
        if self.re_no_cap_no_dot.search(self._token):
            return False
        elif self.re_cap_or_dot_6.search(self._token):
            return False
        return True

    has_http = re.compile("http?[:/]")    # looks like a wrong regexp
    has_www = re.compile("www.")

    @property
    def is_url(self):
        # YD: many more shemas exist: file, ftp, gopher, hdl, http, https, imap, mailto, mms, news, nntp, prospero,
        #     rsync, rtsp, rtspu, sftp, shttp, sip, sips, snews, svn, svn+ssh, telnet, wais
        return bool(self.has_http.search(self._token) or self.has_www.search(self._token))

    @property
    def word_length(self):
        return self._tlength

    @property
    def word_shape(self):
        token = self._token
        hasupper, haslower, hasdigit, haspunct, hasother = \
            self.hasupper, self.haslower, self.hasdigit, self.haspunct, self.hasother

        hasundersc = "_" in token

        if haslower and not any((hasupper, hasdigit, haspunct, hasother)):
            return 'allLowercase'

        if hasdigit:

            if not any((hasupper, haslower, hasundersc)):  # hack! must include also haspunct, hasother
                return 'onlyDigits'
            if hasupper or haslower:
                return 'containsDigitAndAlpha'
            return 'other'

        if ch_isupper(token[0]):
            if not any((haslower, hasdigit, haspunct, hasother)):
                return 'allCaps'

            hasupper_, haslower_, hasdigit_, haspunct_, hasother_ = self._internal_flags
            if haslower_ and not any((hasupper_, hasdigit_, haspunct_, hasother_ )):
                return 'firstCap'
            if token[1] == '.' and len(token) == 2:
                return 'capPeriod'
            if (hasupper_ or haslower_) and not any ((hasdigit_, haspunct_, hasother_)):
                return 'mixedCase'
            if (hasupper_ or haspunct_ or hasother_) and not any((haslower_, hasdigit_, hasundersc)):
                return 'allCapsAndPunct'
            # hasother_ moved; hasundersc added
            if (hasupper_ or haslower_ or haspunct_ or hasother_) and not (hasdigit_ or hasundersc):
                return 'firstCapAlphaAndPunct'
            return 'other'

        if ch_islower(token[0]):
            hasupper_, haslower_, hasdigit_, haspunct_, hasother_ = self._internal_flags  # lookup_scan(token[1:])
            if not hasdigit_:
                return 'alphaAndPunct'

        if (haspunct or hasother) and not any((hasupper, haslower, hasdigit, hasundersc)):
            return 'onlyPunct'

        if (hasupper or haslower) and not any((hasdigit, haspunct, hasother)):
            return 'mixedCase'

        return 'other'

    def prefix(self, n):
        return self._token[:n]

    def suffix(self, n):
        if n == 0:
            return ""
        return self._token[-n:]


class FeatVectProcessor(AbstractStep):
    def __init__(self, l=None):
        super().__init__(l)


    COERCE_MAP = {
        str: lambda x: x,
        int: lambda x: str(x),
        bool: lambda x: str(int(x)),
    }

    @classmethod
    def coerce_fn(cls, obj):
        return cls.COERCE_MAP[type(obj)](obj)

    def _split_line(self, line, errfile=sys.stderr):
        """Returns a three-element tuple (first_flag, token, pos) after splitting this line
        into `first_flag` and the rest, then trying to split the rest into three fields of which
        the first two are token and POS. On error returns: (None, None, error-message).
        """
        try:
            first_flag, theline = line.split(PARSE_DELIM, 1)
            token, pos, *_ = theline.split()
            return first_flag, token, pos
        except ValueError as err:
            class_name = self.__class__.__name__
            msg = "cannot process line {!r}: {}".format(line, err)
            print("{}: {}".format(class_name, msg), file=errfile)
            return None, None, "!!ERROR: {}".format(msg)

    def process_line(self, line):
        first_flag, token, pos = self._split_line(line)
        if first_flag is None and token is None:
            yield pos  # which would be the error message
        else:
            stoken = ScannedTokenNER(token)
            flags_sequence = (
                token,
                map_pos_ner(pos, self.language),
                stoken.first_capital,
                stoken.all_capitals,
                stoken.internal_caps,
                stoken.all_lower_case,
                stoken.contains_digit,
                stoken.contains_digit_and_alpha,
                stoken.only_digits,
                stoken.is_punctuation,
                stoken.contains_punctuation,
                stoken.is_hyphenated,
                stoken.is_initial,
                stoken.is_url,
                stoken.word_length,
                stoken.prefix(3),
                stoken.suffix(3),
                stoken.prefix(4),
                stoken.suffix(4),
                stoken.word_shape,
                first_flag,  # first_flag is one of ("0", "1")
            )
            yield " ".join(map(self.coerce_fn, flags_sequence))

    def process_lines(self, lines):
        is_first = True
        for line in lines:
            if not line.strip():
                yield ""
                is_first = True
            else:
                # packing an `is_first` flag with/into the line:
                extended_line = "{}{}{}".format(int(is_first), PARSE_DELIM, line)
                for out_item in self.process_line(extended_line):
                    yield out_item
                is_first = False
        yield ""


if __name__ == '__main__':
     FeatVectProcessor.main()
