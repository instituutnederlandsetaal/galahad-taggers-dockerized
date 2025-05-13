"""
Utility functions and classes used to facilitate unit testing.
Created on 2016/11/17.

"""

import io
from os.path import isfile, join as pjoin
from bisect import bisect_left


def spaces_to_tabs(alist):
    """Returns a new list with  any spaces replaced with tabs in all elements."""
    return [elm.replace(" ", '\t') for elm in alist]


def replace_extention(filename, newext):
    """Returns a filename with original extension replaced by the specified
       new extension."""
    DOT = "."
    name_list = filename.split(DOT)[:-1]
    return DOT.join(name_list + [newext.lstrip(DOT)])


def open_file(afile, mode='r', encoding=None):
    """Returns this same afile object if afile is file-like object,
       or opens and returns a file handle if afile is a string, assuming
       it is a file name. Raises RuntimeError otherwise."""
    if hasattr(afile, 'write'):  return afile
    if isinstance(afile, str):  return open(afile, mode, encoding=encoding)
    raise TypeError("Expected string filename or file-like object, got {}".format(type(afile)))


def collect_filenames(adir, ext):
    """Collects and returns a list of filenames within given directory with given extension."""
    return [filename for filename in os.listdir(adir) if isfile(pjoin(adir, filename)) and filename.endswith(ext)]


class CustomStringIO(io.StringIO):
    """A handy writable StringIO buffer that allows for accessing the written content
       even after close() has been invoked. (Useful for testing purposes.)"""

    def __init__(self, *args, **kwargs):
        io.StringIO.__init__(self, *args, **kwargs)
        self._content = None

    def close(self):
        self._content = self.getvalue()
        super().close()

    def getvalue(self):
        try:
            return super().getvalue()
        except ValueError as err:
            if 'I/O operation on closed file' in str(err):
                return self._content
            raise


# ___________________________________________________________________________
# Unittest section below.

"""
Unit tests for the common util module.
Created on 2016/11/17.
"""

import unittest
import os
import sys
import shutil
import tempfile
from sortedcontainers.sortedset import SortedSet


class TestSPacesToTabs(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(["one\ttwo\tthree"], spaces_to_tabs(["one two three"]))

    def test_complex(self):
        expected = ["one\t\tthree\tfour\t", "five\tsix"]
        result = spaces_to_tabs(["one\t\tthree\tfour\t", "five\tsix"])
        self.assertEqual(expected, result)


class TestReplaceExtention(unittest.TestCase):

    def test_replace_extention_sright_case_no_dot_in_newext(self):
        self.assertEqual('myfile-1.pdf', replace_extention('myfile-1.txt', 'pdf'))
        self.assertEqual('yourfile-1.doc', replace_extention('yourfile-1.txt', 'doc'))

    def test_replace_extention_sright_case_with_dot_in_newext(self):
        self.assertEqual('myfile-2.pdf', replace_extention('myfile-2.txt', '.pdf'))
        self.assertEqual('yourfile-2.doc', replace_extention('yourfile-2.txt', '.doc'))


class TestOpenFile(unittest.TestCase):

    def test_fhandle_case(self):
        fhandle = CustomStringIO()
        self.assertIs(fhandle, open_file(fhandle, 'w'))

    def test_filename_case(self):
        try:
            tempf = tempfile.NamedTemporaryFile(mode='w')
            fhandle = open_file(tempf.name)
            self.assertTrue(hasattr(fhandle, 'write'))
        finally:
            try: fhandle.close()
            except: pass
            try: tempf.close()
            except: pass

    def test_raises_exception(self):
        self.assertRaises(TypeError, open_file, 42)


class TestCollectFilenames(unittest.TestCase):

    #TEMP_DIR = "./tmp"
    temp_dir = None

    @classmethod
    def touch_file(cls, path):
        with open(path, 'w') as fhl:
            fhl.write("")

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        #print("Temporary directory:", cls.temp_dir)
        cls.touch_file(os.path.join(cls.temp_dir, 'file1.txt'))
        cls.touch_file(os.path.join(cls.temp_dir, 'file2.txt'))
        cls.touch_file(os.path.join(cls.temp_dir, 'file3.foo'))
        cls.touch_file(os.path.join(cls.temp_dir, 'file4.bar'))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
        assert not os.path.exists(cls.temp_dir)

    def test_collect_filenames_case_txt(self):
        expected = ('file1.txt', 'file2.txt')
        actual = collect_filenames(self.temp_dir, '.txt')
        self.assertEqual(set(expected), set(actual))

    def test_collect_filenames_case_foo(self):
        expected = ('file3.foo',)
        actual = collect_filenames(self.temp_dir, '.foo')
        self.assertEqual(set(expected), set(actual))

    def test_collect_filenames_case_bar(self):
        expected = ('file4.bar',)
        actual = collect_filenames(self.temp_dir, '.bar')
        self.assertEqual(set(expected), set(actual))

    def test_collect_filenames_case_nothing_found(self):
        self.assertEqual(0, len(collect_filenames(self.temp_dir, '.brokenext')))


class TestCustomStringIO(unittest.TestCase):

    def test_stright_case(self):
        buff = CustomStringIO()
        buff.write("SOME CONTENT-1")
        buff.close()
        self.assertEqual("SOME CONTENT-1", buff.getvalue())
        self.assertEqual("SOME CONTENT-1", buff.getvalue())

    def test_not_closed(self):
        buff = CustomStringIO()
        buff.write("SOME CONTENT-2")
        self.assertEqual("SOME CONTENT-2", buff.getvalue())
        self.assertEqual("SOME CONTENT-2", buff.getvalue())


if __name__ == '__main__':
    unittest.main()
