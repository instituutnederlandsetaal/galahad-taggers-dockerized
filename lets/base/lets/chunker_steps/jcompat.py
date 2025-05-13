"""
Adapters for porting lt3_java/preprocessor_java/Chunker/src/domein Java package.
Created on 2016/10/31

Using sortedcontainers (http://www.grantjenks.com/docs/sortedcontainers/) here.

"""

from sortedcontainers.sortedset import SortedSet


class JList(list):
    """A Python list to Java List adapter providing (only!) get(), add()
       and subList() methods."""

    def get(self, idx):
        return self[idx]

    def add(self, elem):
        self.append(elem)

    def subList(self, idx_strart, idx_end):
        return self[idx_strart: idx_end]


class MapMixin:
    """Mixin to turn a Python dict-like class into a Java Map with put()
       and containsKey() methods."""

    def put(self, key, value):
        self[key] = value

    def containsKey(self, key):
        return key in self


class HashMap(MapMixin, dict):
    """An adapter turning a Python dict into a Java HashMap with (only!) put()
       and containsKey() methods."""


class JSetMixin:
    """Mixin to turn a Python set into a Java Set api with contains() and remove()
       methods."""

    def contains(self, elem):
        return elem in self

    def remove(self, elem):
        try:
            super(JSetMixin, self).remove(elem)
            return True
        except KeyError:
            return False


class HashSet(JSetMixin, set):
    """A Python set to Java HashSet adapter."""


class JSortedSet(JSetMixin, SortedSet):
    """A Python set to Java SortedSet adapter."""

    def addAll(self, seq):
        self.update(seq)


class JIterator(object):
    """A simulating implementation of Java Iterator with (only!) next()
       and hasNext() methods. remove() not implemented to allow for
       wrapping up arbitrary Python sequences. (Use JListIterator for
       an iterator with working remove().)"""

    def __init__(self, sequence):
        self._seq_iter = iter(sequence)
        self._next = self._get_next()

    def __repr__(self):
        return "<{}(has_next={}, next={!r}) object at 0x{:016X}>" \
                    .format(self.__class__.__name__, self.has_next(), self._next, id(self))

    def _get_next(self):
        try:
            return next(self._seq_iter)
        except StopIteration:
            return None

    def has_next(self):
        """Returns True iff this iterator has at least one more item, False
           otherwise."""
        return self._next is not None

    hasNext = has_next

    def __iter__(self):
        return self

    def __next__(self):
        result = self._next
        if result is None:
            raise StopIteration
        self._next = self._get_next()
        return result

    next = __next__
    """Returns the next item of this iterator, if any. Raises StopIteration
       if no more items are available.
    """

    def remove(self):
        """Removes the element last returned by next().
           Raises NotImplementedError if underlying collection is not an
           instance of list -- we cannot operate with underlying sequence
           if it not a list but a Python iterator in the general sense."""
        raise NotImplementedError("see docstring")


class JListIterator(JIterator):
    """A simulating implementation of Java ListIterator with (only!) next(),
       hasNext() and remove() methods."""

    ALLOWED_SEQUENCE_TYPES = (list, SortedSet)

    def __init__(self, alist):
        assert isinstance(alist, self.ALLOWED_SEQUENCE_TYPES), \
                "accepting only {!r}, got {}".format(self.ALLOWED_SEQUENCE_TYPES, type(alist))
        self._mylist = alist
        self._idx = -1  #: reflects the current element's index if sequence is a list
        self._next = self._get_next()

    def _get_next(self):
        try:
            res = self._mylist[self._idx + 1]
        except IndexError:
            self._idx += 1  # we need this for remove() to work correctly for removing the last element
            return None
        else:
            self._idx += 1
            return res

    def remove(self):
        if self._idx < 1:
            raise IndexError("next() must be called before remove()")
        del self._mylist[self._idx - 1]
        self._idx -= 1
