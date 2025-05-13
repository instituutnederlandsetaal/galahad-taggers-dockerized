"""
Pure Python impl. of scanning + determining token characters' types.

"""

# Fastest lookup is in a set of ascii codes. This is close to even checking for a range!

_SUPSUBS = "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉"
_PUNCTS = '!"&\'(),./:<>?\\{}' # ^
_PUNCT2 = '!"&\'(),./:;<>?{}'  # ^[]
_DIGITS = "0123456789"
_UPPERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LOWERS = "abcdefghijklmnopqrstuvwxyz"
_OTHERS = "#$%*+-;=@[]_`|~"

# some special letters: Fr: 'ÀàÂâÆæÇçÉéÈèÊêËëÎîÏïÔôŒœÙùÛûÜüŸÿ' + De: 'ÄäÖöÜüß'


globs = globals()
for varname in ('_SUPSUBS', '_PUNCTS', '_PUNCT2', '_DIGITS', '_UPPERS', '_LOWERS'):
    globs[varname] = set(ord(ch) for ch in globs[varname])


_ALPHAS = _UPPERS | _LOWERS
_ALPHANUMS = _ALPHAS | _DIGITS
_PUNCTS |= _PUNCT2

ch_isupper = lambda ch: ord(ch) in _UPPERS
ch_islower = lambda ch: ord(ch) in _LOWERS
ch_isdigit = lambda ch: ord(ch) in _DIGITS
ch_ispunct = lambda ch: ord(ch) in _PUNCTS #or (ch.isalpha() and not (ord(ch) in _ALPHAS))  # hack! _PUNCTS only
ch_isalpha = lambda ch: ord(ch) in _ALPHAS
ch_isalnum = lambda ch: ord(ch) in _ALPHANUMS


def lookup_scan(token):
    """Scans the string token detecting different types of characters, and returns
       a five-element tuple of boolean flags
          (hasupper, haslower, hasdigit, haspunct, hasother).
       Does NOT honor non-ascii letters like German 'umlauts' and French accented
       letters."""
    hasupper = haslower = hasdigit = haspunct = hasother = False
    for ch in token:
        c = ord(ch)
        isupper = c in _UPPERS
        islower = c in _LOWERS
        isdigit = c in _DIGITS
        ispunct = (c in _PUNCTS)
        isother = not (isupper or islower or isdigit or ispunct)
        hasupper = hasupper or isupper
        haslower = haslower or islower
        hasdigit = hasdigit or isdigit
        haspunct = haspunct or ispunct
        hasother = hasother or isother
        # exiting earlier doesn't pay off :(
        if all((hasupper, haslower, hasdigit, haspunct, hasother)):
            break
    return (hasupper, haslower, hasdigit, haspunct, hasother)


def ascii_scan(token):
    """Scans the string token detecting different types of characters, and returns
       a five-element tuple of boolean flags
          (hasupper, haslower, hasunder, hasdigit, hasother).
       Does NOT honor non-ascii letters like German 'umlauts' and French accented
       letters."""
    hasupper = haslower = hasdigit = haspunct = hasother = False
    for ch in token:
        c = ord(ch)
        isupper = (c > 64 and c < 91)
        islower = (c > 96 and c < 123)
        isdigit = (c > 47 and c < 58)
        ispunct = (c in _PUNCTS)
        isother = not (isupper or islower or isdigit or ispunct)
        hasupper = hasupper or isupper
        haslower = haslower or islower
        hasdigit = hasdigit or isdigit
        haspunct = haspunct or ispunct
        hasother = hasother or isother
        # exiting earlier doesn't pay off :(
    return (hasupper, haslower, hasdigit, haspunct, hasother)


def true_scan(token):
    """Scans the string token detecting different types of characters, honoring
       non-ascii letters, and returns a five-element tuple of boolean flags
       (hasupper, haslower, hasdigit, haspunct, hasother). Examples for non-ascii
       letters are German 'umlauts' and French accented letters."""
    hasupper = haslower = hasdigit = haspunct = hasother = False
    for ch in token:
        c = ord(ch)
        isupper = ch.isupper()
        islower = ch.islower()
        isdigit = ch.isdigit() and c not in _SUPSUBS
        ispunct = (c in _PUNCTS)
        isother = not (isupper or islower or isdigit or ispunct)
        hasupper = hasupper or isupper
        haslower = haslower or islower
        hasdigit = hasdigit or isdigit
        haspunct = haspunct or ispunct
        hasother = hasother or isother
        # exiting earlier doesn't pay off :(
    return (hasupper, haslower, hasdigit, haspunct, hasother)


char_scan = lookup_scan
