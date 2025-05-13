import os
import sys
# Some path magic to import huggingface.
sys.path.append("./lets")
from lets.preprocessor import PreProcessor

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

preprocessor = None

def init() -> None:
    """
    Any initialization the tagger may need before processing.
    """



def process(in_file: str, out_file: str) -> None:
    """
    Process the file at path "in_file" and write the result to path "out_file".
    """
    preprocessor = PreProcessor(l=os.environ["LETS_LANG"])
    with open(out_file, "x") as f_out:
        f_out.write("token\tlemma\tpos\tchunk\tner\n")
        with open(in_file, "r") as f_in:
            corpus = f_in.readlines()
            output = preprocessor.process_lines(corpus)
            for field in output:
                f_out.write(f"{field}\n")
