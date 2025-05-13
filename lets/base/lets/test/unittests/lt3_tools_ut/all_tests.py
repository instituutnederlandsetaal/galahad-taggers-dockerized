# -*- coding: utf-8 -*-
"""
Import and run all unit tests for the chunker_steps package.
(Acceptance tests NOT included on purpose.)

Created on 2016/11/06.

"""

import sys
from os.path import abspath, normpath, dirname, join as pjoin


REPO_ROOT = normpath(abspath(pjoin(dirname(__file__), "..", "..", "..")))
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)


_TEST_MODULES = (
    'test.unittests.lt3_tools_ut.scanutil_test',
    'test.unittests.lt3_tools_ut.feat_test',
)

# import all test modules:
for mod in _TEST_MODULES:
    exec("from {} import *".format(mod))


if __name__ == '__main__':
    import unittest
    unittest.main()
