"""
Created: 2016/10/26
Unit tests for the basic containers modle.

"""

import unittest
from chunker_steps.basic import Word, Chunk


class TestWord(unittest.TestCase):

    def test_creation_missing_args(self):
        self.assertRaises(TypeError, Word)
        self.assertRaises(TypeError, Word, 5)
        self.assertRaises(TypeError, Word, 5, 'token', 'lem', 'VB', 'V-mapped', 'mana')

    def test_creation(self):
        word = Word(5, 'token', 'lem', 'VB', 'V-mapped', 'mana', 'en')
        self.assertEqual(5, word.getPosition())
        self.assertEqual('token', word.getToken())
        self.assertEqual('lem', word.getLemma())
        self.assertEqual('VB', word.getPos())
        self.assertEqual('V-mapped', word.getMappedPos())
        self.assertEqual('mana', word.getMorphAna())
        self.assertEqual('en', word.getLanguage())

    def test_set_get_phr(self):
        word = Word(5, 'token', 'lem', 'VB', 'V-mapped', 'mana', 'en')
        word.setPhr("foobar")
        self.assertEqual("foobar", word.getPhr())

    def test__str__(self):
        word = Word(5, 'token', 'lem', 'VB', 'V-mapped', 'mana', 'en')
        self.assertEqual("5 token[lem][VB][V-mapped](None)\n", str(word))

    def test__repr__(self):
        word = Word(5, 'token', 'lem', 'VB', 'V-mapped', 'mana', 'en')
        expected = "Word(nr=5, token='token', lemma='lem', pos='VB', mapped_pos='V-mapped') at"
        result = repr(word)
        self.assertTrue(result.startswith(expected))


class TestChunk(unittest.TestCase):

    def setUp(self):
        self.wordlist = list()
        self.wordlist.append(Word(1, 'word1', 'lem1', 'VB', 'V-mapped1', 'mana1', 'en'))
        self.wordlist.append(Word(2, 'word2', 'lem2', 'VB', 'V-mapped2', 'mana2', 'en'))

    def test_creation_missing_args(self):
        self.assertRaises(TypeError, Chunk)
        self.assertRaises(TypeError, Chunk, 5)
        self.assertRaises(TypeError, Chunk, 5, self.wordlist)
        self.assertRaises(TypeError, Chunk, 5, self.wordlist, 1)

    def test_creation_ok(self):
        Chunk(5, self.wordlist, 1, 2)

    def test__str__(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        expected = "5 1-2 O word1 word2 V-mapped1+V-mapped2"
        self.assertEqual(expected, str(chunk))

    def test__repr__(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        expected = "5 1-2 O word1 word2 V-mapped1+V-mapped2"
        self.assertEqual(expected, repr(chunk))

    def test_get_mapped_pos_sequence(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        expected = "V-mapped1+V-mapped2"
        self.assertEqual(expected, chunk.getMappedPosSequence())

    def test_get_tokens(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        expected = "word1 word2"
        self.assertEqual(expected, chunk.getTokens())

    def test_get_start_idx(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        self.assertEqual(1, chunk.getStartIdx())

    def test_get_end_idx(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        self.assertEqual(2, chunk.getEndIdx())

    def test_get_chunk(self):
        chunk = Chunk(5, self.wordlist, 1, 2)
        self.assertEqual(self.wordlist, chunk.getChunk())

    def test_position(self):
        chunk = Chunk(4, self.wordlist, 1, 2)
        self.assertEqual(4, chunk.getPosition())

    def test_get_on_chunk(self):
        achunk = Chunk(4, self.wordlist, 2, 4)
        cnk = achunk.getChunk()
        self.assertEqual("1 word1[lem1][VB][V-mapped1](None)\n", str(cnk.get(0)))

    def test__set_mapped_pos_sequence(self):
        wordlist = [Word(13, 'itself', 'itself', 'PRP', 'PREP', "", 'en')]
        achunk = Chunk(8, wordlist, 13, 13)
        self.assertEqual('PREP', achunk.getMappedPosSequence())


if __name__ == '__main__':
    unittest.main()
