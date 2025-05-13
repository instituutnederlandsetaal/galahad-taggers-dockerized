"""
Acceptance tests for the chunk.parse module.
Created on 2016/11/06.

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

from test.unittests.testutil import open_file
from chunker import Chunker


FILE_SIZE_LIMIT = 4     # in MB; <= 0 means no limit, defaults to the moderate 4MB


# TODO: clean the chunker acceptance from the hardcoded set of files test

ACCEPTANCE_FILES = (
    ('Madagascar_en', 'En'),   # this one is a must for some tests to run, keep it always

    # English:
    ('PSA_inputCrossLang_en', 'En'),
    ('JDN_jaar_input_en', 'En'),
    ('Photoshop_EN_part', 'En'),
    ('paris', 'En'),
    #('nobib', 'En'),    # ~ 6MB
    #('train_reviews_train_text', 'En'), # ~ 50 MB
    ('st05853.en12_utf8', 'En'),

    # German:
    ('PSA_inputCrossLang_du', 'De'),
    ('JDN_jaar_input_du', 'De'),
    ('WTCB23-de', 'De'),    # ~ 700 kB

    # French:
    ('PSA_inputCrossLang_fr', 'Fr'),
    ('JDN_jaar_input_fr', 'Fr'),
    ('Photoshop_FR_part', 'Fr'),
    #('RIZIV_fr', 'Fr'),     # ~ 15 MB

    # Dutch:
    ('Madagascar_nl', 'Nl'),
    ('PSA_inputCrossLang_nl', 'Nl'),
    ('JDN_jaar_input_nl', 'Nl'),
    #('RIZIV_nl', 'Nl'),     # ~ 22 MB
)


def fname_last_part(fname, lastchunks=2):
    return os.sep.join(fname.split(os.sep)[-lastchunks:])


class ChunkerAcceptanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._generated_cnks = list()
        return      # !!! suppressed in favor of using the data files directly
        if exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR, exist_ok=True)
        for filename, subdir in ACCEPTANCE_FILES:
            for ext in ('.pos', '.lem', '.cnk'):
                full_src = pjoin(REPO_ROOT, 'test', 'integrationtests', 'data', subdir, filename + ext)
                full_dst = pjoin(TEMP_DIR, filename + ext)
                assert not exists(full_dst), "dest file exists: " + full_dst
                print("Copying", filename + ext, "...")
                shutil.copy2(full_src, full_dst)

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
        if exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        cls._cleanup_generated_cnks()
        return

    MSG_SEP = "|"   # pipe char

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

    def _process_sample_file(self, filename, subdir):
        start = time.clock()
        print("\n*** File:", filename, "...", file=sys.stderr)
        # outf = CustomStringIO()
        pos_file = pjoin(filename + '.pos')
        lem_file = pjoin(filename + '.lem')
        cnk_file = pjoin(filename + '.new.cnk')
        chunker = Chunker(l=subdir.lower())
        try:
            chunker.process_files_by_name(lem_file, pos_file, cnk_file)
        except Exception as err:
            print("!!", filename, "FAILED!", err, file=sys.stderr)
            # store the name to allow for cleanup later
            self.__class__._generated_cnks.append(cnk_file)
            return False

        print("    elapsed time: {:.2f} sec.".format(time.clock() - start), file=sys.stderr)
        #with open(pjoin(TEMP_DIR, filename + '.python.cnk'), 'w') as fhl:
        #    fhl.write(outf.getvalue())
        #actual_data = io.StringIO(outf.getvalue())
        ok = True
        try:
            self.assertFilesEqual(pjoin(TEMP_DIR, filename + '.cnk'), cnk_file)
        except AssertionError as err:
            messages = str(err).split(self.MSG_SEP)
            # print("Found ", len(messages), " line differences in ",
            #      filename + ".cnk:\n", "\n\n".join(messages), sep="", file=sys.stderr)
            print("Found ", len(messages), " line differences in ", filename + ".new.cnk", sep="", file=sys.stderr)
            ok = False
        finally:
            # store the name to allow for cleanup later
            self.__class__._generated_cnks.append(cnk_file)
        return ok

    def _file_accepted_for_test(self, filename):
        if FILE_SIZE_LIMIT > 0:
            return os.path.getsize(filename) < FILE_SIZE_LIMIT * 1024 * 1024 # in MB
        return True

    def __test_acceptance_files(self):  # suppressed in favor of using the data files directly
        failed_count = 0
        for filename, subdir in ACCEPTANCE_FILES:
            full_path_no_ext = pjoin(TEMP_DIR, filename)
            if self._file_accepted_for_test(full_path_no_ext + '.pos'):
                failed_count += int(not self._process_sample_file(full_path_no_ext, subdir))
            else:
                print("\n--- Skipped file", filename, file=sys.stderr)
        self.assertTrue(failed_count == 0, "{} files FAILED - see output for details".format(failed_count))

    def test_against_ALL_data(self):
        #data_dir = '/home/yassen'
        data_dir = pjoin(REPO_ROOT, 'test', 'integrationtests', 'data')

        def collect_files(adir, ext='.pos'):
            return [pjoin(adir, file) for file in os.listdir(adir) if file.endswith(ext)]

        def collect_recursively(adir, ext='.pos'):
            result = list()
            for root, dirs, files in os.walk(adir):
                result += [pjoin(root, file) for file in files if file.endswith(ext)]
            return result

        failed_count = 0
        for subdir in ('En', 'De', 'Fr', 'Nl'):
            for file in collect_files(pjoin(data_dir, subdir)):
                if self._file_accepted_for_test(file):
                    failed_count += int(not self._process_sample_file(file[:-4], subdir))
                else:
                    print("\n--- Skipped file", file, file=sys.stderr)
        self.assertTrue(failed_count == 0, "{} files FAILED - see output for details".format(failed_count))


if __name__ == '__main__':
    unittest.main()
