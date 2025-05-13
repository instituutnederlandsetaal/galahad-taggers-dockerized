"""
Ported from lt3_java/preprocessor_java/Chunker/src/domein Java package.
Created on 2016/10/31

"""

from lets.abstract_step import AbstractStep
from lets.chunker_steps import PARSE_DELIM as DELIM
from lets.chunker_steps.chunker_util import matches
from lets.chunker_steps.jcompat import JList
from lets.chunker_steps.basic import Chunk, Word
from lets.chunker_steps.chunkers import get_chunk_function


class SentenceProcessor(AbstractStep):
    """A processor of sentence-wide tab-delimited text line word sequences."""

    def __init__(self, l='nl'):
        super(SentenceProcessor, self).__init__(l)
        self.l = l
        self._sent = None  # both truly initialized by self._reset_state()
        self._counter = None

    def _reset_state(self):
        self._sent = JList()  # TODO: revert to Python list
        self._counter = 0

    def _create_chunks(self, chunkboundaries):
        chunks = list()
        start = 0
        chunkId = 0
        for bound in chunkboundaries:
            chunks.append(Chunk(chunkId, self._sent[start: bound + 1], start, bound))
            start = bound + 1
            chunkId = chunkId + 1
        return chunks

    def _step_one(self, chunks):
        """Assign chunk type (NP + VP)   [comment copied from the Java code]"""
        for chk in chunks:
            if (chk.getMappedPosSequence().startswith("N") or "+N" in chk.getMappedPosSequence() or
                        chk.getMappedPosSequence() == "FW" or matches("^PRON-[a-z]+$", chk.getMappedPosSequence())):
                chk.setType("NP")
            elif chk.getMappedPosSequence().startswith("V") or "+V" in chk.getMappedPosSequence():
                chk.setType("VP")
            elif "ADJ" in chk.getMappedPosSequence():
                chk.setType("AP")
            elif "ADV" in chk.getMappedPosSequence():
                chk.setType("ADVP")
        return chunks

    def _step_two(self, chunks):
        """TODO: what does this step do?"""
        for chk in chunks:
            if (chk.getMappedPosSequence() == "PREP" and (len(chunks) > chk.getPosition() + 1) and
                        chunks[chk.getPosition() + 1].getType() == "NP"):
                chk.setType("PP")
        return chunks

    def _step_three(self, chunks):
        """TODO: what does this step do?"""
        for chk in chunks:
            if chk.getType() == "O":
                for w in chk.getChunk():
                    w.setPhr("O")
            else:
                for w in chk.getChunk():
                    w.setPhr("I-" + chk.getType())

                chk.getChunk().get(0).setPhr("B-" + chk.getType())
        return chunks

    def _process_sentence(self):
        """Processes this sentense's word sequence, accumulated internally."""
        chunker_fn = get_chunk_function(self.language)
        chunkboundaries = chunker_fn(self._sent)
        chunks = self._create_chunks(chunkboundaries)
        chunks = self._step_one(chunks)
        chunks = self._step_two(chunks)
        chunks = self._step_three(chunks)
        for word in self._sent:
            yield word.tab_delimited()
        yield ""

    def process_line(self, line):
        raise NotImplementedError("process_line() not used within SentenceProcessor")

    def process_lines(self, lines):
        """Accumulates all words coming out of this `lines` iterator; then processes them
           all together via self._process_sentence() yielding tab-delimited output text
           lines."""
        self._reset_state()
        for in_line in lines:
            if not in_line.strip():
                for out_line in self._process_sentence():
                    yield out_line
                self._reset_state()
            else:
                self._sent.append(Word(self._counter, *in_line.strip().split(DELIM), "", self.l))
                self._counter += 1


if __name__ == "__main__":
    SentenceProcessor.main()
