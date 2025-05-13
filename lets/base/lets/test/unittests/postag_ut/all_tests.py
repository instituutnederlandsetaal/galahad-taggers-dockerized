"""
Import and run all unit tests for the postag_steps package.
Created on 2016/12/11.

"""

import sys
from os.path import abspath, normpath, dirname, join as pjoin


REPO_ROOT = normpath(abspath(pjoin(dirname(__file__), "..", "..", "..")))
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)


_TEST_MODULES = (
    'test.unittests.postag_ut.clean_output',
    'test.unittests.postag_ut.feat_vects',
)

# import all test modules:
for mod in _TEST_MODULES:
    exec("from {} import *".format(mod))


if __name__ == '__main__':
    import unittest
    unittest.main()
