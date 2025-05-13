"""
Import and run ALL unit tests for the ugent lt3 preprocessor.
(Acceptance tests NOT included on purpose.)

Created on 2016/12/11.

"""

import unittest
import sys
from os.path import abspath, normpath, dirname, join as pjoin


REPO_ROOT = normpath(abspath(pjoin(dirname(__file__), "..", "..")))
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)


_MY_TEST_MODULES = [
    'test.unittests.test_abstract_steps',
    'test.unittests.test_abstract_crfpp',
    # FIXME: fails with FileNotFoundError: [Errno 2] No such file or directory: 'models/tokenizer/en/suffixes'
    #'test.unittests.test_tokenizer',
    'test.unittests.testutil',
]
_ALL_TESTS_MODULES = (
     'test.unittests.lemmatizer_ut.all_tests',
     'test.unittests.chunker_ut.all_tests',
     'test.unittests.lt3_tools_ut.all_tests',
     'test.unittests.ner_ut.all_tests',
     'test.unittests.postag_ut.all_tests',
)

# import all test modules:
for mod in _ALL_TESTS_MODULES:
    exec("from {} import _TEST_MODULES; _MY_TEST_MODULES.extend(_TEST_MODULES)".format(mod))

for mod in _MY_TEST_MODULES:
    exec("from {} import *".format(mod))


if __name__ == '__main__':
    unittest.main()
