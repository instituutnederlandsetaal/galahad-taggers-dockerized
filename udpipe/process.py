# standard
import contextlib
import threading
import itertools

# local
from udpipe2_server import Models
import wembeddings

# The extension of output files produced by the tagger.
OUTPUT_EXTENSION = ".conllu"
# Expected throughput in chars per sec.
PROCESSING_SPEED = 370

tagger = None


class DotDict:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = DotDict(value)  # Recursively convert nested dictionaries
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


def init() -> None:
    """
    Any initialization the tagger may need before processing.
    """
    global tagger
    args = {
        "port": "",
        "default_model": "nl_alpino",
        "models": [
            "dutch-alpino-ud-2.12-230717:nl_alpino-ud-2.12-230717:nl:nld:dut",
            "models/nl_all-ud-2.12-230717.model",
            "nl_alpino",
            "https://ufal.mff.cuni.cz/udpipe/2/models#universal_dependencies_212_models",
        ],
        "batch_size": 32,
        "concurrent": None,
        "logfile": None,
        "max_request_size": 4096 * 1024,
        "preload_models": [],
        "threads": 0,
        "wembedding_preload_models": [],
        "wembedding_server": None,
    }

    # Create the WEmbeddings client
    if args["wembedding_server"] is not None:
        args["wembedding_server"] = wembeddings.WEmbeddings.ClientNetwork(
            args["wembedding_server"]
        )
    else:
        args["wembedding_server"] = wembeddings.WEmbeddings(
            threads=args["threads"], preload_models=args["wembedding_preload_models"]
        )

    # Create a semaphore if needed
    args["optional_semaphore"] = (
        threading.Semaphore(args["concurrent"])
        if args["concurrent"] is not None
        else contextlib.nullcontext()
    )

    # Load the models
    models = Models(DotDict(args))
    tagger = models.models_list[0]
    print("Model initialized.")


def process(in_file: str, out_file: str) -> None:
    """
    Process the file with the global tagger instance.
    Pie outputs to the same directory as the input file.
    We process the file in a temporary directory so we don't polute /input.
    """
    with open(out_file, "w+", encoding="utf-8") as f_out:
        with open(in_file, "r", encoding="utf-8") as f_in:
            text = f_in.read()
            sentences = tagger.tokenize(text, "")
            writer = tagger.create_writer("conllu")
            conllu = tagger.predict(sentences, True, True, writer)
            f_out.write(conllu)


if __name__ == "__main__":
    init()
    process("input.txt", "output.conllu")
