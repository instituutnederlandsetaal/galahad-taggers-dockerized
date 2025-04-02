# standard
import os
import xml.etree.ElementTree as ET

# third-party
import stanza

# local
from conllu_tei_helper import parse_tei

# The extension of output files produced by the tagger.
OUTPUT_EXTENSION = ".conllu"

# Expected throughput in chars per sec.
# The timeout and expected job duration are based on this,
# so set it to a lower value to increase the timeout.
PROCESSING_SPEED = 370  # todo: measure this!

xml_nlp = None
txt_nlp = None


def init() -> None:
    """
    Any initialization the tagger may need before processing.
    """
    global xml_nlp
    xml_nlp = stanza.Pipeline(
        lang="nl",
        tokenize_pretokenized=True,
        processors="tokenize,lemma,pos,ner,depparse",
    )

    global txt_nlp
    stanza_model = os.getenv("STANZA_MODEL")
    if stanza_model == "alpino":
        txt_nlp = stanza.Pipeline(
            lang="nl",
            processors={
                "tokenize": "alpino",
                "lemma": "alpino",
                "pos": "alpino",
                "depparse": "alpino",
                "ner": "conll02",
            },
        )
    elif stanza_model == "lassysmall":
        txt_nlp = stanza.Pipeline(
            lang="nl",
            processors={
                "tokenize": "lassysmall",
                "lemma": "lassysmall",
                "pos": "lassysmall",
                "depparse": "lassysmall",
                "ner": "wikiner",
            },
        )


def process(in_file: str, out_file: str) -> None:
    """
    Process the file at path "in_file" and write the result to path "out_file".
    """
    with open(out_file, "w+", encoding="utf-8") as f_out:
        with open(in_file, "r", encoding="utf-8") as f_in:
            is_xml = is_file_xml(in_file)
            nlp = xml_nlp if is_xml else txt_nlp
            doc = parse_tei(in_file) if is_xml else f_in.read()

            result = nlp(doc)
            f_out.write("{:C}".format(result))
            f_out.write("\n")


def is_file_xml(in_file: str) -> bool:
    try:
        ET.parse(in_file)
        return True
    except:
        return False
