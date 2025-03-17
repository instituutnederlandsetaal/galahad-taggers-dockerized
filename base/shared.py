# Contains values used by both tagger worker and webservice

import os

UPLOAD_FOLDER = "input"
STATUS_FOLDER = "status"
PROCESS_FOLDER = "process"
OUTPUT_FOLDER = "output"
ERROR_FOLDER = "error"

for folder in [
    UPLOAD_FOLDER,
    STATUS_FOLDER,
    PROCESS_FOLDER,
    OUTPUT_FOLDER,
    ERROR_FOLDER,
]:
    os.makedirs(folder, exist_ok=True)

TEXT_EXTENSIONS = {"txt"}
ALLOWED_EXTENSIONS = TEXT_EXTENSIONS


def file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[1].lower()
