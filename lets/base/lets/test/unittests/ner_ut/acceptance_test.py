"""
Acceptance tests for the Named Entity Recognizer package.
Created on 2016/11/24.

"""

import unittest
import os
import sys
import time
import shutil
from os.path import abspath, normpath, dirname, exists, join as pjoin

REPO_ROOT = normpath(abspath(pjoin(dirname(__file__), "..", "..", "..")))
TEMP_DIR = pjoin(REPO_ROOT, "tmp")
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)
print("REPO_ROOT:", REPO_ROOT)

from ner import NER
from test.unittests.testutil import collect_filenames, open_file


FILE_SIZE_LIMIT = 4     # in MB; <= 0 means no limit, defaults to the moderate 4MB

# FIXME: YD: This works only on my machine. Provide destination with .ner output adequate to NER models.
# DATA_DIR = pjoin(REPO_ROOT, 'test', 'integrationtests', 'data')
DATA_DIR = r"/home/yassen/Work/spaces/eclipse-4.6/ugent_lt3_java/WORK/ner4"


def fname_last_part(fname, lastchunks=2):
    return os.sep.join(fname.split(os.sep)[-lastchunks:])


class NERAcceptanceTest(unittest.TestCase):

    MSG_SEP = "|"   # pipe char

    @classmethod
    def setUpClass(cls):
        cls._generated_cnks = list()

    def assertFilesEqual(self, expected_file, actual_file):
        err_list = list()
        with open_file(expected_file) as expf, open_file(actual_file) as actf:
            for lno, (expln, realln) in enumerate(zip(expf, actf)):
                try:
                    self.assertEqual(expln, realln, "line {:d} differ: {!r} != {!r}".format(lno+1, expln, realln))
                except AssertionError as err:
                    err_list.append(err)
        if err_list:
            raise AssertionError(self.MSG_SEP.join((str(err) for err in err_list)))

    @classmethod
    def _cleanup_generated_cnks(cls):
        print(sep="")
        for cnk_file in cls._generated_cnks:
            print("Removing", fname_last_part(cnk_file), "...  ", end="")
            try:
                os.remove(cnk_file)
                print("OK.")
            except Exception as err:        # pylint: disable=broad-except
                print("!!", err)

    @classmethod
    def tearDownClass(cls):
        return
        if exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        cls._cleanup_generated_cnks()

    SUBDIR2LANG_MAP = {
        'En': 'en',
        'en': 'en',
        'De': 'de',
        'de': 'de',
        'Fr': 'fr',
        'fr': 'fr',
        'Nl': 'nl',
        'nl': 'nl',
        'nl2': 'nl',
    }

    def _process_sample_file(self, filename, subdir):
        start = time.clock()
        print("\n*** File:", filename, "...", file=sys.stderr)
        pos_file = pjoin(filename + '.pos')
        ner_file = pjoin(filename + '.new.ner')
        language = self.SUBDIR2LANG_MAP[subdir]

        ner = NER(language)

        try:
            pass
            ner.process_file_by_name(pos_file, ner_file)
        except Exception as err:
            print("!!", filename, "FAILED!", err, file=sys.stderr)
            # store the name to allow for cleanup later
            self.__class__._generated_cnks.append(ner_file)
            return False

        print("    elapsed time: {:.2f} sec.".format(time.clock() - start), file=sys.stderr)
        ok = True
        try:
            pass
            self.assertFilesEqual(pjoin(TEMP_DIR, filename + '.ner'), ner_file)
            print("OK:", pos_file)
        except AssertionError as err:
            messages = str(err).split(self.MSG_SEP)
            print("Found ", len(messages), " line differences in ", filename + ".new.ner", sep="", file=sys.stderr)
            ok = False
        finally:
            # store the name to allow for cleanup later
            self.__class__._generated_cnks.append(ner_file)
        return ok

    def _file_accepted_for_test(self, filename):
        if FILE_SIZE_LIMIT > 0:
            return os.path.getsize(filename) < FILE_SIZE_LIMIT * 1024 * 1024 # in MB
        return True

    def test_against_ALL_data(self):

        def collect_files(adir, ext='.pos'):
            return [pjoin(adir, file) for file in os.listdir(adir) if file.endswith(ext)]

        def collect_recursively(adir, ext='.pos'):
            result = list()
            for root, dirs, files in os.walk(adir):  # @UnusedVariable
                result += [pjoin(root, file) for file in files if file.endswith(ext)]
            return result

        failed_count = 0
        total_count = 0
        for subdir in ('En', 'De', 'Fr', 'Nl'):
            for file in collect_files(pjoin(DATA_DIR, subdir)):
                if self._file_accepted_for_test(file): 
                    total_count += 1
                    failed_count += int(not self._process_sample_file(file[:-4], subdir))
                else:
                    print("\n--- Skipped file", file, file=sys.stderr)
        self.assertTrue(failed_count == 0, "{} of {} files FAILED - see output for details" \
                        .format(failed_count, total_count))


if __name__ == '__main__':
    unittest.main()
