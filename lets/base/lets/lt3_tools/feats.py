# coding: utf-8

"""
LT3 feature toosl module, ported from
  preprocessor_java/LT3Tools/src/feats Java package.

Created: 2016/11/18.

"""

from lets.lt3_tools.scanutil import lookup_scan


class ScannedToken(object):
    """ScannedToken objects encapsulate a non-empty string together with several
       boolean flags denoting the existence of certain types of characters within
       that string, e.g. `hasupper`, `haslower`, `hasdigit`, `haspunct`, `hasother`.

       Further deductions are possible (and provided via property getters) about
       the token, like `isupper`, `islower`, `isalpha`, `isalnum`, etc.
       """

    def __init__(self, token):
        if not token.strip():
            raise ValueError("Token cannot be empty (got {!r})".format(token))
        # TODO: reject tokens with white space?
        self._token = token
        self.hasupper, self.haslower, self.hasdigit, self.haspunct, self.hasother = lookup_scan(token)

    @property
    def isupper(self):
        return self.hasupper and not (self.haslower or self.hasdigit or self.haspunct or self.hasother)

    @property
    def islower(self):
        return self.haslower and not (self.hasupper or self.hasdigit or self.haspunct or self.hasother)

    @property
    def isalpha(self):
        return (self.hasupper or self.haslower) and not (self.hasdigit or self.haspunct or self.hasother)

    @property
    def isdigit(self):
        return self.hasdigit and not (self.hasupper or self.haslower or self.haspunct or self.hasother)

    @property
    def ispunct(self):
        return self.haspunct and not (self.hasupper or self.haslower or self.hasdigit or self.hasother)

    @property
    def isother(self):
        return self.hasother and not (self.hasupper or self.haslower or self.hasdigit or self.haspunct)
