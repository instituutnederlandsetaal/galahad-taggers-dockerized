"""
Unit tests for the jcompat module.
Created on 2016/10/31

"""

import unittest

from sortedcontainers.sortedset import SortedSet
from chunker_steps.jcompat import HashMap, HashSet, JSortedSet, JList, JIterator, JListIterator


class TestHashMap(unittest.TestCase):

    def test_creation(self):
        HashMap()
        HashMap((('one', 1), ('two', 2)))

    def test_put(self):
        hashmap = HashMap()
        self.assertEqual({}, hashmap)
        hashmap['one'] = 1
        self.assertEqual({'one': 1}, hashmap)
        hashmap.put('two', 2)
        self.assertEqual({'one': 1, 'two': 2}, hashmap)

    def test_contains_key_negative(self):
        hashmap = HashMap()
        self.assertFalse(hashmap.containsKey('key-1'))
        hashmap.put('key-11', 'value-11')
        self.assertFalse(hashmap.containsKey('key-1'))

    def test_contains_key_positive(self):
        hashmap = HashMap()
        hashmap.put('key-11', 'value-11')
        self.assertTrue(hashmap.containsKey('key-11'))


class TestHashSet(unittest.TestCase):

    def test_creation(self):
        HashSet()
        HashSet((4, 3, 3, 3, 2, 'five'))

    def test_contains_positive(self):
        aset = HashSet((4, 3, 3, 3, 2, 'five'))
        self.assertTrue(aset.contains(3))
        self.assertTrue(aset.contains('five'))

    def test_contains_negative(self):
        aset = HashSet((5, 3, 2, 2, 11, 'six'))
        self.assertFalse(aset.contains(4))
        self.assertFalse(aset.contains(1))
        self.assertFalse(aset.contains('blah'))


class TestJSortedSet(unittest.TestCase):

    def test_creation(self):
        JSortedSet()
        JSortedSet((4, 3, 3, 3, 2, 9))

    def test_add(self):
        aset = JSortedSet()
        for item in (4, 3, 3, 3, 8, 2):
            aset.add(item)
        alist = list(aset)
        self.assertEqual([2, 3, 4, 8], alist)

    def test_add_all(self):
        aset = JSortedSet()
        aset.addAll((1, 2, 3, 4, 5))
        self.assertEqual(JSortedSet((1, 2, 3, 4, 5)), aset)

    def test_contains_positive(self):
        aset = JSortedSet((4, 3, 3, 3, 2, 11))
        self.assertTrue(aset.contains(2))
        self.assertTrue(aset.contains(3))
        self.assertTrue(aset.contains(4))
        self.assertTrue(aset.contains(11))

    def test_contains_negative(self):
        aset = JSortedSet((5, 3, 2, 2, 11))
        self.assertFalse(aset.contains(4))
        self.assertFalse(aset.contains(1))
        self.assertFalse(aset.contains('blah'))

    def test_remove_does_it_indeed(self):
        aset = JSortedSet((4, 1, 1, 5, 9))
        aset.remove(1)
        self.assertEqual(JSortedSet((4, 5, 9)), aset)

    def test_remove_returns_true(self):
        aset = JSortedSet((3, 1, 1, 4, 8))
        self.assertTrue(aset.remove(1))
        self.assertEqual(JSortedSet((3, 4, 8)), aset)

    def test_remove_returns_false(self):
        aset = JSortedSet((6, 2, 2, 5, 11))
        self.assertFalse(aset.remove(7))
        self.assertEqual(JSortedSet((2, 5, 6, 11)), aset)


class TestJList(unittest.TestCase):

    def test_creation(self):
        JList()
        JList((1, 2, 3, 4, 5, 'blah'))

    def test_add(self):
        alist = JList()
        self.assertEqual(0, len(alist))
        alist.add(15)
        self.assertEqual(1, len(alist))
        self.assertEqual(JList((15,)), alist)

    def test_get_success(self):
        alist = JList((1, 2, 3, 4, 5, 'blah'))
        self.assertEqual(1, alist.get(0))
        self.assertEqual(3, alist.get(2))
        self.assertEqual('blah', alist.get(5))

    def test_get_wrong_index_fails(self):
        alist = JList((11, 12, 13, 14, 15, 'bar'))
        self.assertRaises(IndexError, alist.get, 6)
        self.assertRaises(IndexError, alist.get, 60)

    def test_sub_list(self):
        alist = JList((21, 22, 23, 24, 29, 39, 42))
        sublist = alist.subList(1, 4)
        self.assertEqual([22, 23, 24], list(sublist))

    def test_sub_list_empty_result(self):
        alist = JList((31, 32, 39))
        sublist = alist.subList(1, 1)
        self.assertEqual([], list(sublist))


class TestJIterator(unittest.TestCase):

    def test_creation_default_fails(self):
        self.assertRaises(TypeError, JIterator)

    def test_creation_list(self):
        JIterator(['one', 'two', 'three'])

    def test_creation_iterator(self):
        JIterator(range(10))

    def test_has_next(self):
        it = JIterator(['one'])
        self.assertTrue(it.has_next())
        self.assertTrue(it.has_next())
        self.assertTrue(it.has_next())
        it = JIterator([])
        self.assertFalse(it.has_next())
        self.assertFalse(it.has_next())
        self.assertFalse(it.has_next())

    def test_next(self):
        it = JIterator(['one'])
        self.assertEqual('one', it.next())
        self.assertRaises(StopIteration, it.next)

    def test_usage_with_for(self):
        it = JIterator(('a', 'b', 'c', 'd'))
        check_list = list()
        for item in it:
            check_list.append(item)
        expected = ['a', 'b', 'c', 'd']
        self.assertEqual(expected, check_list)

    def test_usage_with_for_with_range(self):
        it = JIterator(range(5))
        check_list = list()
        for item in it:
            check_list.append(item)
        expected = [0, 1, 2, 3, 4]
        self.assertEqual(expected, check_list)

    def test_whishful_api(self):
        it = JIterator(('a', 'b', 'c'))
        check_list = list()
        while it.has_next():
            item = it.next()
            check_list.append((item, it.has_next()))
        expected = [('a', True), ('b', True), ('c', False)]
        self.assertEqual(expected, check_list)

    def test__repr__(self):
        it = JIterator(('a', 'b', 'c'))
        regex = "^<JIterator\(has_next=True, next='a'\) object at 0x[0-9A-F]{16}>$"
        self.assertRegex(repr(it), regex)

    def test_remove_not_implemented(self):
        it = JIterator(('a', 'b', 'c'))
        it.next()
        self.assertRaises(NotImplementedError, it.remove)


class TestJListIterator(unittest.TestCase):

    def test_creation_default_fails(self):
        self.assertRaises(TypeError, JListIterator)

    def test_creation_list(self):
        JListIterator(['one', 'two', 'three'])

    def test_creation_sorted_set(self):
        JListIterator(SortedSet(['one', 'two', 'three']))

    def test_creation_iterator_fails(self):
        self.assertRaises(AssertionError, JListIterator, range(10))

    def test_has_next(self):
        it = JListIterator(['one'])
        self.assertTrue(it.has_next())
        self.assertTrue(it.has_next())
        self.assertTrue(it.has_next())
        it = JListIterator([])
        self.assertFalse(it.has_next())
        self.assertFalse(it.has_next())
        self.assertFalse(it.has_next())

    def test_next(self):
        it = JListIterator(['one'])
        self.assertEqual('one', it.next())
        self.assertRaises(StopIteration, it.next)

    def test_usage_with_for(self):
        it = JListIterator(['a', 'b', 'c', 'd'])
        check_list = list()
        for item in it:
            check_list.append(item)
        expected = ['a', 'b', 'c', 'd']
        self.assertEqual(expected, check_list)

    def test_whishful_api(self):
        it = JListIterator(['a', 'b', 'c'])
        check_list = list()
        while it.has_next():
            item = it.next()
            check_list.append((item, it.has_next()))
        expected = [('a', True), ('b', True), ('c', False)]
        self.assertEqual(expected, check_list)

    def test_whishful_api_with_sorted_set(self):
        it = JListIterator(SortedSet(['a', 'b', 'c']))
        check_list = list()
        while it.has_next():
            item = it.next()
            check_list.append((item, it.has_next()))
        expected = [('a', True), ('b', True), ('c', False)]
        self.assertEqual(expected, check_list)

    def test__repr__(self):
        it = JListIterator(['a', 'b', 'c'])
        regex = "^<JListIterator\(has_next=True, next='a'\) object at 0x[0-9A-F]{16}>$"
        self.assertRegex(repr(it), regex)

    def test_remove_before_next_fails(self):
        it = JListIterator([1, 2, 3])
        self.assertRaises(IndexError, it.remove)

    def test_remove_first(self):
        alist = [1, 2, 3]
        it = JListIterator(alist)
        self.assertEqual(1, it.next())
        it.remove()
        self.assertEqual([2, 3], alist)

    def test_remove_midst(self):
        alist = JList(('a', 'b', 'c', 'd'))
        self.assertEqual(['a', 'b', 'c', 'd'], alist)
        it = JListIterator(alist)
        self.assertEqual('a', it.next())
        self.assertEqual('b', it.next())
        it.remove()
        self.assertEqual('c', it.next())
        self.assertEqual('d', it.next())
        self.assertRaises(StopIteration, it.next)
        self.assertEqual(['a', 'c', 'd'], alist)

    def test_remove_last(self):
        alist = [1, 2, 3]
        it = JListIterator(alist)
        self.assertEqual(1, it.next())
        self.assertEqual(2, it.next())
        self.assertEqual(3, it.next())
        it.remove()
        self.assertEqual([1, 2], alist)

    def test_remove_from_single_element_list(self):
        alist = [1]
        it = JListIterator(alist)
        self.assertEqual(1, it.next())
        it.remove()
        self.assertEqual([], alist)


if __name__ == '__main__':
    unittest.main(verbosity=0)
