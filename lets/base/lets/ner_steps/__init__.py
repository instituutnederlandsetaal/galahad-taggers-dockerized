"""
lt3 NER steps package.
(Some common constants placed here.)

"""

import os
from os.path import join as pjoin

# FIXME: replace with appropriate relative location:

if 'HOME' in os.environ:
    HOME_DIR = os.environ['HOME']
    NER_MODELS_HOME = pjoin(HOME_DIR, 'Work/spaces/eclipse-4.6/ugent_lt3_java/preprocessor_java/NER/src/models')

#: Used for a field delimiter when representing LEM and POS parsing output as text lines
PARSE_DELIM = "\t"
