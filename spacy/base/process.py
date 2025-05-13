import spacy
import os
"""
Initialize the tagger if needed and process input files by calling the specific tagger implementation 
and ensuring the output is written to the expected file.
"""

# The extension of output files produced by the tagger.
OUTPUT_EXTENSION = ".tsv"

# Expected throughput in chars per sec.
# The timeout and expected job duration are based on this,
# so set it to a lower value to increase the timeout.
PROCESSING_SPEED = 370 # todo: measure this!

nlp = None

def init() -> None:
    """
    Any initialization the tagger may need before processing.
    """
    global nlp
    nlp = spacy.load(os.environ["SPACY_MODEL"])

nlp = None

def process(in_file: str, out_file: str) -> None:
    """
    Process the file at path "in_file" and write the result to path "out_file".
    """
    with open(out_file, "x") as f_out:
        f_out.write("token\tlemma\tpos\ttag\tdep\n")
        with open(in_file, "r") as f_in:
            corpus = f_in.readlines()
            for line in corpus:
                doc = nlp(line.strip())
                for sent in doc.sents:
                    for token in sent:
                        f_out.write(f"{token.text}\t{token.lemma_}\t{token.pos_}\t{token.tag_}\t{token.dep_}\n")
                    f_out.write("\n") # sentence boundaries

