"""
Utilities for porting lt3_java/preprocessor_java/Chunker/src/domein Java package.
Created on 2016/10/31

"""

import re


def matches(regex, astring):
    """Returns True iff given string matches given regular expression,
       otherwise returns False."""
    return bool(re.match(regex, astring))


def contains(needle, haystack):
    """Returns True iff `haystack` contains `needle` string, False otherwise."""
    return needle in haystack
