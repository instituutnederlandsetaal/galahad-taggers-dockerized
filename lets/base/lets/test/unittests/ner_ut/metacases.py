# coding: utf-8

"""
LT3FEats functions test cases meta description.

Used by ut_generator.py to create sets of both Python and Java unit tests
to allow for comparing the behavior of both implementations.

Created on 2016/11/20.


This is a giant OrderedDict structure where the key of each element is a tuple
of all synonymous functions under test, specified as 'Class.function' string.

The value mapped to each key is a tuple of two-element tuples, the left specifying
the assert method and the right specifying the argument(s) to the function.

The right tuple may optionally contain a reason for the test ti be skipped, which
is a string starting with "R:". Thus make sure no string argument starts with
this combination, to avoid confusing the test generator.

A single test case meta-description format:
         ((assertMethod, expected), (*arguments, optinal_skip_reason)),

e.g., for the LT3Feats.all_capitals() function (having no optinal skip reason):
         (('assertEqual', "0 "), ("ACEUb",)),   # note the comma within the one-element tuple!

and with an optional skip reason, which will generate skip decorator/annotation to suppress that test:
         (('assertEqual', "1 "), ("ACEUI", "R:incorrectly implemented")),

Give this structure to the ut_generator.TestGenerator class.


FIXME: IMPORTANT: Decide on implementation/expected values and remove the skip reasons maked "R:" below.

"""

from collections import OrderedDict


NER_FEATS_METACASES = OrderedDict((

    (('ScannedTokenNER.first_capital',),  (
         (('assertEqual', "1 "), ("Aceui.",)),
         (('assertEqual', "1 "), ("Àçèüî.", "R:no special letters handling yet")),
         (('assertEqual', "0 "), ("aCEUI",)),
         (('assertEqual', "0 "), ("âÇÉÛÏ",)),
         (('assertEqual', "0 "), (".",)),
         (('assertEqual', "0 "), (".ACEUI",)),
         (('assertEqual', "0 "), (".ÄÇÉÛÏ",)),
    )),

    (('ScannedTokenNER.all_capitals',), (
         (('assertEqual', "1 "), ("ACEUI", "R:incorrectly implemented")),
         (('assertEqual', "1 "), ("ÄÇÉÛÏ", "R:no special letters handling yet|Java version incorrectly implemented")),
         (('assertEqual', "0 "), ("ACEUI2", "R:incorrectly implemented")),
         (('assertEqual', "0 "), ("ÄÇÉÛÏ2", "R:no special letters handling yet")),
         (('assertEqual', "0 "), ("ACEUI,", "R:no special letters handling yet")),
         (('assertEqual', "0 "), ("ÄÇÉÛÏ,", "R:no special letters handling yet")),
         (('assertEqual', "0 "), (".", "R:incorrectly implemented")),
         (('assertEqual', "0 "), ("", "R:incorrectly implemented")),
         (('assertEqual', "0 "), ("ACEUb",)),
         (('assertEqual', "0 "), ("ÄÇÉÛî", "R:no special letters handling yet")),
         (('assertEqual', "0 "), ("iACEU", "R:incorrectly implemented")),
         (('assertEqual', "0 "), ("îÄÇÉÛ", "R:no special letters handling yet")),
         (('assertEqual', "0 "), ("aceui", "R:incorrectly implemented")),
         (('assertEqual', "0 "), ("àçèüî", "R:no special letters handling yet")),
    )),

    (('ScannedTokenNER.internal_caps',), (
        (('assertEqual', "1 "), ("ACEUI",)),
        (('assertEqual', "1 "), ("ÄÇÉÛÏ", "R:no special letters handling yet")),
        (('assertEqual', "1 "), ("aCEUI",)),
        (('assertEqual', "1 "), ("äÇÉÛÏ", "R:no special letters handling yet")),
        (('assertEqual', "1 "), ("AcEuio",)),
        (('assertEqual', "1 "), ("ÄçÈùïö", "R:no special letters handling yet")),
        (('assertEqual', "1 "), ("aceuI",)),
        (('assertEqual', "1 "), ("àçèüÎ", "R:no special letters handling yet")),
        (('assertEqual', "1 "), ("aC",)),
        (('assertEqual', "1 "), ("àÇ", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("A",)),
        (('assertEqual', "0 "), ("Ä",)),
        (('assertEqual', "1 "), ("AceuI",)),
        (('assertEqual', "1 "), ("ÄçèüÎ", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("Aceui",)),
        (('assertEqual', "0 "), ("Äçèüî",)),
        (('assertEqual', "0 "), ("aceuio",)),
        (('assertEqual', "0 "), ("àçèüîö",)),
        (('assertEqual', "0 "), ("Aceuio",)),
        (('assertEqual', "0 "), ("Äçèùïö",)),
    )),

    (('ScannedTokenNER.all_lower_case',),  (
        (('assertEqual', "1 "), ("aceuio",)),
        (('assertEqual', "1 "), ("àçèüîö",)),
        (('assertEqual', "1 "), ("ace_uio",)),
        (('assertEqual', "1 "), ("àçè_üîö",)),
        (('assertEqual', "1 "), ("aceuio.",)),
        (('assertEqual', "1 "), ("àçèüîö.",)),
        (('assertEqual', "0 "), ("aceuiO",)),
        (('assertEqual', "0 "), ("àçèüîÖ", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("Aceuio",)),
        (('assertEqual', "0 "), ("Äçèüîö", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("abCDef",)),
        (('assertEqual', "0 "), ("acEUio",)),
        (('assertEqual', "0 "), ("àçËÙîö", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("ACEUI",)),
        (('assertEqual', "0 "), ("ÄÇÉÛÏ", "R:no special letters handling yet")),
    )),

    (('ScannedTokenNER.contains_digit',),  (
        (('assertEqual', "1 "), ("Ab.,'c228def",)),
        (('assertEqual', "1 "), ("Äß.,'ç228üîö",)),
        (('assertEqual', "1 "), ("1",)),
        (('assertEqual', "1 "), ("Ab.,'Cde9",)),
        (('assertEqual', "1 "), ("Äß.,'Çüî9",)),
        (('assertEqual', "1 "), ("5def",)),
        (('assertEqual', "1 "), ("5üîö",)),
        (('assertEqual', "0 "), ("IOAE",)),
        (('assertEqual', "0 "), ("ÏÔÄÉ",)),
        (('assertEqual', "0 "), ("m³",)),
    )),

    (('ScannedTokenNER.contains_digit_and_alpha',),  (
        (('assertEqual', "1 "), ("1234A",)),
        (('assertEqual', "1 "), ("1234Ä",)),
        (('assertEqual', "1 "), ("1U",)),
        (('assertEqual', "1 "), ("1Ü",)),
        (('assertEqual', "1 "), ("Ab789",)),
        (('assertEqual', "1 "), ("Äß789",)),
        (('assertEqual', "1 "), ("5def",)),
        (('assertEqual', "1 "), ("5üîö",)),
        (('assertEqual', "0 "), ("IOAE",)),
        (('assertEqual', "0 "), ("ÏÔÄÉ",)),
        (('assertEqual', "0 "), ("456789",)),
        (('assertEqual', "0 "), ("m³",)),
    )),

    (('ScannedTokenNER.only_digits',),  (
        (('assertEqual', "0 "), ("40,000",)),
        (('assertEqual', "1 "), ("1234",)),
        (('assertEqual', "1 "), ("100",)),
        (('assertEqual', "0 "), ("A789",)),
        (('assertEqual', "0 "), ("Â789",)),
        (('assertEqual', "0 "), ("5def",)),
        (('assertEqual', "0 "), ("5üîö",)),
        (('assertEqual', "1 "), ("", "R:wrong expected value")),
        (('assertEqual', "0 "), ("IOAE",)),
        (('assertEqual', "0 "), ("ÏÔÄÉ",)),
        (('assertEqual', "0 "), ("5678v",)),
        (('assertEqual', "0 "), ("5678ÿ",)),
        (('assertEqual', "0 "), ("⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉",)),
    )),

    (('ScannedTokenNER.is_punctuation',),  (
        (('assertEqual', "1 "), ("^",)),
        (('assertEqual', "1 "), (";",)),
        (('assertEqual', "0 "), ("123,",)),
        (('assertEqual', "0 "), ("!100",)),
        (('assertEqual', "0 "), ("A789",)),
        (('assertEqual', "0 "), ("Ä789",)),
        (('assertEqual', "0 "), ("789",)),
        (('assertEqual', "0 "), ("5def",)),
        (('assertEqual', "0 "), ("5üîö",)),
        (('assertEqual', "1 "), ("", "R:wrong expected value")),
        (('assertEqual', "1 "), (",",)),
        (('assertEqual', "1 "), ("!,./?",)),
        (('assertEqual', "0 "), ("IOAE",)),
        (('assertEqual', "0 "), ("ÏÔÄÉ",)),
        (('assertEqual', "0 "), ("5678v",)),
        (('assertEqual', "0 "), ("5678ÿ",)),
    )),

    (('ScannedTokenNER.contains_punctuation',),  (
        (('assertEqual', "0 "), ("^pas",)), # contradicts isPunctuation()!
        (('assertEqual', "1 "), (";",)),
        (('assertEqual', "0 "), ("Río",)),
        (('assertEqual', "0 "), ("]",)),
        (('assertEqual', "1 "), ("123,",)),
        (('assertEqual', "1 "), ("!100",)),
        (('assertEqual', "0 "), ("A789",)),
        (('assertEqual', "0 "), ("Â789", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("5def",)),
        (('assertEqual', "0 "), ("5üîö", "R:no special letters handling yet")),
        (('assertEqual', "1 "), (",",)),
        (('assertEqual', "1 "), ("EU,./42",)),
        (('assertEqual', "1 "), ("ÈÜ,./42",)),
        (('assertEqual', "0 "), ("IOAE",)),
        (('assertEqual', "0 "), ("ÏÔÄÉ", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("5678v",)),
        (('assertEqual', "0 "), ("5678ÿ", "R:no special letters handling yet")),
        # and some cases with caps:
        (('assertEqual', "1 "), ("ACEUIO.",)),
        (('assertEqual', "1 "), ("ÀÇÈÜÎÖ.", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("ACEUIO",)),
        (('assertEqual', "0 "), ("ÀÇÈÜÎÖ",)),
        (('assertEqual', "0 "), ("ACE%$@#_",)),
        (('assertEqual', "0 "), ("ÀÇÈ%$@#_", "R:no special letters handling yet")),
        (('assertEqual', "1 "), (".ACE%$@#",)),
        (('assertEqual', "1 "), (".ÀÇÈ%$@#",)),
        (('assertEqual', "0 "), ("acE%$@#",)),
        (('assertEqual', "0 "), ("àçÈ%$@#", "R:no special letters handling yet")),
        (('assertEqual', "1 "), ("ACE?$@#_",)),
        (('assertEqual', "1 "), ("ÀÇÈ?$@#_",)),
    )),

    (('ScannedTokenNER.is_hyphenated',),  (
        (('assertEqual', "0 "), ("12",)),
        (('assertEqual', "0 "), ("-",)),
        (('assertEqual', "0 "), ("--",)),
        (('assertEqual', "0 "), ("a-",)),
        (('assertEqual', "0 "), ("ä-",)),
        (('assertEqual', "0 "), ("A-",)),
        (('assertEqual', "0 "), ("À-",)),
        (('assertEqual', "0 "), ("ace-",)),
        (('assertEqual', "0 "), ("ACE-",)),
        (('assertEqual', "0 "), ("äçë-",)),
        (('assertEqual', "0 "), ("-ace?",)),
        (('assertEqual', "0 "), ("-àçê?",)),
        (('assertEqual', "0 "), ("-a-",)),
        (('assertEqual', "0 "), ("-â-",)),
        (('assertEqual', "0 "), ("-ace-",)),
        (('assertEqual', "0 "), ("-àçé-",)),
        (('assertEqual', "1 "), ("12-a",)),
        (('assertEqual', "1 "), ("12-ä",)),
        (('assertEqual', "1 "), ("qwe-rt",)),
        (('assertEqual', "1 "), ("äßç-üä",)),
    )),

    (('ScannedTokenNER.is_initial',),  (
        (('assertEqual', "1 "), ("A.",)),
        (('assertEqual', "0 "), ("A",)),
        (('assertEqual', "0 "), (".A", "R:incorrectly implemented")),
        (('assertEqual', "0 "), ("..A", "R:incorrectly implemented")),
        (('assertEqual', "0 "), ("abc",)),
        (('assertEqual', "1 "), ("G.M.",)),
        (('assertEqual', "1 "), ("I.B.M.",)),
        (('assertEqual', "0 "), ("IBM",)),
        (('assertEqual', "1 "), ("Â.", "R:no special letters handling yet")),
        (('assertEqual', "0 "), (".À",)),
        (('assertEqual', "0 "), ("..Ä",)),
        (('assertEqual', "0 "), ("àçé",)),
        (('assertEqual', "1 "), ("U.E.",)),
        (('assertEqual', "1 "), ("Ù.Ë.", "R:no special letters handling yet")),
        (('assertEqual', "1 "), ("U.S.A.",)),
        (('assertEqual', "1 "), ("Ü.Ç.Â.", "R:no special letters handling yet")),
        (('assertEqual', "0 "), ("IBM",)),
        (('assertEqual', "0 "), ("ÎÇÊ",)),
    )),

    (('ScannedTokenNER.is_url',),  (
        (('assertEqual', "0 "), ("not-a-URL",)),
        (('assertEqual', "1 "), ("http://example.com",)),
        (('assertEqual', "1 "), ("https://example.com", "R:incorrect java implementation")),  # wrong return value
        (('assertEqual', "1 "), ("ftp://ftp.example.com", "R:incorrect java implementation")),  # wrong return value
        (('assertEqual', "1 "), ("mailto://someone@example.com", "R:incorrect java implementation")),  # wrong return value
        (('assertEqual', "1 "), ("www.example.com",)),
        (('assertEqual', "0 "), ("foooohttp://example.com", "R:incorrect java implementation")),  # wrong return value
        (('assertEqual', "0 "), ("barrrwww.example.com", "R:incorrect java implementation")),  # wrong return value
        (('assertEqual', "0 "), ("wwwexample.com", "R:incorrect java implementation")),  # wrong return value
        (('assertEqual', "0 "), ("http////::::example.com", "R:incorrect java implementation")),
        (('assertEqual', "0 "), ("https/example.com",)),  # wrong return value
    )),

    # We do not test ScannedTokenNER.word_length as original versions return strings and current returns int. 

    (('ScannedTokenNER.prefix()',),  (
        (('assertEqual', "123 "), ("123", 3)),
        (('assertEqual', "123 "), ("1234", 3)),
        (('assertEqual', "123 "), ("12345", 3)),
        (('assertEqual', "123 "), ("123", 4)),
        (('assertEqual', "1 "), ("1", 4)),
        (('assertEqual', "1 "), ("123", 1)),
        (('assertEqual', " "), ("123", 0)),
        (('assertEqual', "abc "), ("abc", 3)),
        (('assertEqual', "abc "), ("abc4", 3)),
        (('assertEqual', "abc "), ("abc45", 3)),
        (('assertEqual', "abc "), ("abc", 4)),
        (('assertEqual', "a "), ("a", 4)),
        (('assertEqual', "a "), ("abc", 1)),
        (('assertEqual', " "), ("abc", 0)),
    )),

    (('ScannedTokenNER.suffix()',),  (
        (('assertEqual', "123 "), ("123", 3)),
        (('assertEqual', "234 "), ("1234", 3)),
        (('assertEqual', "345 "), ("12345", 3)),
        (('assertEqual', "123 "), ("123", 4)),
        (('assertEqual', "1 "), ("1", 4)),
        (('assertEqual', "3 "), ("123", 1)),
        (('assertEqual', " "), ("123", 0)),
        (('assertEqual', "abc "), ("abc", 3)),
        (('assertEqual', "bcd "), ("abcd", 3)),
        (('assertEqual', "cde "), ("abcde", 3)),
        (('assertEqual', "abc "), ("abc", 4)),
        (('assertEqual', "a "), ("a", 4)),
        (('assertEqual', "c "), ("abc", 1)),
        (('assertEqual', " "), ("abc", 0)),
    )),

    (('ScannedTokenNER.word_shape',),  (
        (('assertEqual', "other"), ("Historiek_",)),
        (('assertEqual', "other"), ("MRI_IRM",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("No-one",)),
        (('assertEqual', "allCapsAndPunct"), ("CAPACITY-BUILDING",)),
        (('assertEqual', "allCapsAndPunct"), ("MM]YYYY",)),
        (('assertEqual', "allCapsAndPunct"), ("N=",)),
        (('assertEqual', "allLowercase"), ("aceuio",)),
        (('assertEqual', "onlyDigits"), ("Ô98",)),
        (('assertEqual', "onlyDigits"), ("â€~03",)),
        (('assertEqual', "allLowercase"), ("àçèüîö", "R:no special letters handling yet")),
        (('assertEqual', "onlyDigits"), ("1234",)),
        (('assertEqual', "containsDigitAndAlpha"), ("12aceACEe5u34",)),
        (('assertEqual', "containsDigitAndAlpha"), ("12àçèÄÇÉè5ü34", "R:no special letters handling yet")),
        (('assertEqual', "onlyPunct"), ("#$%^&-=+[]{}!@*()<>;:/|`~'",)),
        (('assertEqual', "other"), ("_",)),
        (('assertEqual', "other"), ("____",)),
        (('assertEqual', "allCaps"), ("ACEUI",)),
        (('assertEqual', "allCaps"), ("ÄÇÉÛÏ", "R:no special letters handling yet")),
        (('assertEqual', "mixedCase"), ("ACeuI",)),
        (('assertEqual', "mixedCase"), ("ÄÇèüÏ", "R:no special letters handling yet")),
        (('assertEqual', "allCapsAndPunct"), ("AC,EU,I.,",)),
        (('assertEqual', "allCapsAndPunct"), ("ÄÇ,ÉÛ,Ï.", "R:no special letters handling yet")),
        (('assertEqual', "capPeriod"), ("A.",)),
        (('assertEqual', "capPeriod"), ("Ä.", "R:no special letters handling yet")),
        (('assertEqual', "mixedCase"), ("acEUiACeuI", "R:no special letters handling yet")),
        (('assertEqual', "mixedCase"), ("àçËÙîÄÇèüî", "R:no special letters handling yet")),
        (('assertEqual', "firstCapAlphaAndPunct"), ("ACEui,aceUI!ACEui.",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("ÄÇÉüî,àçËÙÏ!ÄÇèüî.", "R:no special letters handling yet")),
        (('assertEqual', "firstCapAlphaAndPunct"), ("AcEui,aceUI!ACEui.",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("ÄçÉüî,àçËÙÏ!ÄÇèüî.", "R:no special letters handling yet")),
        (('assertEqual', "alphaAndPunct"), ("aCEui,aceUI!ACEui.",)),
        (('assertEqual', "alphaAndPunct"), ("àÇÉüî,àçËÙÏ!ÄÇèüî.", "R:no special letters handling yet")),
        (('assertEqual', "onlyPunct"), (".,!?.",)),
        (('assertEqual', "alphaAndPunct"), ("m³",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("Río",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("Paraná",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("Cristóbal",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("Açu",)),
        (('assertEqual', "firstCapAlphaAndPunct"), ("No-one",)),
        (('assertEqual', "alphaAndPunct"), ("http://www.fedweb.belgium.be/nl/over_de_organisatie/ontwikkeling_en_ondersteuning/medewerkers/competentiemanagement/",)),
    )),

    (('feat_vect.map_pos_ner()',),  (  # map_pos() is is now a module-level function
        # English:
        (('assertEqual', "SYM"), ("ADJ", "en")),
        (('assertEqual', "("), ("(", "en")),
        (('assertEqual', "CC"), ("CC", "en")),
        # Dutch:
        (('assertEqual', "NP"), ("SPEC(deeleigen)", "nl")),
        (('assertEqual', "FW"), ("SPEC(vreemd)", "nl")),
        (('assertEqual', "NP"), ("N(eigen", "nl")),
        (('assertEqual', "SPEC"), ("SPEC(fooo)", "nl")),
        (('assertEqual', "SPEC"), ("SPEC", "nl", "R:Java fails with 'String index out of range: -1'")),
        # French:
        (('assertEqual', "A"), ("ADJ", "fr")),
        (('assertEqual', "ADV"), ("ADV", "fr")),
        (('assertEqual', "CHIF"), ("NUM", "fr")),
        (('assertEqual', "P"), ("PRP", "fr")),
        (('assertEqual', "PONCT"), ("FRFOO", "fr")),
        # German:
        (('assertEqual', "DEFOO"), ("DEFOO", "de")),
    )),

))
