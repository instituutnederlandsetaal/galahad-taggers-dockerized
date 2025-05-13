import os
import codecs

from lets.abstract_step import AbstractStep


class AdjustCapitalization(AbstractStep):
    def __init__(self, l):
        super().__init__(l)
        self.language = l
        self.lexicon = []
        self.lexiconLower = []
        with codecs.open(os.path.dirname(os.path.realpath(__file__)) + '/../models/lemmatizer/lemmaLexicon.{}'.format(l), 'r', 'utf8') as f:
            for l in f.readlines():
                l_strip = l.strip()
                if l_strip:
                    self.lexicon.append(l_strip)
                    items = l_strip.split()
                    newline = items[0].lower() + ' ' + items[1]
                    self.lexiconLower.append(newline)

    def process_line(self, line):
        if line.strip():
            result = line
            lineItems = line.strip().split()
            orgWord = lineItems[0]
            pos = lineItems[1]
            isNP = False  # boolean which indicates if a word is a proper noun or not
            # (necessary to determine for English and Dutch, because proper nouns are mapped to common nouns)
            if self.language == 'en':
                if pos.startswith('NNP'):
                    isNP = True
            if self.language == 'nl':
                if pos.startswith('N(eigen'):
                    isNP = True
            pos = self.mapPOS(pos)  # map the POS tags to the tagset used in the lemmatizer training data
            word = self.adjustCap(orgWord, pos, isNP, self.lexicon,
                                  self.lexiconLower)  # adjust capitalization of the word if necessary
            result = orgWord + ' ' + word + ' ' + pos  # MVDK 12-05-2015: also write out the original word form
            result.encode('utf8')
            return [result, '']
        else:
            return ['']

    def mapPOS(self, pos):
        language = self.language
        # maps the POS tagset of the POS tagger to the tag set used in the lemmatization training data (= a smaller subset)
        # the POS tag of a word is a feature in its feature vector
        if language == 'fr':
            if pos == 'NUM' or pos.startswith('PRO') or pos.startswith('PRP') or pos == 'KON' or pos.startswith(
                    'DET') or pos == 'ADV':
                pos = 'FtW'
        if language == 'nl':
            mainCat = pos[:pos.find('(')]  # main POS category e.g. N (noun)
            subCats = pos[pos.find('(') + 1:pos.rfind(')')].split(
                ',')  # POS subcategories e.g. for nouns: ev (singular), mv (plural)...
            isNP = False  # proper nouns and common nouns are mapped to the same category (N), but we have to remember if a noun is common or proper, in case it needs to be lowercased
            if mainCat == 'N':
                newpos = 'N('
                if 'ev' in subCats:
                    newpos += 'ev'
                if 'mv' in subCats:
                    newpos += 'mv'
                if 'dim' in subCats:
                    newpos += ',dim'
                if 'gen' in subCats:
                    newpos += ',gen'
                if 'dat' in subCats:
                    newpos += ',dat'
                newpos += ')'
            elif mainCat == 'LID':
                newpos = 'LID()'
            elif mainCat == 'TW':
                newpos = 'NUM('
                if 'hoofd' in subCats:
                    newpos += 'hoofd'
                if 'rang' in subCats:
                    newpos += 'rang'
                if 'mv-n' in subCats:
                    newpos += ',mv-n'
                if 'bijz' in subCats:
                    newpos += ',bijz'
                if 'dim' in subCats:
                    newpos += ',dim'
                newpos += ')'
            elif mainCat == 'VNW':
                newpos = 'VNW(' + subCats[0] + ')'
            elif mainCat == 'ADJ':
                if 'basis' in subCats:
                    newpos = 'ADJ(basis'
                    if 'met-e' in subCats:
                        newpos += ',met-e'
                        if 'bijz' in subCats:
                            newpos += ',bijz'
                        elif 'mv-n' in subCats:
                            newpos += ',mv-n'
                        else:
                            newpos += ',stan'
                    elif 'met-s' in subCats:
                        newpos += ',met-s'
                    else:
                        newpos += ',zonder'
                        if 'mv-n' in subCats:
                            newpos += ',mv-n'
                    newpos += ')'
                elif 'comp' in subCats:
                    newpos = 'ADJ(comp'
                    if 'met-e' in subCats:
                        newpos += ',met-e'
                        if 'bijz' in subCats:
                            newpos += ',bijz'
                        elif 'mv-n' in subCats:
                            newpos += ',mv-n'
                        else:
                            newpos += ',stan'
                    elif 'met-s' in subCats:
                        newpos += ',met-s'
                    else:
                        newpos += ',zonder'
                    newpos += ')'
                elif 'sup' in subCats:
                    newpos = 'ADJ(sup'
                    if 'met-e' in subCats:
                        newpos += ',met-e'
                        if 'bijz' in subCats:
                            newpos += ',bijz'
                        elif 'mv-n' in subCats:
                            newpos += ',mv-n'
                        else:
                            newpos += ',stan'
                    else:
                        newpos += ',zonder'
                    newpos += ')'
                else:
                    if 'dim' in subCats:
                        newpos = 'ADJ(dim)'
            elif mainCat == 'WW':
                if 'inf' in subCats:
                    newpos = 'WW(inf'
                    if 'met-e' in subCats:
                        newpos += ',met-e'
                    newpos += ')'
                if 'od' in subCats:
                    newpos = 'WW(od'
                    if 'met-e' in subCats:
                        newpos += ',met-e'
                    else:
                        newpos += ',zonder'
                    if 'mv-n' in subCats:
                        newpos += ',mv-n'
                    newpos += ')'
                if 'pv' in subCats:
                    newpos = 'WW(pv'
                    if 'conj' in subCats:
                        newpos += ',conj'
                    if 'tgw' in subCats:
                        newpos += ',tgw'
                    if 'verl' in subCats:
                        newpos += ',verl'
                    if 'ev' in subCats:
                        newpos += ',ev'
                    if 'met-t' in subCats:
                        newpos += ',met-t'
                    if 'mv' in subCats:
                        newpos += ',mv'
                    newpos += ')'
                if 'vd' in subCats:
                    newpos = 'WW(vd'
                    if 'met-e' in subCats:
                        newpos += ',met-e'
                    else:
                        newpos += ',zonder'
                    if 'mv-n' in subCats:
                        newpos += ',mv-n'
                    newpos += ')'
            else:
                newpos = pos
            pos = newpos
        if language == 'en':
            if pos == 'NNPS':
                pos = 'NNS'
            if pos == 'NNP':
                pos = 'NN'
            if pos == 'RP':
                pos = 'RB'
            if pos == 'WRB':
                pos = 'RB'
        if language == 'de':
            if pos == 'VMFIN':
                pos = 'VMFIN'
            elif pos.startswith('V'):
                pos = 'V' + pos[2:]
            elif pos.startswith('ADJ'):
                pos = 'ADJ'
            elif pos.startswith('PD'):
                pos = 'PD'
        return pos

    def adjustCap(self, word, pos, isNP, lexicon, lexiconLower):
        # adjusts the capitalization of a word if necessary (e.g. a word at the beginning of a sentence which is not a proper noun needs to be lowercased)
        # MOD Geert Coorman: removed unicode specifier in order to avoid the JYthon syntax error
        # Exception in thread "main" SyntaxError: Illegal character in file '<string>' for encoding 'utf-8'
        # upperChars=[u'Á',u'É',u'Í',u'Ó',u'Ú',u'Ä',u'Ë',u'Ï',u'Ö',u'Ü',u'À',u'È',u'Ì',u'Ò',u'Ù',u'Â',u'Ê',u'Î',u'Ô',u'Û'] # special upper case characters that need to be lowercased if necessary
        language = self.language
        line = word + ' ' + pos
        if language == 'fr':
            sameCasing = ['SYM', 'SENT', 'PUN', 'PUN:cit',
                          'ABR']  # POS tags for which the casing of the words stays the same
            if pos not in sameCasing:
                # if only the first letter of the word is uppercase
                if word[0].isupper() and word[1:].islower():
                    if pos != 'NAM':  # we assume a proper noun always starts with a capital letter
                        word = word.lower()  # all other words are lowercased
                # elif the word consists of lowercase as well as uppercase letters
                elif word != word.upper() != word.lower():
                    pass  # we assume this is deliberate
                # elif the word consists of uppercase letters entirely
                elif word.isupper():
                    if pos == 'NAM':
                        if not line in lexicon:  # check if the word is in the lexicon with other casing
                            lineLower = word.lower() + ' ' + pos
                            if lineLower in lexiconLower:
                                word = lexicon[lexiconLower.index(lineLower)].split()[
                                    0]  # adjust the casing if this is the case
                            else:
                                pass  # otherwise change nothing, in case the proper noun is an acronym
                    elif pos != 'ABR':  # all other words (except for abbreviations, which can be made up of capital letters entirely) are lowercased
                        word = word.lower()
        if language == 'en':
            sameCasing = ['LS', 'SYM', '"', '$', '(', ')', ',', '.', ':',
                          '``']  # POS tags for which the casing of the words stays the same
            if pos not in sameCasing:
                # if only the first letter of the word is uppercase
                if word[0].isupper() and word[1:].islower():
                    if not isNP:  # we assume a proper noun always starts with a capital letters
                        if pos == 'JJ' or pos.startswith('NN') or pos.startswith(
                                'PRP'):  # check if the word is in the lexicon with other casing
                            # we assume that words with other POS tags are always lowercase
                            if not line in lexicon:
                                lineLower = word.lower() + ' ' + pos
                                if lineLower in lexiconLower:
                                    word = lexicon[lexiconLower.index(lineLower)].split()[
                                        0]  # adjust the casing if possible
                                else:
                                    word = word.lower()  # all other words are lowercased
                        else:
                            word = word.lower()
                # elif the word consists of lowercase as well as uppercase letters
                elif word != word.lower() != word.upper():
                    pass  # we assume this is deliberate
                # elif the word consists of uppercase letters entirely
                elif word.isupper():
                    if pos.startswith('NN') or pos == 'JJ' or pos == 'PRP':
                        if not line in lexicon:  # check if the word is in the lexicon with other casing
                            lineLower = word.lower() + ' ' + pos
                            if lineLower in lexiconLower:
                                word = lexicon[lexiconLower.index(lineLower)].split()[
                                    0]  # adjust the casing if possible
                            else:
                                if not isNP:  # proper nouns stay uppercase in case they are acronyms
                                    word = word.lower()  # all other words are lowercased entirely
                    else:  # all other words are lowercased
                        word = word.lower()
        if language == 'nl':
            sameCasing = ['LET()', 'SPEC(deeleigen)',
                          'SPEC(symb)']  # POS tags for which the casing of the word stays the same
            if pos not in sameCasing:
                # if only the first letter of the word is uppercase
                if word[0].isupper() and word[1:].islower():
                    if pos.startswith('N(') or pos.startswith(
                            'ADJ('):  # check if the word is in the lexicon with other casing
                        # we assume that words with other POS tags are always lowercase
                        if not line in lexicon:  # check if the word is in the lexicon with other casing
                            lineLower = word.lower() + ' ' + pos
                            if lineLower in lexiconLower:
                                word = lexicon[lexiconLower.index(lineLower)].split()[
                                    0]  # adjust the casing if possible
                            else:
                                if not isNP:  # proper nouns always start with a capital letter (except for months/week days (included in the lexicon), which is why we didn't rule out NP's from the beginning)
                                    word = word.lower()  # all other words are lowercased
                    else:
                        word = word.lower()
                # elif the word consists of lowercase as well as uppercase letters
                elif word != word.lower() != word.upper():
                    pass  # we assume this is deliberate
                # elif the word consists of uppercase letters entirely
                elif word.isupper():
                    if pos.startswith('N(') or pos.startswith('ADJ('):
                        if not line in lexicon:  # check if the word is in the lexicon with other casing
                            lineLower = word.lower() + ' ' + pos
                            if lineLower in lexiconLower:
                                word = lexicon[lexiconLower.index(lineLower)].split()[
                                    0]  # adjust the casing if possible
                            else:
                                if not isNP:  # proper nouns stay uppercase in case they are acronyms
                                    word = word.lower()  # all other words are lowercased entirely
                    else:  # all other words are lowercased
                        word = word.lower()
        if language == 'de':
            sameCasing = ['$(', '$,', '$.', 'XY', 'TRUNC']  # POS tags for which the casing of the words stays the same
            if pos not in sameCasing:
                # if only the first letter of the word is uppercase
                if word[0].isupper() and word[1:].islower():
                    if pos != 'NE' and pos != 'NN':  # common and proper nouns always start with a capital letter in German
                        if pos == 'ADJ' or pos == 'PPER' or pos == 'PPOSAT' or pos == 'PPOSS' or pos == 'PRF':  # check if the word is in the lexicon with other casing
                            # we assume that words with other POS tags are always lowercase
                            if not line in lexicon:
                                lineLower = word.lower() + ' ' + pos
                                if lineLower in lexiconLower:
                                    word = lexicon[lexiconLower.index(lineLower)].split()[
                                        0]  # adjust the casing if possible
                                else:
                                    word = word.lower()  # all other words are lowercased
                        else:
                            word = word.lower()
                # elif the word consists of lowercase as well as uppercase letters
                elif word != word.lower() != word.upper():
                    pass  # we assume this is deliberate
                # elif the word consists of uppercase letters entirely
                elif word.isupper():
                    if pos == 'NN' or pos == 'NE' or pos == 'ADJ' or pos == 'PPOSS' or pos == 'PPOSAT' or pos == 'PRF':
                        if not line in lexicon:  # check if the word is in the lexicon with other casing
                            lineLower = word.lower() + ' ' + pos
                            if lineLower in lexiconLower:
                                word = lexicon[lexiconLower.index(lineLower)].split()[
                                    0]  # adjust the casing if possible
                            else:
                                if pos == 'NE':
                                    pass  # proper nouns stay uppercase in case they are acronyms
                                elif pos == 'NN':
                                    word = word[0] + word[
                                                     1:].lower()  # common nouns always have to start with a capital letter
                                else:
                                    word = word.lower()  # all other words are lowercased
                    else:  # all other words are lowercased
                        word = word.lower()
        return word

if __name__ == "__main__":
    AdjustCapitalization.main()
