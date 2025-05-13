"""
Unit tests for the utils module.
Created on 2016/10/31

"""

import unittest
from chunker_steps.chunker_util import matches, contains


class TestMatches(unittest.TestCase):

    def test_matches_positive(self):
        self.assertTrue(matches("^[a-f]+$", "aabbccdd"))

    def test_matches_negative(self):
        self.assertFalse(matches("^[a-f]+$", "aabbccdx"))

    def test_matches_number(self):
        # Note that the Java matcher returns False if using  "[0-9]+" to match "22-2-98"
        # and Python returns True! Thus we need to always specify that we want a full match:
        self.assertTrue(matches("[0-9]+", "22-2-98"))
        self.assertFalse(matches("^[0-9]+$", "22-2-98"))


class TestContains(unittest.TestCase):

    def test_contains_positive(self):
        self.assertTrue(contains("123", "012345"))
        self.assertTrue(contains("123", "123"))
        self.assertTrue(contains("", "1"))
        self.assertTrue(contains("", ""))

    def test_contains_negative(self):
        self.assertFalse(contains("1230", "012345"))
        self.assertFalse(contains("1", ""))


if __name__ == '__main__':
    unittest.main(verbosity=0)
