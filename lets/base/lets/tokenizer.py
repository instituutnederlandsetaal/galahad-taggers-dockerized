import re
import os
import sys
import codecs

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from lets.abstract_step import AbstractStep


def split_sgml(word):
    found = True
    while found:
        m = re.match(r'^([^<>]*)(<\/?([^<>]+)>)(.*)$', word)
        if m:
            word = m.group(1) + m.group(4)
        else:
            found = False

    return word


class Tokenizer(AbstractStep):
    """
    Args:
        l: language
        r: newline switch (boolean)
        e: sentence newline switch (boolean)
    """

    def __init__(self, l, r=True, e=True):
        super().__init__()
        language = l
        with open(os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/suffixes'.format(language)) as f:
            self.suffixes = dict(l.split() for l in f if not l.startswith("#"))
            suffixes = [len(k) for k in self.suffixes.keys()]
            self.suffixes_max_length = max(suffixes)
            self.suffixes_min_length = min(suffixes)
        with open(os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/prefixes'.format(language)) as f:
            self.prefixes = dict(l.split() for l in f if not l.startswith("#"))
            prefixes = [len(k) for k in self.prefixes.keys()]
            self.prefixes_max_length = max(prefixes) if prefixes else 0
            self.prefixes_min_length = min(prefixes) if prefixes else 0
        self.abbreviations = self.read_file(
            os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/abbr'.format(language))
        self.apostrof = self.read_file(
            os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/apostrof'.format(language))
        self.ordinals = self.read_file(
            os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/ordinals'.format(language))
        self.coord = self.read_file(
            os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/coord'.format(language))
        self.nosplit = self.read_file(
            os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/nosplit'.format(language))
        self.measures = self.read_file(
            os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/general/measure')
        self.moneys = self.read_file(os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/general/money')
        with open(os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/{}/special_words'.format(language),
                  'r') as f:
            lines = [l.strip().split() for l in f if not l.startswith("#")]
            self.special_words1 = dict(l for l in lines if len(l) == 2)
            self.special_words2 = {l[0]: (l[1], l[2]) for l in lines if len(l) == 3}
        self.uc_alpha = 'A-Z'
        self.lc_alpha = 'a-z'
        self.lc_alpha_special = ''
        with codecs.open(os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/general/sgml.ent.alpha', 'r',
                         'iso-8859-1') as f:
            lines = [l.strip().split() for l in f if not l.startswith("#")]
            for l in lines:
                if len(l) == 3:
                    if l[0][0].isupper():
                        self.uc_alpha += l[1]
                    else:
                        self.lc_alpha += l[1]
                        self.lc_alpha_special += l[1]
            self.user_defined_tags = {l[0]: l[1] for l in lines if len(l) == 2}
        with codecs.open(os.path.dirname(os.path.realpath(__file__)) + '/models/tokenizer/general/sgml.ent.nonalpha',
                         'r', 'iso-8859-1') as f:
            lines = [l.strip().split('\t') for l in f if not l.startswith("#")]
            self.predefined_tags = {l[0]: l[1] if len(l) > 1 else '' for l in lines}
        self.r = r
        self.e = "" if e else None

        self.last_line = None
        self.last_hyphened = None

        # Tokenizer variables
        # Replace certain unicode character(s) to another value
        #
        # Format: (character_regex, replacement_character)
        #
        # To completely remove a character, use "" as replacement
        self.replace_character_map = [
            ("“", ""),  # left double quotation mark -> remove
            ("”", ""),  # right double quotation mark -> remove
            ('"', ""),  # straight double quotation mark -> remove
            ("„", ""),  # left lower quotation mark -> remove
            ("«", "« "), # Ensure space after 'left-pointing double angle quotation mark', before word
            ("»", " »"),  # Ensure space after word, before 'right-pointing double angle quotation mark'
            ('\u2018', "'"),  # Left Single Quotation Mark -> Apostrophe
            ('\u2019', "'"),  # Right Single Quotation Mark -> Apostrophe
        ]

    @staticmethod
    def read_file(file_name):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            return [l.strip() for l in f if not l.startswith("#")]

    def clean_and_tokenize_line(self, line):
        for char, replacement in self.replace_character_map:
            line = re.sub(char, replacement, line)

        return line.strip().split()

    def process_line(self, line):
        words2 = []
        hyphened = None
        words = line.strip().split()
        words = self.clean_and_tokenize_line(line)
        while len(words) > 0:
            word = words.pop(0)

            # print('word', word, words, lines)
            add_end_utt = False
            prefixes = []
            suffixes = []

            if not re.match(r'^[' + self.lc_alpha + self.uc_alpha + 'r]+$', word) and word not in self.nosplit:
                word = self.replace_sgml_entities(word)
                word = split_sgml(word)
                word = self.missing_space(word, words)
                word = self.special_characters(word, words)
                word = self.punct_at_beginning(word, prefixes)
                add_end_utt, hyphened, word = self.punct_at_end(word, words, suffixes, add_end_utt)
                word = self.apply_files(word, prefixes, suffixes)
            self.special_words(word, words, prefixes, suffixes, words2, 0, [], hyphened, add_end_utt)

        self.check_hyphen(words2, self.last_line, self.last_hyphened)

        if line.strip() == '' and self.last_line and self.last_line[-1] != self.e:
            self.last_line.append(self.e)

        self.last_hyphened = hyphened

        result = self.last_line if self.last_line else []
        if self.last_line is not None:
            if self.r:
                result.append('')
        self.last_line = None if words2 == [] else words2
        return result

    def special_words(self, word, words, prefixes, suffixes, words2, line_index, lines, hyphened, add_end_utt):
        if word in self.special_words1:
            word = self.special_words1[word]
        if word in self.special_words2:
            suffixes.insert(0, self.special_words2[word][1])
            word = self.special_words2[word][0]
        # if not words and hyphened and len(lines) == line_index + 1 :
        #     word = hyphened + ' -'
        words2.extend(prefixes)
        if word:
            words2.append(word)
        words2.extend(suffixes)
        if add_end_utt and self.e is not None:
            words2.append(self.e)

    def apply_files(self, word, prefixes, suffixes):

        # check suffixes
        for i in range(self.suffixes_min_length, min(self.suffixes_max_length, len(word)) + 1):
            if word[-i:].lower() in self.suffixes:
                suffixes.insert(0, word[-i:])
                word = word[:-i]
                break
        # check prefixes
        for i in range(self.prefixes_min_length, min(self.prefixes_max_length, len(word)) + 1):
            if word[:i].lower() in self.prefixes:
                prefixes.append(word[:i])
                word = word[i:]
                break

        # split f5,-   hfl50   DM0,50   BEF7,50
        m = re.match(r'^([a-zA-Z]+)(\.*)([0-9][-=0-9.,]+)$', word)
        if m and m.group(1) in self.moneys:
            prefixes.append(m.group(1) + m.group(2))
            word = m.group(3)
        else:
            m = re.match(r'^([a-zA-Z]+)(\.*)([-=0-9.,]+[0-9])$', word)
            if m and m.group(1) in self.moneys:
                prefixes.append(m.group(1) + m.group(2))
                word = m.group(3)

        # split 180C  350F  12oz  375g  2.5cm  450-900g  1-2lb  170,500km  etc.
        m = re.match(r'^([-0-9.,]+)([' + self.lc_alpha + self.uc_alpha + r']+)$', word)
        if m is not None:
            if m.group(2) in self.measures or m.group(2) in self.moneys:
                suffixes.insert(0, m.group(2))
                word = m.group(1)

        # split 450-900 etc.
        m = re.match(r'^(\'?[0-9.,]+)(-+)(\'?[0-9.,]+([.,]-)?)$', word)
        if m is not None:
            suffixes.insert(0, m.group(3))
            suffixes.insert(0, m.group(2))
            word = m.group(1)

        return word

    def punct_at_end(self, word, words, suffixes, add_end_utt):
        hyphened = None
        found = True
        while found:
            if word in [".", "!", "?", "...", "…"]:
                found = False
                add_end_utt = True
            else:
                m = re.match(r'^(.+?)([#"(){}\[\]!?:;@\$%^&*+|=~<>\/\\_…]|\.+|,+|-+|`+|\'+|\.-|,-|\.=|,=)$',
                             word)
                if m is None:
                    found = False
                else:
                    is_abbreviation = m.group(2) == '.' \
                                      and not re.search(r'[-#`\'"(){}\[\]!?:;,@\$%^&*+|=~<>\/\\_]$',
                                                        m.group(1)) \
                                      and (
                                          m.group(
                                              1) in self.abbreviations  # list of known abbreviations with period
                                          or (
                                              words and re.match(
                                                  r'^[-`\'"(){}\[\]!?:;,@\$%^*+|=~>\/\\]*[a-z]',
                                                  words[
                                                      0]) is not None)
                                          # probably abbreviation if next word (if it exists), starts with lower case letter # not: bla. <p>
                                          or re.match(r'^[A-Z]$', m.group(
                                              1))  # one single capital letter is probably second initial
                                          or (suffixes and re.match(r'^,;:?!$', suffixes[0]))
                                          or re.match(r'^[A-Za-z]+(\.[-A-Za-z])+$', m.group(1))
                                          or ('.' in self.ordinals and re.match(r'^[0-9]+$', m.group(1)))
                                          # probably abbreviation if another period inside word: e.g. A.M.
                                      )
                    if (is_abbreviation or
                            (m.group(2) == '"' and re.search(r'[0-9]$', m.group(1))) or
                            (m.group(2) == ')' and re.search(r'[A-Za-z]\(', m.group(1))) or
                            (m.group(2) == ';' and re.search(r'&[A-Za-z]+$', m.group(1))) or
                            re.match(r'^(\.+|,+|-+|`+|\'+|\*+)$', word) or
                            (m.group(2) in ['.-', ',-', '.=', ',='] and re.search(r'[0-9]$', m.group(1)))):
                        found = False
                    else:
                        if m.group(2) == '-':
                            if not words and not suffixes:
                                word = m.group(1)
                                found = False
                                hyphened = m.group(1)
                            else:
                                if ((words and words[0].lower() in self.coord) or (
                                            suffixes and suffixes[0] == ',')):
                                    found = False
                                else:
                                    suffixes.insert(0, m.group(2))
                                    word = m.group(1)
                        else:
                            if m.group(2) in [".", "...", "…"]:
                                add_end_utt = True
                            else:
                                if m.group(2) in ["!", "?"]:
                                    if not suffixes or suffixes[0] in ['\'', '\'\'', '"']:
                                        if not words or re.match(r'^[^' + self.lc_alpha + r']', words[0]):
                                            add_end_utt = True
                                    else:
                                        if (suffixes[0] not in [',',
                                                                ')']):
                                            # "wil hij met met Naar de klote!, die uitkomt in"
                                            add_end_utt = True
                            word = m.group(1)
                            suffixes.insert(0, m.group(2))

        return add_end_utt, hyphened, word

    def punct_at_beginning(self, word, prefixes):
        found = True
        while found:
            m = re.match(r'^([#"(){}\[\]!?:;@\$%^&*+|=~<>\/\\_]|\.+|,+|-+|`+|\'+)(.+)$', word)
            if m is None:
                found = False
            else:
                if (word in self.apostrof
                    or (m.group(1) == "("
                        and (
                                    re.search(r'\)[A-Z' + self.lc_alpha + r']', m.group(2)) or
                                    re.search(r'\)-[^\s]*[' + self.uc_alpha + self.lc_alpha + r']',
                                              m.group(2))
                        )
                        )
                    or (m.group(1) == '.' and re.match(r'^[0-9]', m.group(2)))
                    or (m.group(1) == "'" and re.match(r'^[0-9][0-9](-|$)', m.group(2)))
                    or (m.group(1) == '&' and re.match(r'^[A-Za-z]+;', m.group(2)))
                    or re.search(r'^(\.+|,+|-+|`+|\'+|\*+)$', word)):
                    found = False
                else:
                    prefixes.append(m.group(1))
                    word = m.group(2)

        return word

    def special_characters(self, word, words):
        if not re.search(r'http', word) and not re.search(r'www', word) and not re.search(r'ftp', word):
            m = re.match(r'^(\S+)([&<>\/])(\S+)$', word)
            if m is not None:
                words.insert(0, m.group(3))
                words.insert(0, m.group(2))
                return self.special_characters(m.group(1), words)
        return word

    def missing_space(self, word, words):
        if not re.match(r'@|www|http|ftp|gopher|URL|htm', word):
            m = re.match(
                r'^([^.]*[' + self.lc_alpha + r'])([\)\'"]*\.[\)\'"]*)([' + self.uc_alpha + self.lc_alpha_special + r'][^.]*)$',
                word)
            if m:
                words.insert(0, m.group(3))
                word = m.group(1) + m.group(2)
        # !!! Here we do not use the same expression as in the perl tokenizer
        m = re.match(
            r'^(\S*[A-Za-z])([\(\)\'"\.!?]*[,:!?\)\(][\)\'"]*)([§°0-9' + self.uc_alpha + self.lc_alpha + r']\S*)$',
            word)
        if m is not None:
            words.insert(0, m.group(3))
            word = m.group(1) + m.group(2)
        else:
            m = re.match(
                r'^(\S*[A-Za-z])([\(\)\'"\.!?][,:!?\)\(\.][\)\'"]*)([§°0-9' + self.uc_alpha + self.lc_alpha + r']\S*)$',
                word)
            if m is not None:
                words.insert(0, m.group(3))
                word = m.group(1) + m.group(2)
        m = re.match(
            r'^([^&]*[' + self.uc_alpha + self.lc_alpha + r'])([\)\'"]*;[\)\'"]*)([' + self.uc_alpha + self.lc_alpha + r']\S*)$',
            word)
        if m is not None:
            words.insert(0, m.group(3))
            word = m.group(1) + m.group(2)
        m = re.match(r'^(.*\.)(--)(.+)$', word)
        if m is not None:
            words.insert(0, m.group(3))
            words.insert(0, m.group(2))
            word = m.group(1)

        return word

    def replace_sgml_entities(self, word):
        prefix = word
        suffix = ''

        found = True
        while found:
            m = re.match(r'(.*)&([' + self.lc_alpha + self.uc_alpha + r']+);(.*)', prefix)
            if m:
                prefix = m.group(1)
                key = m.group(2)
                if key in self.user_defined_tags:
                    suffix = self.user_defined_tags[key] + m.group(3) + suffix
                else:
                    if key in self.predefined_tags:
                        suffix = self.predefined_tags[key] + m.group(3) + suffix
                    else:
                        suffix = "&" + m.group(2) + ";" + m.group(3) + suffix
            else:
                found = False
        word = prefix + suffix
        return word

    def check_hyphen(self, words2, last_line, last_hyphened):
        if last_hyphened:
            def check_schiet_en_vechtgeval():
                m = re.search(r'^(.+)-', words2[0])
                return m and m.group(1).lower() in self.coord

            if not words2:
                last_line[-1] += ' -'
            elif words2[0].lower() in self.coord or check_schiet_en_vechtgeval():
                last_line[-1] += '-'
            elif re.search(r'[' + self.uc_alpha + r']$', last_hyphened):
                last_line.pop()
                words2[0] = last_hyphened + '-' + words2[0]
            elif re.search(r'^[' + self.lc_alpha + r']', words2[0]):
                last_line.pop()
                words2[0] = last_hyphened + words2[0]
            elif re.search(r'^[0-9' + self.uc_alpha + r']', words2[0]):  # "Groot-Brittannie"
                last_line.pop()
                words2[0] = last_hyphened + '-' + words2[0]
            else:
                last_line[-1] += ' -'

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument("-r", help="switch off newline", action="store_false")
        parser.add_argument("-e", help="switch off sentence newline", action="store_false")
        return parser


if __name__ == "__main__":
    Tokenizer.main()
