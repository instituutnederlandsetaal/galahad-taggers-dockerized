"""
Test data for unit-testing Sentence class.
Created on 2016/11/01

"""

#: sequence of tuples (token, lemma, pos, pos_mapped)
SENTENCE_DATA_1 = (
    ('local', 'local', 'JJ', 'ADJ'),
    ('communities', 'community', 'NNS', 'N'),
    (',', ',', ',', 'PCT'),
    ('migrants', 'migrant', 'NNS', 'N'),
    (',', ',', ',', 'PCT'),
    ('children', 'child', 'NNS', 'N'),
    (',', ',', ',', 'PCT'),
    ('persons', 'person', 'NNS', 'N'),
    ('with', 'with', 'IN', 'PREP'),
    ('disabilities', 'disability', 'NNS', 'N'),
    ('and', 'and', 'CC', 'CONJ-coord'),
    ('people', 'people', 'NNS', 'N'),
    ('in', 'in', 'IN', 'PREP'),
    ('vulnerable', 'vulnerable', 'JJ', 'ADJ'),
    ('situations', 'situation', 'NNS', 'N'),
    ('and', 'and', 'CC', 'CONJ-coord'),
    ('the', 'the', 'DT', 'DET'),
    ('right', 'right', 'NN', 'N'),
    ('to', 'to', 'TO', 'PREP'),
    ('development', 'development', 'NN', 'N'),
    (',', ',', ',', 'PCT'),
    ('as', 'as', 'RB', 'ADV'),
    ('well', 'well', 'RB', 'ADV'),
    ('as', 'as', 'IN', 'PREP'),
    ('gender', 'gender', 'NN', 'N'),
    ('equality', 'equality', 'NN', 'N'),
    (',', ',', ',', 'PCT'),
    ('empowerment', 'empowerment', 'NN', 'N'),
    ('of', 'of', 'IN', 'PREP'),
    ('women', 'woman', 'NNS', 'N'),
    ('and', 'and', 'CC', 'CONJ-coord'),
    ('intergenerational', 'intergenerational', 'JJ', 'ADJ'),
    ('equity', 'equity', 'NN', 'N'),
    (',', ',', ',', 'PCT'),
)

#: The Sentence output of the SENTENCE_DATA_1 input
SENTENCE_OUTPUT_1 = """\
local	local	JJ	B-NP
communities	community	NNS	I-NP
,	,	,	O
migrants	migrant	NNS	B-NP
,	,	,	O
children	child	NNS	B-NP
,	,	,	O
persons	person	NNS	B-NP
with	with	IN	B-PP
disabilities	disability	NNS	B-NP
and	and	CC	O
people	people	NNS	B-NP
in	in	IN	B-PP
vulnerable	vulnerable	JJ	B-NP
situations	situation	NNS	I-NP
and	and	CC	O
the	the	DT	B-NP
right	right	NN	I-NP
to	to	IN	B-PP
development	development	NN	B-NP
,	,	,	O
as	as	RB	B-ADVP
well	well	RB	I-ADVP
as	as	IN	B-PP
gender	gender	NN	B-NP
equality	equality	NN	I-NP
,	,	,	O
empowerment	empowerment	NN	B-NP
of	of	IN	B-PP
women	woman	NNS	B-NP
and	and	CC	O
intergenerational	intergenerational	JJ	B-NP
equity	equity	NN	I-NP
,	,	,	O

"""
